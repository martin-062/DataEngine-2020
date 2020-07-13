# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 21:40:39 2020

@author: Administrator
"""


# 词云展示
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from lxml import etree
from nltk.tokenize import word_tokenize

# 生成词云
def create_word_cloud(f):
	print('根据词频，开始生成词云!')
	cut_text = word_tokenize(f)
	#print(cut_text)
	cut_text = " ".join(cut_text)
	wc = WordCloud(
		max_words=100,
		width=2000,
		height=1200,
    )
	wordcloud = wc.generate(cut_text)
	# 写词云图片
	wordcloud.to_file("wordcloud.jpg")
	# 显示词云文件
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.show()

# 数据加载
data = pd.read_csv('./Market_Basket_Optimisation.csv', header=None)
# 清除表内所有空，得到transactions列表
transactions = []
for i in range(0,data.shape[0]):
    temp = []
    for j in range(0,data.shape[1]):
        if str(data.values[i, j]) !='nan':
            temp.append(data.values[i, j])
    transactions.append(temp)

# 生成词云
all_word = ' '.join('%s' %item for item in transactions)  #join将序列中的元素以指定的字符拼接接生成一个新的字符串
#print(all_word)
create_word_cloud(all_word)