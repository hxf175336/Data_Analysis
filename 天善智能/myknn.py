# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/19 20:31
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : myknn.py
# Description : KNN算法的实现
# ----------------------------------
from numpy import *
import operator
from os import  listdir
def knn(k,testdata,traindata,labels):
	traindatasize=traindata.shape[0]  # 数据行数，即数据个数
	# 从列方向扩展
	# tile(a,(size,1))
	dif=tile(testdata,(traindatasize,1))-traindata  #扩展为相同维度后计算差值
	sqdif=dif**2  # 平方
	sumsqdif=sqdif.sum(axis=1) # 各列平方和
	distance=sumsqdif**0.5     # 计算距离
	sortdistance=distance.argsort() #距离排序，得到序号
	count={}
	for i in range(0,k):
		vote=labels[sortdistance[i]]    # 投票结果，类别
		count[vote]=count.get(vote,0)+1 # 统计类别出现次数
	sortcount=sorted(count.items(),key=operator.itemgetter(1),reverse=True)
	return sortcount[0][0]

#将图片处理为文本
#先将所有图片转为固定宽高，比如32*32，然后再转为文本
#pillow
from PIL import Image
im=Image.open("C:/Users/xuefa/Pictures/Camera Roll/111.jpg") # 打开图片
fh=open("C:/Users/xuefa/Pictures/Camera Roll/111.txt","a") # 打开文件
# im.save("C:/Users/xuefa/Pictures/Camera Roll/tt.bmp")       # 保存为其他格式
width=im.size[0]             # 获取图片的长和宽
height=im.size[1]
# k=im.getpixel((1,9))         # 获取像素，RGB
for i in range(0,width):
	for j in range(0,height):
		cl=im.getpixel((i,j))  # 获取RGB
		clall=cl[0]+cl[1]+cl[2]
		if(clall==0):
			# 黑色
			fh.write("1")
		else:
			fh.write("0")
	fh.write("\n")
fh.close()


# 加载数据
def datatoarray(fname):
	arr=[]
	fh=open(fname)
	for i in range(0,32):
		thisline=fh.readline()
		for j in range(0,32):
			arr.append(int(thisline[j]))
	return arr
arr1=datatoarray("data/testandtraindata/traindata/0_4.txt")
# print(arr1)

# 建立一个函数取文件名前缀
def seplabel(fname):
	filestr=fname.split(".")[0]
	label=int(filestr.split("-")[0])
	return label

# 建立训练数据集
def traindata():
	labels=[]
	trainfile=listdir("data/testandtraindata/traindata")#查看目录下的文件
	num=len(trainfile)
	# 长度1024(列)，每一行存储一个文件
	# 用一个数组存储所有训练数据，行：文件总数，列：1024
	trainarr=zeros((num,1024))
	for i in range(0,num):
		thisfname=trainfile[i]
		thislabel=seplabel(thisfname)
		labels.append(thislabel)
		trainarr[i,:]=datatoarray("data/testandtraindata/traindata/"+thisfname)  #读取当前所有数据
	return trainarr,labels

# 用测试数据调用KNN算法去测试，看是否能够准确识别
def datatest():
    trainarr,labels=traindata()
    testlist=listdir("data/testandtraindata/testdata/")
    tnum=len(testlist)
    for i in range(0,tnum):
        thistestfile=testlist[i]
        testarr=datatoarray("data/testandtraindata/testdata/"+thistestfile)
        rknn=knn(3,testarr,trainarr,labels)
        print(rknn)
datatest()
# #抽某一个测试文件出来进行试验
# trainarr,labels=traindata()
# thistestfile="data/testandtraindata/traindata/8_76.txt"
# testarr=datatoarray("data/testandtraindata/testdata/"+thistestfile)
# rknn=knn(3,testarr,trainarr,labels)
# print(rknn)