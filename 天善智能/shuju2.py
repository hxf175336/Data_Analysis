# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/15 12:28
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : shuju2.py
# Description :数据探索与数据清洗
# ----------------------------------
'''
数据探索与数据清洗

	数据探索的目的是及早发现数据的一些简单规律与特征，数据清洗的目的是留下可靠数据，避免脏数据的干扰。两者不分先后顺序。

	1.数据探索的核心是：
		1、数据质量分析
		2、数据特征分析（分布、对比、周期性、相关性、常见统计量等）

	2.数据清洗步骤：
		1、缺失值处理（通过describe与len直接发现、通过0数据发现）
		2、异常值处理（通过散点图发现）
			一般遇到缺失值，处理方式为（删除、插补、不处理）
		插补的方式：均值插补、中位数插值、众数插补、固定值插补、最近数据插补、回归插补、拉格朗日插值、牛顿插值法、分段插值等等
			遇到异常值，一般处理方式为视为缺失值、删除、修补（平均数、中位数等等）、不处理。
	3、数据集成的过程
		1、观察数据，发现其中关系
		2、进行数据读取与整合
		3、去除重复数据


'''

'''
#导入数据
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pylab as pyl

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='csdn') # 连接数据库
sql='select * from taob'                 # sql语句
data=pd.read_sql(sql,conn)               # 读入sql数据
# print(data.describe())                   # 描述数据
print(len(data))                         # 数据长度
#数据清洗
#发现缺失值
x=0
data["price"][(data["price"]==0)]=None    # 将价格为0的数据置为空值
for i in data.columns:
	for j in range(len(data)):
		if(data[i].isnull())[j]:
			data[i][j]="36"
			x+=1
print(x)  # 处理的个数
# 异常值处理
# 画散点图（横轴为价格，纵轴为评论数）
# 得到价格
data2=data.T
price=data2.values[2]
# 得到评论数
comt=data2.values[3]
pyl.subplot(2,2,1)
pyl.plot(price,comt,'o')

#评论数异常>200000，价格异常>2300
line=len(data.values)     # 行数
col=len(data.values[0])   # 列数
da=data.values
for i in range(0,line):
    for j in range(0,col):
        if(da[i][2]>2300):
            # print(da[i][j])
            da[i][j]=36  # 设置为中位数
        if(da[i][3]>200000):
            # print(da[i][j])
            da[i][j]=58
da2=da.T
price=da2[2]
comt=da2[3]

pyl.subplot(2,2,2)
pyl.plot(price,comt,'o')

# 分布分析
pricemax=da2[2].max()
pricemin=da2[2].min()
commentmax=da2[3].max()
commentmin=da2[3].min()
#极差：最大值-最小值
pricerg=pricemax-pricemin
commentrg=commentmax-commentmin
#组距：极差/组数
pricedst=pricerg/12
commentdst=commentrg/12

#画价格的直方图
pricesty=np.arange(pricemin,pricemax,pricedst)
pyl.subplot(2,2,3)
pyl.hist(da2[2],pricesty)

#画评论的直方图
commentsty=np.arange(commentmin,commentmax,commentdst)
pyl.subplot(2,2,4)
pyl.hist(da2[3],commentsty)
pyl.show()
'''

import numpy as np
a=np.array([[1,5,6],[9,4,3]])
b=np.array([[6,36,7],[2,3,39]])
c=np.concatenate((a,b))  #整合
print(c)