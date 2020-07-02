# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义函数：通过指定 URL获取内容，完成后返回一个soup文件
def get_page_content(request_url):
    #得到页面内容
    Headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html = requests.get(request_url, headers = Headers, timeout = 10)
    content = html.text
    #通过content创建BeautifulSoup对象, 解析成soup文件
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

# 定义函数：分析当前页面的投诉
def analysis(soup):
    #找到完整的投诉信息框
    temp = soup.find('div', class_='tslb_b')
    #创建一个数据框
    df = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
    #在完整的投诉信息框中找到每一行,返回一个tr标签的列表
    tr_list = temp.find_all('tr')   
    for tr in tr_list:
        #使用Series字典建立一个空集，用以存放投诉信息
        temp = {}
        #从每一行找到所有列,数据按照每个单元格分解，返回一个td标签的列表
        td_list = tr.find_all('td') 
        #print(td_list)
        #第一个tr没有td，其余都有8个td.  通过if循环判断是否第一列，否就进行分析
        if len(td_list) > 0:
            #解析各个字段的每个单元格内容，并且赋值给temp字典
            temp['id'], temp['brand'], temp['car_model'], temp['type'], temp['desc'], temp['problem'], temp['datetime'], temp['status'] = td_list[0].text, td_list[1].text, td_list[2].text, td_list[3].text, td_list[4].text, td_list[5].text, td_list[6].text, td_list[7].text
            #根据对应columns依次放到DataFrame中     
            df = df.append(temp, ignore_index=True) 
    return df

#df = analysis(soup)
#print(df)

#设定抓取页数
page_num = 20
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-0-0-0-0-0-'

#创建一个数据框
result = pd.DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])

#循环抓取20页
for i in range(page_num):
    request_url = base_url + str(i+1) + '.shtml'
    #根据函数获取不同页URL内容
    soup = get_page_content(request_url)
    #获取soup文件后对它进行解析
    df = analysis(soup)
    print(df)
    result = result.append(df)
result.to_csv('L2 practice.csv', index=False, encoding='gbk')