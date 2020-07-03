# 使用KMeans进行聚类
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np

# 数据加载
#data = pd.read_csv('Mall_Customers.csv', encoding='gbk')
data = pd.read_csv('car_data.csv', encoding='gbk')
# 取其中四个字段数据重新生成一个表格
train_x = data[['人均GDP','城镇人口比重','交通工具消费价格指数','百户拥有汽车量']]

# LabelEncoder，将性别字段改成数字male=1，female=0
#from sklearn.preprocessing import LabelEncoder
#le = LabelEncoder()
#train_x['Gender'] = le.fit_transform(train_x['Gender'])
print(train_x)

# train_x四列分别做数据规范化,规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
# 用DataFrame将train_x生成的矩阵改成数据表
#pd.DataFrame(train_x).to_csv('temp.csv', index=False)
#print(train_x)

'''
# K-Means 手肘法：统计不同K取值的误差平方和,从图表中选择后续聚类合适的K值
import matplotlib.pyplot as plt
sse = []
for k in range(1, 11):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 11)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
plt.show()
'''

# 使用KMeans聚类
kmeans = KMeans(n_clusters=3)
# 训练
kmeans.fit(train_x)
# 预测
predict_y = kmeans.predict(train_x)
print(predict_y)

# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
print(result)
# 将结果导出到CSV文件中
result.to_csv('L3 practice.csv',index=False,encoding='gbk')

'''
### 使用层次聚类
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import KMeans, AgglomerativeClustering
import matplotlib.pyplot as plt
model = AgglomerativeClustering(linkage='ward', n_clusters=3)
y = model.fit_predict(train_x)
print(y)

linkage_matrix = ward(train_x)
dendrogram(linkage_matrix)
plt.show()
'''