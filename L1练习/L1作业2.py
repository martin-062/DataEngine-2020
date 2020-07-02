# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 21:54:47 2020

@author: MaJun4
"""


import pandas as pd
from pandas import Series, DataFrame
column = {'语文':[68,95,98,90,80],
          '数学':[65,76,86,88,90],
          '英语':[30,98,88,77,90]}
df1 = DataFrame(column,index=['张飞','关羽','刘备','典韦','许褚'])
print(df1)
print(df1.describe())

#直接增加总成绩列
'''
df1['总成绩'] = df1[u'语文'] + df1[u'英语'] + df1[u'数学']  
'''

def plus_column(df):
    df['总成绩'] = df[u'语文'] + df[u'数学'] + df[u'英语']
    return df
df1 = df1.apply(plus_column, axis=1)
df1 = df1.sort_values([u'总成绩'], ascending = False)
df1['名次'] = df1['总成绩'].rank(ascending = False)
df1['名次'] = df1['名次'].astype('int')
print(df1)
df1.to_excel('L1 practice-2.xlsx')
