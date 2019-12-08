# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/14 16:52
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : shuju1_mpl.py
# Description :
# ----------------------------------
'''
matplotlib.pyplot模块
	1、折线图和散点图plot  plot(x轴数据，y轴数据，展现形式)，参数是可以叠加的
		颜色参数：
			c-cyan--青色
			r-red--红色
			m-magente--品红
			g-green--绿色
			b-blue--蓝色
			y-yellow--黄色
			k-black--黑色
			w-white--白色
		线条样式：
			-  直线
			-- 虚线
			-. -.式
			:  细小虚线
		点的样式：
			s--方形
			h--六角形
			H--六角形
			*--星形
			+--加号
			x--x形
			d--菱形
			D--菱形
			p--五角星
	2、直方图hist
		随机数的生成
		直方图绘制 hist(data,sty,histtype)  # 数据 形式 轮廓参数
	3、子图绘图
		subplot(2,2,1)
	4、可视化分析案例
		读取和讯博客的数据并可视化分析


'''
'''
import matplotlib.pyplot as pyl
import numpy as np

# 1、折线图和散点图plot
x=[1,2,3,4,8]
y=[5,7,2,1,5]
'''

'''
pyl.plot(x,y)          # 折线图
pyl.show()
pyl.plot(x,y,'o')      # 散点图，会叠加
pyl.show()

pyl.plot(x,y,'oc')     # 青色的散点图
pyl.show()

pyl.plot(x,y,'-')      # 直线
pyl.show()

pyl.plot(x,y,'--')       # 虚线
pyl.show()

pyl.plot(x,y,'-.')       # 虚线
pyl.show()

pyl.plot(x,y,':')       # 细小虚线
pyl.show()

pyl.plot(x,y,'*')       # 星形
pyl.show()

pyl.plot(x,y,'d')       # 菱形
pyl.show()

pyl.plot(x,y,'h')       # 六角形
pyl.show()
'''

'''
pyl.plot(x,y)
x2=[1,3,6,8,10,12,19]
y2=[1,6,9,10,19,23,35]
pyl.plot(x2,y2)

pyl.title("show")         # 添加标题
pyl.xlabel("ages")        # 添加x轴标题
pyl.ylabel("temp")        # 添加y轴标题
pyl.xlim(0,20)            # 设置x轴范围
pyl.ylim(0,35)            # 设置y轴范围
pyl.show()
'''

'''
# 2、直方图hist
# 随机数的生成
import numpy as np
data=np.random.random_integers(1,20,10) #(最小值，最大值，个数) 生成随机整数
# print(data)
data2=np.random.normal(5.0,2.0,10) # (均值,西格玛,个数) 生成正态分布的随机数
# print(data2)

data3=np.random.normal(10.0,1.0,10000)
# pyl.hist(data3)
# pyl.show()

data4=np.random.random_integers(1,25,1000)
# print(data4)
# pyl.hist(data4)
sty=np.arange(1,30,2)
# pyl.hist(data4,sty)
# pyl.hist(data4,sty,histtype='stepfilled')
# pyl.hist(data4,histtype='stepfilled')
# pyl.show()
# 更多随机数生成更多知识参考http://www.mamicode.com/info-detail-507676.html

#3、柱状图
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

num_list = [1.5, 0.6, 7.8, 6]
plt.bar(range(len(num_list)), num_list)
plt.show()

# 4、子图绘图
pyl.subplot(2,2,1)
x1=[1,2,3,4,5]
y1=[5,3,5,23,5]
pyl.plot(x1,y1)

pyl.subplot(2,2,2)
x2=[5,2,3,8,6]
y2=[7,9,12,12,3]
pyl.plot(x2,y2)

pyl.subplot(2,1,2)
x3=[5,6,7,10,19,20,29]
y3=[6,2,4,21,5,1,5]
pyl.plot(x3,y3)
pyl.show()

'''
'''
5.可视化分析案例
	读取和讯博客的数据并可视化分析
'''
# 读取和讯博客的数据并可视化分析
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv('data/myhexun.csv')
# print(data.shape) # 查看数据结构
# print(data.values)  # 查看 values[第几行][第几列]
# print(data.values[0])
# print(data.values[1][1])

# 转置
data2=data.T
y1=data2.values[3] # 获取阅读数
x1=data2.values[4] # 获取评论数
# plt.plot(x1,y1)
# plt.show()
x2=data2.values[0] # 取id
# plt.plot(x2,y1)
# plt.show()
plt.plot(x2,x1)
plt.show()