# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/23 13:25
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : bayes_use.py
# Description : 贝叶斯算法的应用
# ----------------------------------

#贝叶斯算法的应用
from numpy import *
import operator
from os import listdir
import numpy as npy
import numpy

class Bayes:

	# 初始化方法
    def __init__(self):
        self.length=-1
        self.labelcount=dict()
        self.vectorcount=dict()

	# 训练方法
    def fit(self,dataSet:list,labels:list):
        if(len(dataSet)!=len(labels)):
            raise ValueError("您输入的测试数组跟类别数组长度不一致")
        self.length=len(dataSet[0])  # 测试数据特征值的长度
        labelsnum=len(labels)        # 类别所有的数量
        norlabels=set(labels)        # 不重复类别的数量
        for item in norlabels:
            thislabel=item
            self.labelcount[thislabel]=labels.count(thislabel)/labelsnum # 求的当前类别占类别总数的比例
        for vector,label in zip(dataSet,labels):
            if(label not in self.vectorcount):
                self.vectorcount[label]=[]
            self.vectorcount[label].append(vector)
        print("训练结束")
        return self

	# 测试方法
    def btest(self,TestData,labelsSet):
        if(self.length==-1):
            raise ValueError("您还没有进行训练，请先训练")
        #计算testdata分别为各个类别的概率
        lbDict=dict()
        for thislb in labelsSet:
            p=1
            alllabel=self.labelcount[thislb]
            allvector=self.vectorcount[thislb]
            vnum=len(allvector)
            allvector=numpy.array(allvector).T
            for index in range(0,len(TestData)):
                vector=list(allvector[index])
                p*=vector.count(TestData[index])/vnum
            lbDict[thislb]=p*alllabel
        thislabel=sorted(lbDict,key=lambda x:lbDict[x],reverse=True)[0]
        return thislabel

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

bys=Bayes()
train_data,labels=traindata()
# print(train_data,labels)
bys.fit(train_data,labels)
# 测试数据
thisdata=datatoarray("data/testandtraindata/testdata/8_90.txt")
labelsall=[0,1,2,3,4,5,6,7,8,9]
# 识别单个手写体数字
'''
result=bys.btest(thisdata,labelsall)
print(result)
'''
# 识别多个手写体数字（批量测试）
testfileall=listdir("data/testandtraindata/testdata")
num=len(testfileall)
count = 0
for i in range(0,num):
	thisfilename=testfileall[i]
	# print(thisfilename)
	thislabel=seplabel(thisfilename)
	# print(thisfilename)
	# print(thislabel)
	thisdataarr=datatoarray("data/testandtraindata/testdata/"+thisfilename)
	label=bys.btest(thisdataarr,labelsall)
	print("该数字是："+str(thislabel)+",识别出来的数字是"+str(label))
	if(label!=thislabel):
		count+=1
print("预测错误的次数："+str(count))
print("错误率："+str(count/num))

'''
预测错误的次数：116
错误率：0.1226215644820296
'''


