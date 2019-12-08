# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/23 15:58
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : bp.py
# Description : BP人工神经网络的实现
# ----------------------------------
'''
BP人工神经网络的实现：
	1、读取数据
	2、导入模块 keras.models Sequential / keras.layers.core Dense Activation
	3、Sequential 建立模型
	4、Dense 建立层
	5、Activation 设定激活函数
	6、compile 模型编译
	7、fit 训练（学习）
	8、验证 （测试、分类预测）
'''
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# 使用人工神经网络预测课程销量
# 数据的读取与整理
import pandas as pda
fname = "data/lesson.csv"
dataf = pda.read_csv(fname, encoding="gbk")
x = dataf.iloc[:, 1:5].values
y = dataf.iloc[:, 5].values
for i in range(0, len(x)):
	for j in range(0, len(x[i])):
		thisdata = x[i][j]
		if (thisdata == "是" or thisdata == "多" or thisdata == "高"):
			x[i][j] = int(1)
		else:
			x[i][j] = -1
for i in range(0, len(y)):
	thisdata = y[i]
	if (thisdata == "高"):
		y[i] = 1
	else:
		y[i] = -1
# 容易错的地方:直接dtc训练
# 正确的做法：转化好格式，将x，y转化为数据框，然后再转化为数组并指定格式
xf = pda.DataFrame(x)
yf = pda.DataFrame(y)
x2 = xf.values.astype(int)
y2 = yf.values.astype(int)
# print(x2)
# 使用人工神经网络模型
from keras.models import Sequential
from keras.layers.core import Dense,Activation
model=Sequential()

# 输入层
model.add(Dense(10,input_dim=len(x2[0])))
model.add(Activation("relu"))
# 输出层
model.add(Dense(1,input_dim=1))
model.add(Activation("sigmoid"))
# 模型的编译
model.compile(loss="binary_crossentropy",optimizer="adam") # 损失函数、求解方法、分类模型
# 训练
model.fit(x2,y2,nb_epoch=1000,batch_size=100) # 学习次数、批处理参数
# 预测分类
rst=model.predict_classes(x).reshape(len(x))
x=0
for i in range(0,len(x2)):
    if(rst[i]!=y[i]):
        x+=1
print("准确率",str(1-x/len(x2)))
import numpy as npy
x3=npy.array([[1,-1,-1,1],[1,1,1,1],[-1,1,-1,1]])
rst=model.predict_classes(x3).reshape(len(x3))
print("其中第一门课的预测结果为:"+str(rst[0]))