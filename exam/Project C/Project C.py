# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:40:07 2020

@author: Administrator
"""


import pandas as pd
import numpy as np

# 数据加载
data = pd.read_csv('CarPrice_Assignment.csv', encoding='gbk')
# 取表中除了ID和NAME列所有字段生成新的表格，用于聚类分析
train_x = data.drop(['car_ID', 'CarName'], axis=1)
# 数据探索
#pd.options.display.max_columns=100
#print(train_x.head())

# 数据预处理，将类别数据数字化
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
# 识别数据是否为object，是则进行数字化
#print(train_x.dtypes)
for index, row in train_x.iteritems():
    if train_x[index].dtypes == object:
        train_x[index] = le.fit_transform(train_x[index])
print(train_x.head())

# 对数据进行规范化[0-1]
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)
#pd.DataFrame(train_x).to_csv('111.csv', encoding='gbk')

# K-Means 手肘法：统计不同K取值的误差平方和sse,识别出最优K=14，兼顾误差与类别数量
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
sse = []
for k in range(2,50):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(train_x)
    sse.append(kmeans.inertia_)
#print(sse)
x = range(2,50)
plt.subplot(2,1,1)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')

# 评估聚类结果的轮廓系数
from sklearn import metrics
ssc = []
for k in range(2,50):
    labels = KMeans(n_clusters=k).fit(train_x).labels_
    ssc_ = metrics.silhouette_score(train_x, labels)
    ssc.append(ssc_)
#print(ssc)
x = range(2,50)
plt.subplot(2,1,2)
plt.xlabel('K')
plt.ylabel('SSC')
plt.plot(x, ssc, 'o-')
plt.show()

# 结合手肘法和轮廓系数图示，选择最优K，输入
K = input('请根据图示输入最优K： ')
# 使用KMeans聚类，训练创建模型
kmeans = KMeans(n_clusters=int(K))
kmeans.fit(train_x)
# 预测，给每一行打标签
predict_y = kmeans.predict(train_x)
#print(predict_y)
# 合并聚类结果，插入到原数据中
result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
result.rename({0:u'聚类结果'}, axis=1, inplace=True)
#print(result)
#result.to_csv('cluster_result.csv', encoding='gbk')

# 找出带有vw及*wagen的行
vw_name_list = ['vokswagen rabbit', 'volkswagen 1131 deluxe sedan', 'volkswagen model 111', 'volkswagen type 3',
           'volkswagen 411 (sw)','volkswagen super beetle', 'volkswagen dasher', 'vw dasher', 'vw rabbit',
           'volkswagen rabbit', 'volkswagen rabbit custom', 'volkswagen dasher']
vw_result = result[result['CarName'].isin(vw_name_list)]
print(vw_result)
# 取出vw产品对应的聚类结果作为列表，用以筛选所有产品类别，找到竞品
vw_cluster_list = vw_result[u'聚类结果'].values.tolist()
#print(vw_cluster_list)
competitor_result = result[result[u'聚类结果'].isin(vw_cluster_list)]
competitor_result.to_csv('competitor_result.csv', encoding='gbk')
