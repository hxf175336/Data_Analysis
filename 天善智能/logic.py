# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/21 16:03
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : logic.py
# Description : 逻辑回归
# ----------------------------------

import pandas as pda
fname="data/luqu.csv"
dataf=pda.read_csv(fname)
x=dataf.iloc[:,1:4].as_matrix()  # 取出，转化为数组
y=dataf.iloc[:,0:1].as_matrix()  # 取出，转化为数组
# print(x)
# print(y)

from sklearn.linear_model import LogisticRegression as LR
# from sklearn.linear_model import RandomizedLogisticRegression as RLR
from stability_selection.randomized_lasso import RandomizedLogisticRegression as RLR
# from sklearn.linear_model import RandomizedLogisticRegression as RLR
r1=RLR()
r1.fit(x,y)
r1.get_support() # 特征筛选
#print(dataf.columns[r1.get_support()])
t=dataf[dataf.columns[r1.get_support()]].as_matrix()
r2=LR()
r2.fit(t,y)
print("训练结束")
print("模型正确率为:"+str(r2.score(x,y)))