# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# 定义函数：通过指定 URL获取内容，完成后返回一个soup文件
def get_page_content(request_url):
    #得到页面内容
    Headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers = Headers, timeout = 10)
    content = html.text
    #通过content创建BeautifulSoup对象, 解析成soup文件
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 定义函数：采集当前页面的车型报价
def analysis(soup):
    #找到完整的车型信息框
    temp = soup.find('div', class_='search-result-list')
    #创建一个数据框
    df = pd.DataFrame(columns=[u'名称', u'最低价', u'最高价', u'产品图片链接'])
    #在完整的车型信息框中分别找到车型名称、价格和图片链接列表
    model_list = temp.find_all('p', class_='cx-name text-hover')
    car_price_list = temp.find_all('p', class_='cx-price')
    picture_link_list = temp.find_all('img', class_='img')
    #print(model_list[0].text)
    #print(picture_link_list)
    
    for i in range(len(model_list)):
        temp = {}
        temp[u'名称'] = model_list[i].text
        #将价格区间分割成最低价格和最高价格
        price_list = car_price_list[i].text.split('-')
        price_array = np.array(price_list)
        #print(price_array.shape)
        #部分车价无区间信息，使用同一价格；暂无车价信息使用暂无
        if price_array.shape ==(2,):
            temp[u'最低价'] = price_array[0] + '万'
            temp[u'最高价'] = price_array[1]
        else:
            temp[u'最低价'] = price_array[0]
            temp[u'最高价'] = price_array[0]
        temp[u'产品图片链接'] = 'http:' + picture_link_list[i].get('src')
        df = df.append(temp, ignore_index=True)
        
    return df

#df = analysis(soup)
#print(df)

#设定抓取页数
page_num = 3
base_url = 'http://car.bitauto.com/xuanchegongju/?mid=8'

#创建一个数据框
result = pd.DataFrame(columns=[u'名称', u'最低价', u'最高价', u'产品图片链接'])

#循环抓取3页
for i in range(page_num):
    if i == 0:
        request_url = base_url
    else:
        request_url = base_url + '&page=' + str(i+1)
    #根据函数获取不同页URL内容
    soup = get_page_content(request_url)
    #获取soup文件后对它进行解析
    df = analysis(soup)
    #print(df)
    result = result.append(df)
print(result)
result.to_csv('Project A.csv', index=False, encoding='gbk')