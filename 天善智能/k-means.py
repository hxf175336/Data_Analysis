# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/22 14:07
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : k-means.py
# Description : 聚类算法实战
# ----------------------------------
'''
k-means算法的步骤：
	1、随机选择k个点作为聚类中心；
	2、计算各个点到这k个点的距离；
	3、将对应的点聚到与他最近的这个聚类中心；
	4、重新计算聚类中心；
	5、比较当前聚类中心，如果是通一个人点，得到聚类结果，若为不同点，则重复2-5。
'''

# k-means算法
'''
# 通过程序实现录取学生的聚类
import numpy as np
import pandas as pd
import matplotlib.pylab as pyl

fname="data/luqu.csv"
dataf=pd.read_csv(fname)     # 得到的是数据框
# print(dataf)
x=dataf.iloc[:,1:4].values   # 提取数据
# print(x)
# 聚类
from sklearn.cluster import Birch
from sklearn.cluster import KMeans
kms=KMeans(n_clusters=2)
y=kms.fit_predict(x)
# print(y)

# x代表学生序号，y代表学生类别
s=np.arange(0,len(y))
# print(s)
pyl.plot(s,y,"o")
pyl.show()
'''
# 通过程序实现商品的聚类
import pandas as pd
import numpy as np
import matplotlib.pylab as pyl
import pymysql

# 导入数据
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="csdn")
sql = "select price,comment from taob limit 300"
dataf = pd.read_sql(sql, conn)
# print(dataf)
# 取出数据
x = dataf.iloc[:, :].values
# 聚类
from sklearn.cluster import Birch
from sklearn.cluster import KMeans

kms = KMeans(n_clusters=3)
y = kms.fit_predict(x)
print(y)
for i in range(0, len(y)):
	if (y[i] == 0):
		pyl.plot(dataf.iloc[i:i + 1, 0:1].values, dataf.iloc[i:i + 1, 1:2].values, "*r")
	elif (y[i] == 1):
		pyl.plot(dataf.iloc[i:i + 1, 0:1].values, dataf.iloc[i:i + 1, 1:2].values, "sy")
	elif(y[i] == 2):
		pyl.plot(dataf.iloc[i:i + 1, 0:1].values, dataf.iloc[i:i + 1, 1:2].values, "pk")
pyl.show()

'''
# 作业：使用聚类来实现文本的聚类
1、用爬虫去爬100个百度百科的词条内容
2、将这些内容分别存入各文件中
3、进行分词，计算tf-idf
4、进行聚类
5、对文档进行分类，k=3
'''

"""
ni ni  
"""
