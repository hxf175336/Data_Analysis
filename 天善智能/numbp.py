# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/24 10:45
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : numbp.py
# Description : 使用人工神经网络实现简单手写体数字的识别
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
from numpy import *
import operator
from os import listdir
import numpy as npy
import numpy
import pandas as pd

#加载数据
def datatoarray(fname):
    arr=[]
    fh=open(fname)
    for i in range(0,32):
        thisline=fh.readline()
        for j in range(0,32):
            arr.append(int(thisline[j]))
    return arr

#建立一个函数取文件名前缀
def seplabel(fname):
    filestr=fname.split(".")[0]
    label=int(filestr.split("_")[0])
    return label

#建立训练数据
def traindata():
    labels=[]
    trainfile=listdir("data/testandtraindata/traindata/")
    num=len(trainfile)
    #长度1024（列），每一行存储一个文件
    #用一个数组存储所有训练数据，行：文件总数，列：1024
    trainarr=zeros((num,1024))
    for i in range(0,num):
        thisfname=trainfile[i]
        thislabel=seplabel(thisfname)
        labels.append(thislabel)
        trainarr[i,:]=datatoarray("data/testandtraindata/traindata/"+thisfname)
    return trainarr,labels

trainarr,labels=traindata()
# print(trainarr,labels)
xf=pd.DataFrame(trainarr)
yf=pd.DataFrame(labels)
# print(xf,yf)
tx2=xf.values.astype(int)
ty2=yf.values.astype(int)
# print(tx2)
# print(ty2)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# 使用人工神经网络模型
from keras.models import Sequential
from keras.layers.core import Dense,Activation
model=Sequential()

# 输入层
model.add(Dense(10,input_dim=1024))
model.add(Activation("relu"))
# 输出层
model.add(Dense(1,input_dim=1))
model.add(Activation("sigmoid"))
# 模型的编译
model.compile(loss="mean_squared_error",optimizer="adam") # 损失函数、求解方法、分类模型
# 训练
model.fit(tx2,ty2,nb_epoch=10000,batch_size=1000) # 学习次数、批处理参数
# 预测分类
rst=model.predict_classes(x).reshape(len(x))
# print(rst)
x=0
for i in range(0,len(x2)):
    if(rst[i]!=y[i]):
        x+=1
print(1-x/len(x2))
import numpy as npy
x3=npy.array([[1,-1,-1,1],[1,1,1,1],[-1,1,-1,1]])
rst=model.predict_classes(tx2).reshape(len(tx2))
print(rst)
