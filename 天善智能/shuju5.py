# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/16 16:24
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : shuju5.py
# Description :数据规约
# ----------------------------------
'''
数据规约
	1、概述
		1、属性规约：对属性进行精简
		2、数值规约：对数值进行精简
	2、主成分分析
		1、属性规约值主成分
		2、PCA算法
		3、实战
'''

# 主成分分析
from sklearn.decomposition import PCA
import pymysql
import pandas as pd
import numpy as np

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='csdn')  # 连接数据库
sql = 'select hits,comment from myhexun'  # sql语句
data9 = pd.read_sql(sql, conn)  # 读入sql数据
ch=data9[u'comment']/data9['hits']   # 评点比
data9[u"评点比"]=ch
# print(data9)
# ---主成分分析进行中---
pca1=PCA()
pca1.fit(data9)
# 返回各个模型中的特征向量
Characteristic=pca1.components_
# print(Characteristic)
'''
特征向量：
	[[ 9.99988245e-01  4.84828800e-03 -5.89693311e-05]
	 [-4.40844610e-03  9.14197207e-01  4.05245645e-01]
 	[ 2.01865720e-03 -4.05240622e-01  9.14207834e-01]]
'''
#各个成分中各自方差百分比，代表贡献率
rate=pca1.explained_variance_ratio_
# print(rate)
'''
贡献率结果：
	[9.99964468e-01 3.03380241e-05 5.19348918e-06]
'''

# 降维
pca2=PCA(2)
pca2.fit(data9)
reduction=pca2.transform(data9)#降维
print(reduction)
'''
[[-751.45243231   -1.17256816]
 [-456.45105186   -1.55758013]
 [-560.45467747   -2.01458137]
 ...
 [-770.45220897   -1.08880769]
 [-771.45219722   -1.08439924]
 [-763.4038739     8.4725782 ]]
'''
recovery=pca2.inverse_transform(reduction)#恢复
print(recovery)
'''
[[ 2.10003975e+01 -7.97941953e-02  1.80012749e-01]
 [ 3.16000008e+02  9.98480589e-01  6.59229089e-03]
 [ 2.11999619e+02  7.64518072e-02 -1.72472445e-01]
 ...
 [ 2.00047491e+00 -9.53369914e-02  2.15076721e-01]
 [ 1.00047898e+00 -9.61550333e-02  2.16922194e-01]
 [ 9.00657628e+00  8.67982763e+00  4.08937108e+00]]

'''
