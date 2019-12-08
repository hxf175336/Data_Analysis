# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/18 16:04
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : dmbj.py
# Description :
# ----------------------------------
from gensim import corpora, models, similarities
import jieba
import urllib.request

d1 = urllib.request.urlopen("http://127.0.0.1/ljm.html").read().decode("utf-8", "ignore")
d2 = urllib.request.urlopen("http://127.0.0.1/gcd.html").read().decode("utf-8", "ignore")
data1 = jieba.cut(d1)
data2 = jieba.cut(d2)
data11 = ""
for item in data1:
	data11 += item + " "
data21 = ""
for item in data2:
	data21 += item + " "
documents = [data11, data21]
texts = [[word for word in document.split()]
		 for document in documents]
from collections import defaultdict

frequency = defaultdict(int)
for text in texts:
	for token in text:
		frequency[token] += 1

texts = [[token for token in text if frequency[token] > 25]
		 for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('D:/Python35/12345.txt')
doc3 = "D:/Python35/d3.txt"
d3 = urllib.request.urlopen("http://127.0.0.1/dmbj.html").read().decode("utf-8", "ignore")
data3 = jieba.cut(d3)
data31 = ""
for item in data3:
	data31 += item + " "
new_doc = data31
new_vec = dictionary.doc2bow(new_doc.split())
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('D:/Python35/6562.txt', corpus)
tfidf = models.TfidfModel(corpus)

featureNum = len(dictionary.token2id.keys())
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=featureNum)
sims = index[tfidf[new_vec]]

print(sims)
