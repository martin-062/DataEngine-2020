# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 22:13:36 2020

@author: Administrator
"""


import pandas as pd

# 数据加载
train = pd.read_csv('./train.csv')
# print(train.head())
# 转化为pandas日期格式
train['Datetime'] = pd.to_datetime(train.Datetime, format='%d-%m-%Y %H:%M')
train.index = train.Datetime
train.drop(['ID', 'Datetime'], axis=1, inplace=True)
#print(train.head())
# 按照天进行采样
daily_train = train.resample('D').sum()
#print(daily_train.head())
daily_train['ds'] = daily_train.index
daily_train['y'] = daily_train.Count
daily_train.drop('Count', axis=1, inplace=True)
#print(daily_train.head())

from fbprophet import Prophet
# 拟合prophet模型
model = Prophet(yearly_seasonality=True, seasonality_prior_scale=0.1) # 季节性组件的强度,值越小越抑制季节性波动。（默认10）
# 训练
model.fit(daily_train)
# 建立未来7个月（213天）数据框
future = model.make_future_dataframe(periods=213)
# 预测未来7个月走势
forecast = model.predict(future)
pd.options.display.max_columns=100
print(forecast.head())

# 画图输出
model.plot(forecast)
# 查看各个成分
model.plot_components(forecast)