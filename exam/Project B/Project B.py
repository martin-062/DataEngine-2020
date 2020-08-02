# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:59:05 2020

@author: Administrator
"""


import pandas as pd
import numpy as np


# 导入数据，注意由于数据是rawdata，不将第一行作为head
data = pd.read_csv('订单表.csv', encoding='gbk')
#print(data.head())
# 只读取产品名称、客户ID做关联分析
new_data = pd.DataFrame(data, columns=['客户ID', '产品名称', '订单日期'])
#print(new_data.head())
new_data.sort_values(['客户ID', '产品名称'], inplace=True)
new_data.to_csv('关联订单表.csv', encoding='gbk', index=False)
#print(new_data.shape)  #shape为(60398,2)

# 使用efficient_apriori工具包
from efficient_apriori import apriori
# 得到一维数组字典orders_series，并且将客户ID作为key, 产品名称作为value
orders_series = new_data.set_index('客户ID')['产品名称']
#print(orders_series)
# 利用嵌套for循环将透视表的数据放到transactions列表里，因为efficient_apriori参数需要列表或元祖
transactions = []
temp_index = 0
for key, value in orders_series.items():
	if key != temp_index:
		temp_set = set()   #利定义一个临时空集合set，去重复订单
		temp_index = key
		temp_set.add(value)
		transactions.append(temp_set)
	else:
		temp_set.add(value)
#print(transactions)

# 挖掘频繁项集与关联规则，通过不断尝试最小支持度和置信度的值，来输出合理的频繁项集和关联规则
itemsets, rules = apriori(transactions, min_support=0.04, min_confidence=0.4)
print('efficient频繁项集：\n', itemsets)
print('efficient关联规则：\n', rules)
