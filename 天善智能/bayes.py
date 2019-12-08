# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/21 15:10
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : bayes.py
# Description :贝叶斯分类
# ----------------------------------
import numpy as np

class Bayes:

	# 初始化方法
	def __init__(self):
		self.length=-1          # 长度
		self.labelcount=dict()       # 标签
		self.vectorcount=dict()      # 向量

	# 训练方法
	def fit(self,dataSet,labels):
		if(len(dataSet)!=len(labels)):
			raise ValueError("您输入的测试数组与类别数组长度不一致")
		self.length=len(dataSet[0]) # 测试数据特征值的长度
		labelsnum=len(labels)       # 所有类别的数量
		norlabels=set(labels)       # 不重复类别的数量
		for item in norlabels:
			thislabel=item          # 当前类别
			self.labelcount[thislabel]=labels.count(thislabel)/labelsnum   # 求的当前类别栈类别总数的比例
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
		# 计算当前testdata分别为各个类别的概率
		lbDict = dict()
		for thislb in labelsSet:
			p = 1
			alllabel = self.labelcount[thislb]
			allvector = self.vectorcount[thislb]
			vnum = len(allvector)  # 当前向量的个数
			allvector = np.array(allvector).T
			for index in range(0, len(TestData)):
				vector = list(allvector[index])
				p *= vector.count(TestData[index]) / vnum
			lbDict[thislb] = p * alllabel
		thislabel = sorted(lbDict, key=lambda x: lbDict[x], reverse=True)[0]# 大到小排序
		return thislabel
