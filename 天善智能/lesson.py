# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/25 16:28
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : lesson.py
# Description :使用Apriori算法实现课程关联分析
# ----------------------------------
'''
使用Apriori算法实现课程关联分析
'''
#计算学院购买课程的关联性
from apriori import *
import pandas as pd

# 导入数据
filename="data/lesson_buy.xls"
dataframe=pd.read_excel(filename,header=None)
# print(dataframe)

# 转化一下数据
dataframe=pd.read_excel(filename,header=None)
#转化一下数据
change=lambda x:pd.Series(1,index=x[pd.notnull(x)])
mapok=map(change,dataframe.values)
data=pd.DataFrame(list(mapok)).fillna(0)
print(data)

#临界支持度、置信度设置
spt=0.2
cfd=0.5

#使用apriori算法计算关联结果
find_rule(data,spt,cfd,"-->")