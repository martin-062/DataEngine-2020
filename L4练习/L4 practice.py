# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 21:59:05 2020

@author: Administrator
"""


import pandas as pd
import numpy as np
from efficient_apriori import apriori

# 导入数据，注意由于数据是rawdata，不将第一行作为head
data = pd.read_csv('Market_Basket_Optimisation.csv', header=None)
# print(data.shape)    shape为(7501,20)
# data.to_csv('data.csv')

# 利用嵌套for循环将data透视表的数据放到transactions列表里，因为efficient_apriori参数需要列表或元祖
transactions = []
for i in range(0,data.shape[0]):
    temp= []
    for j in range(0,data.shape[1]):
        # print(data.values[i,j])，发现内部会有空值nan
        if str(data.values[i, j]) !='nan':
            temp.append(data.values[i,j])
    transactions.append(temp)
# print(transactions[0:10])

# 第一种简单挖掘apriori算法
# 挖掘频繁项集与关联规则，通过不断尝试最小支持度和置信度的值，来输出合理的频繁项集和关联规则
itemsets, rules = apriori(transactions, min_support=0.05, min_confidence=0.2)
print('efficient频繁项集：\n', itemsets)
print('efficient关联规则：\n', rules)


# 第二种mlxtend apriori算法
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
# 先对数据进行独热编码，因为mlxtend apriori参数需要进行独热编码后的df
temp2 = TransactionEncoder()
# 进行one-hot编码
temp2_hot_encoded = temp2.fit(transactions).transform(transactions)
# print(temp2_hot_encoded)
df = pd.DataFrame(temp2_hot_encoded, columns=temp2.columns_)
#print(df)

# 挖掘频繁项集,通过排序发现，min_lift=1筛选出6个关联规则，比较合理；对应调整support=0.05
frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False, ignore_index=True)
print('-'*20, 'mlxtend频繁项集', '-'*20)
print(frequent_itemsets)
# 根据频繁项集计算关联规则
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)
rules = rules.sort_values(by='lift', ascending=False, ignore_index=True)
print('-'*20, 'mlxtend关联规则', '-'*20)
print(rules)

