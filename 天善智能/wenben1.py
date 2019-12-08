# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/17 9:38
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : wenben1.py
# Description :文本
# ----------------------------------
'''
文本挖掘
	1、分词
		1.全模式
		2.精准模式
		3.搜索引擎模式
		4.默认使用精准模式
	2、词性标注  import jieba.posseg
		a：形容词
		c：连词
		d：副词
		e：叹词
		f：方位词
		i：成语
		m：数词
		n：名词
		nr：人名
		ns：地名
		nt：机构团体
		nz：其他专有名词
		p：介词
		r：代词
		t：时间
		u：助词
		v：动词
		vn：动名词
		w：标点符号
		un：未知词语
	3、词典加载
	 	jieba.load_userdict("filename")
	4、更改词频
	5、提取关键词
		import jieba.analyse
	6、实例

'''
import jieba

# 1、分词
sentence = '我喜欢上海东方明珠'
print('-------------------------全模式-------------------------------------')
w1 = jieba.cut(sentence,cut_all=True) #全模式,分词
for item in w1:
	print(item)
print("")
'''
-------------------------全模式-------------------------------------
我
Loading model cost 0.701 seconds.
喜欢
上海
Prefix dict has been built succesfully.
上海东方
海东
东方
东方明珠
方明
明珠

'''

print('-------------------------精准模式-------------------------------------')
w2 = jieba.cut(sentence,cut_all=False) #精准模式,分词
for item in w2:
	print(item)
print("")
'''
-------------------------精准模式-------------------------------------
我
喜欢
上海
东方明珠
'''

print('-------------------------搜索引擎模式-------------------------------------')
w3 = jieba.cut_for_search(sentence) #精准模式,分词
for item in w3:
	print(item)
print("")
'''
-------------------------搜索引擎模式-------------------------------------
我
喜欢
上海
东方
方明
明珠
东方明珠
'''

print('-------------------------不带参数默认使用精准模式-------------------------------------')
w4 = jieba.cut(sentence) #精准模式,分词
for item in w4:
	print(item)
print("")
'''
-------------------------不带参数默认使用精准模式-------------------------------------
我
喜欢
上海
东方明珠
'''

# 2、词性标注
import jieba.posseg
w5=jieba.posseg.cut(sentence)
# .flag词性
# .word词语
print('--------------------------词性标注-------------------------------------')
for item in w5:
	print(item.word+'----'+item.flag)
print("")
'''
--------------------------词性标注-------------------------------------
我----r
喜欢----v
上海----ns
东方明珠----nr

'''

print('--------------------------词典加载-------------------------------------')
# 3、词典加载
jieba.load_userdict("D:\software\Anaconda3\Lib\site-packages\jieba\dic2.txt")
sentence2 = "天善智能是一个很好的机构"
w6=jieba.posseg.cut(sentence2)
for item in w6:
	print(item.word+'-----'+item.flag)

print('--------------------------更改词频-------------------------------------')
# 4、更改词频
sentence="我喜欢上海东方明珠"
w7=jieba.cut(sentence)
for item in w7:
	print(item)
print("")
jieba.suggest_freq("上海东方",True)
w8=jieba.cut(sentence)
for item in w8:
	print(item)
print("")
'''
--------------------------更改词频-------------------------------------
我
喜欢
上海
东方明珠

我
喜欢
上海
东方明珠
'''
import jieba.analyse
sentence3="我喜欢上海东方明珠"
# 5、提取关键词
print('--------------------------提取关键词-------------------------------------')
tag=jieba.analyse.extract_tags(sentence3,2) #参数：句子 关键词个数
print(tag)
print("")
'''
--------------------------提取关键词-------------------------------------
['东方明珠', '喜欢']
'''

# 6、返回词语的位置
print('--------------------------返回词语的位置-------------------------------------')
w9 = jieba.tokenize(sentence)
for item in w9:
	print(item)
print("")
w10 = jieba.tokenize(sentence,mode="search") #以搜索引擎方式
for item in w10:
	print(item)
print("")
'''
--------------------------返回词语的位置-------------------------------------
('我', 0, 1)
('喜欢', 1, 3)
('上海', 3, 5)
('东方明珠', 5, 9)

('我', 0, 1)
('喜欢', 1, 3)
('上海', 3, 5)
('东方', 5, 7)
('方明', 6, 8)
('明珠', 7, 9)
('东方明珠', 5, 9)
'''

#修正1：add_word只能调高词频，不能调低词频，使用jieba.suggest_freq("词语",True)也一样
# sentence="我喜欢上海东方明珠"
# #jieba.add_word("我喜欢")
# jieba.suggest_freq("我喜欢",True)
# w7=jieba.cut(sentence)
# for item in w7:
#     print(item)
# print("")
# #修正2：按理来说调低词频可以使用del_word(词语)或者jieba.suggest_freq(("词1-前","词1-后"),True)，但是这里无法降低词频，有可能是电脑问题，或其他问题，各位同学也可以研究一下这个地方
# '''----问题代码开始----'''
# sentence="上海体育场不错的"
# #jieba.del_word("上海体育场")
# jieba.suggest_freq(("上海","体育场"),True)
# w8=jieba.cut(sentence,)
# for item in w8:
#     print(item)
# sentence="稻云科技是做云计算的"
# w7=jieba.cut(sentence)
# print('--------------------------更改词频-------------------------------------')
# for item in w7:
# 	print(item)

# 实例
# 分析血尸的词频
print('--------------------------分析血尸的词频-------------------------------------')
data=open("data/血尸.txt").read()
tag=jieba.analyse.extract_tags(data,30)
print(tag)
print("")
'''
--------------------------分析血尸的词频-------------------------------------
['老三', '二哥', '东西', '伢子', '烟头', '耗子', '血尸', '洞里', '下面', '独眼', '一声', '听到', '知道', '下去', '时候', '血红', '血淋淋', '竟然', '什么', '匣子', '好像', '绳子', '一看', '出来', '梭子', '大叫', '大胡子', '过去', '肯定', '老二']
'''
#盗墓笔记的关键词提取
#编码问题解决方案
print('--------------------------盗墓笔记的关键词提取------------------------------------')
data=open("data/盗墓笔记2.txt","r",encoding='utf-8').read()
# print(data)
import urllib.request
# data=urllib.request.urlopen("http://127.0.0.1/dmbj.html").read().decode("utf-8","ignore")
tag=jieba.analyse.extract_tags(data,30)
print(tag)
'''
--------------------------盗墓笔记的关键词提取------------------------------------
['三叔', '我们', '胖子', '油瓶', '潘子', '什么', '东西', '知道', '这里', '但是', '没有', '一个', '看到', '老痒', '事情', '时候', '一下', '感觉', '阿宁', '已经', '这个', '这么', '他们', '起来', '可能', '里面', '不是', '自己', '地方', '就是']
'''
## 可以下载盘古词库


