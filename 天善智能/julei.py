# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/22 10:01
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : julei.py
# Description : 聚类实战
# ----------------------------------
'''
主要内容：
	1、决策树
	2、聚类概述
	3、聚类常见算法
	4、聚类三法
	5、K-means算法概述
	6、K-means算法实战
'''

# 决策树
import pandas as pd
fname="data/lesson.csv"
dataf=pd.read_csv(fname,encoding="gbk")
# print(dataf)
# 提取x,y数据
x=dataf.iloc[:,1:5].values
y=dataf.iloc[:,5].values
# print(x)
# print(y)
for i in range(0,len(x)):
	for j in range(0,len(x[i])):
		thisdata=x[i][j]
		if(thisdata=="是" or thisdata=="多" or thisdata=="高"):
			x[i][j]=int(1)
		else:
			x[i][j]=int(-1)
# print(x)
for i in range(0,len(y)):
	thisdata=y[i]
	if(thisdata=="高"):
		y[i]=1
	else:
		y[i]=-1

# 容易错的地方：直接dtc训练
# 正确的做法：转化格式，将x,y转化为数据框，再转化为数组并指定格式
xf=pd.DataFrame(x)
# print(xf)
yf=pd.DataFrame(y)
# print(yf)
x2=xf.values.astype(int)
y2=yf.values.astype(int)
# print(x2,y2)
# 建立决策树
from sklearn.tree import DecisionTreeClassifier as DTC
dtc=DTC(criterion="entropy") # 以信息熵的形式建立决策树
dtc.fit(x2,y2)

# 直接预测销量高低
import numpy as np
x3=np.array([[1,-1,-1,1],[1,1,1,1],[-1,1,-1,1]])
rst=dtc.predict(x3)
print(rst)

# 可视化决策树：决策树往左看是正能量，往右看是负能量
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
with open("data/dtc.dot","w") as file:
	export_graphviz(dtc,feature_names=["combat","num","promotion","datanum"],out_file=file)

#
