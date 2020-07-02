# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:50:51 2020

@author: Administrator
"""


import pandas as pd
print('STEP1:数据加载')
df1 = pd.read_csv('car_complain.csv')
#发现表格中一汽大众有两种写法，统一
df1['brand'].replace('一汽-大众', '一汽大众', inplace = True)
print(df1,'\n'*2)

print('STEP2:数据预处理——缺陷分类')
#Series.str.get_dummies()拆分series中以“|”分隔的字符串，然后返回一个df
problem_lable = df1.problem.str.get_dummies(',')
#print(problem_lable)
df1 = df1.join(problem_lable)
#df1.to_excel('car_complain.xlsx')
#请教老师你提供的drop函数中 ,1，是axis=1的意思吗，为何能够简写,还是axis都可以简写成0\1
df1 = df1.drop(['problem','datetime','status','desc'],1)
print(df1,'\n\n')

print('STEP3:对数据进行探索，品牌投诉总数、车型投诉总数、哪个品牌的平均车型投诉最多','\n')
df2 = df1.groupby(['brand'])['id'].agg(['count'])
df2 = df2.sort_values('count', ascending= False)
print('品牌投诉总数 ', df2, '\n')
df2.to_csv('品牌投诉总数.csv')
df3 = df1.groupby(['car_model'])['id'].agg(['count']).sort_values('count', ascending = False)
print('车型投诉总数 ', df3, '\n')
df3.to_csv('车型投诉总数.csv')
#先用品牌和车型聚合数数，然后根据品牌在聚合求品牌的平均车型投诉数
df4 = df1.groupby(['brand','car_model'])['id'].agg(['count']).groupby(['brand']).mean().sort_values('count', ascending= False)
print('品牌平均车型投诉总数', df4)
df4.to_csv('品牌平均车型投诉总数.csv')
