# -*- coding: utf-8 -*-
# --------------------------------------
# @Time    : 2019/10/14 15:45
# @Author  : hxf
# @Email   : 1870212598@qq.com
# @File    : shuju3_input.py
# Description :数据导入
# ----------------------------------
'''
数据导入
	导入csv文件
	导入excel文件
	导入MySQLS数据库中的数据
	导入html数据
	导入文本数据 read_table
'''
import pandas as pda
print('----------------------------------读取csv文件------------------------------------------------')
i=pda.read_csv('data/hexun.csv')
print('----------------------------------------------------------------------------------')
print(i)
print(i.describe())
print('----------------------------------------------------------------------------------')
print(i.sort_values(by="hits"))

# print('----------------------------------读取excel文件------------------------------------------------')
# j=pda.read_excel('data/hexun.xls')
# print('----------------------------------------------------------------------------------')
# print(j)
# print(j.describe())
# print('----------------------------------------------------------------------------------')
# print(j.sort_values(by="hits"))
#
# print('----------------------------------读取html数据------------------------------------------------')
# k=pda.read_html('data/abc.html')
# print(k)
# l=pda.read_html('https://book.douban.com/')
# print(l)
#
# print('----------------------------------读取.txt文件------------------------------------------------')
# m=pda.read_table('data/abc.txt')
# print(m)

'''
print('----------------------------------读取sql文件------------------------------------------------')
import pymysql
conn=pymysql.connect(host="127.0.0.1",user="root",passwd="123456",db="hexun")
sql="select * from myhexun"
n=pda.read_sql(sql,conn)
print(n)
'''