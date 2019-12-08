# -*- coding: gbk -*-

"""
    ����:     ����
    �汾:     1.0
    ����:     2017/03/01
    ��Ŀ���ƣ�ʶ��Twitter�û��Ա� (Twitter User Gender Classification)
    Kaggle��ַ��https://www.kaggle.com/crowdflower/twitter-user-gender-classification
"""
import os
import pandas as pd
from common_tools import get_dataset_filename, unzip, cal_acc
from pd_tools import inspect_dataset, check_profile_image, \
	split_train_test, clean_text, proc_text, get_word_list_from_data, \
	extract_tf_idf, extract_rgb_feat, extract_rgb_hist_feat
import nltk
from nltk.text import TextCollection
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA

# �������ݼ�·��

dataset_path = './dataset'  # ���ݼ�·��
zip_filename = 'twitter-user-gender-classification.zip'  # zip�ļ���
zip_filepath = os.path.join(dataset_path, zip_filename)  # zip�ļ�·��
cln_datapath = './cln_data.csv'  # ��ϴ�õ�����·��

# �Ƿ��һ������
is_first_run = False


def run_main():
	"""
		������
	"""
	# ��������
	dataset_filename = get_dataset_filename(zip_filepath)  # ���ݼ��ļ�������zip�У�
	dataset_filepath = os.path.join(dataset_path, dataset_filename)  # ���ݼ��ļ�·��

	if is_first_run:
		print('��ѹzip...', end='')
		unzip(zip_filepath, dataset_path)
		print('���.')

		# ��ȡ����
		data = pd.read_csv(dataset_filepath, encoding='latin1',
						   usecols=['gender', 'description', 'link_color',
									'profileimage', 'sidebar_color', 'text'])
		# 1. �鿴���ص����ݼ�
		inspect_dataset(data)

		# 2. ������ϴ
		# 2.1. ���� 'gender' �й�������
		filtered_data = data[(data['gender'] == 'male') | (data['gender'] == 'female')]

		# 2.2 ���˵� 'description' ��Ϊ�յ�����
		filtered_data = filtered_data.dropna(subset=['description'])

		# 2.3 ���˵� 'link_color' �к� 'sidebar_color' �зǷ���16��������
		filtered_data = filtered_data[filtered_data['link_color'].str.len() == 6]
		filtered_data = filtered_data[filtered_data['sidebar_color'].str.len() == 6]

		# 2.4 ��ϴ�ı�����
		print('��ϴ�ı�����...')
		cln_desc = filtered_data['description'].apply(clean_text)
		cln_text = filtered_data['text'].apply(clean_text)
		filtered_data['cln_desc'] = cln_desc
		filtered_data['cln_text'] = cln_text

		# 2.5 ����profileimage�������ж�ͷ��ͼƬ�Ƿ���Ч��
		# �������µ��д���ͷ��ͼƬ�����·��
		print('����ͷ������...')
		saved_img_s = filtered_data['profileimage'].apply(check_profile_image)
		filtered_data['saved_image'] = saved_img_s
		# ���˵���Ч��ͷ������
		filtered_data = filtered_data[filtered_data['saved_image'] != '']

		# ���洦��õ�����
		filtered_data.to_csv(cln_datapath, index=False)

	# ��ȡ����õ�����
	clean_data = pd.read_csv(cln_datapath, encoding='latin1',
							 usecols=['gender', 'cln_desc', 'cln_text',
									  'link_color', 'sidebar_color', 'saved_image'])

	# �鿴label�ķֲ�
	print(clean_data.groupby('gender').size())

	# �滻male->0, female->1
	clean_data.loc[clean_data['gender'] == 'male', 'label'] = 0
	clean_data.loc[clean_data['gender'] == 'female', 'label'] = 1

	# 3. �ָ����ݼ�
	# �ִ� ȥ��ͣ�ô�
	proc_desc_s = clean_data['cln_desc'].apply(proc_text)
	clean_data['desc_words'] = proc_desc_s

	proc_text_s = clean_data['cln_text'].apply(proc_text)
	clean_data['text_words'] = proc_text_s

	df_train, df_test = split_train_test(clean_data)
	# �鿴ѵ�������Լ�������Ϣ
	print('ѵ�����и�������ݸ�����', df_train.groupby('label').size())
	print('���Լ��и�������ݸ�����', df_test.groupby('label').size())

	# 4. ��������
	# 4.1 ѵ������������ȡ
	print('ѵ������������ȡ��')
	# 4.1.1 �ı�����
	# description����
	print('ͳ��description��Ƶ...')
	n_desc_common_words = 50
	desc_words_in_train = get_word_list_from_data(df_train['desc_words'])
	fdisk = nltk.FreqDist(desc_words_in_train)
	desc_common_words_freqs = fdisk.most_common(n_desc_common_words)
	print('descriptino�г�������{}�����ǣ�'.format(n_desc_common_words))
	for word, count in desc_common_words_freqs:
		print('{}: {}��'.format(word, count))
	print()

	# ��ȡdesc�ı���TF-IDF����
	print('��ȡdesc�ı�����...', end=' ')
	desc_collection = TextCollection(df_train['desc_words'].values.tolist())
	tr_desc_feat = extract_tf_idf(df_train['desc_words'], desc_collection, desc_common_words_freqs)
	print('���')
	print()

	# text����
	print('ͳ��text��Ƶ...')
	n_text_common_words = 50
	text_words_in_train = get_word_list_from_data(df_train['text_words'])
	fdisk = nltk.FreqDist(text_words_in_train)
	text_common_words_freqs = fdisk.most_common(n_text_common_words)
	print('text�г�������{}�����ǣ�'.format(n_text_common_words))
	for word, count in text_common_words_freqs:
		print('{}: {}��'.format(word, count))
	print()

	# ��ȡtext�ı�TF-IDF����
	text_collection = TextCollection(df_train['text_words'].values.tolist())
	print('��ȡtext�ı�����...', end=' ')
	tr_text_feat = extract_tf_idf(df_train['text_words'], text_collection, text_common_words_freqs)
	print('���')
	print()

	# 4.1.2 ͼ������
	# link color��RGB����
	tr_link_color_feat_ = extract_rgb_feat(df_train['link_color'])
	tr_sidebar_color_feat = extract_rgb_feat(df_train['sidebar_color'])

	# ͷ���RGBֱ��ͼ����
	tr_profile_img_hist_feat = extract_rgb_hist_feat(df_train['saved_image'])

	# ����ı�������ͼ������
	tr_feat = np.hstack((tr_desc_feat, tr_text_feat, tr_link_color_feat_,
						 tr_sidebar_color_feat, tr_profile_img_hist_feat))

	# ������Χ��һ��
	scaler = StandardScaler()
	tr_feat_scaled = scaler.fit_transform(tr_feat)

	# ��ȡѵ������ǩ
	tr_labels = df_train['label'].values

	# 4.2 ��������������ȡ
	print('��������������ȡ��')
	# 4.2.1 �ı�����
	# description����
	# ��ȡdesc�ı���TF-IDF����
	print('��ȡdesc�ı�����...', end=' ')
	te_desc_feat = extract_tf_idf(df_test['desc_words'], desc_collection, desc_common_words_freqs)
	print('���')
	print()

	# text����
	# ��ȡtext�ı�TF-IDF����
	print('��ȡtext�ı�����...', end=' ')
	te_text_feat = extract_tf_idf(df_test['text_words'], text_collection, text_common_words_freqs)
	print('���')
	print()

	# 4.2.2 ͼ������
	# link color��RGB����
	te_link_color_feat_ = extract_rgb_feat(df_test['link_color'])
	te_sidebar_color_feat = extract_rgb_feat(df_test['sidebar_color'])

	# ͷ���RGBֱ��ͼ����
	te_profile_img_hist_feat = extract_rgb_hist_feat(df_test['saved_image'])

	# ����ı�������ͼ������
	te_feat = np.hstack((te_desc_feat, te_text_feat, te_link_color_feat_,
						 te_sidebar_color_feat, te_profile_img_hist_feat))

	# ������Χ��һ��
	te_feat_scaled = scaler.transform(te_feat)

	# ��ȡѵ������ǩ
	te_labels = df_test['label'].values

	# 4.3 PCA��ά����
	pca = PCA(n_components=0.95)  # ����95%�ۼƹ����ʵ���������
	tr_feat_scaled_pca = pca.fit_transform(tr_feat_scaled)
	te_feat_scaled_pca = pca.transform(te_feat_scaled)

	# 5. ģ�ͽ���ѵ�����Ա�PCA����ǰ���Ч��
	# ʹ��δ����PCA����������
	lr_model = LogisticRegression()
	lr_model.fit(tr_feat_scaled, tr_labels)

	# ʹ��PCA�����������
	lr_pca_model = LogisticRegression()
	lr_pca_model.fit(tr_feat_scaled_pca, tr_labels)

	# 6. ģ�Ͳ���
	pred_labels = lr_model.predict(te_feat_scaled)
	pred_pca_labels = lr_pca_model.predict(te_feat_scaled_pca)
	# ׼ȷ��
	print('δ����PCA����:')
	print('����ά�ȣ�', tr_feat_scaled.shape[1])
	print('׼ȷ�ʣ�{}'.format(cal_acc(te_labels, pred_labels)))

	print()
	print('����PCA������:')
	print('����ά�ȣ�', tr_feat_scaled_pca.shape[1])
	print('׼ȷ�ʣ�{}'.format(cal_acc(te_labels, pred_pca_labels)))

	# 7. ɾ����ѹ���ݣ�����ռ�
	if os.path.exists(dataset_filepath):
		os.remove(dataset_filepath)


if __name__ == '__main__':
	run_main()
