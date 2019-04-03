#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# __author__ = 'Frank'
import csv
import time
from lxml.html import etree
from selenium import webdriver
from efficient_apriori import apriori

# 定义导演
director = '张艺谋'


# 定义加载数据函数
def load_data(director_name):
    file = './' + director_name + '.csv'
    url = 'https://movie.douban.com/subject_search?search_text={}&cat=1002&start='.format(director_name)
    driver = webdriver.Chrome()
    movie_xpath = "/html/body/div[@id='wrapper']/div[@id='root']//div[1]//div[@class='item-root']/div[@class='detail']/div[@class='title']/a[@class='title-text']"
    actor_xpath = "/html/body/div[@id='wrapper']/div[@id='root']//div[1]//div[@class='item-root']/div[@class='detail']/div[@class='meta abstract_2']"
    with open(file, encoding = 'utf-8-sig', newline = '', mode = 'w') as f:
        fwriter = csv.writer(f)
        for i in range(0, 10000, 15):
            request_url = url + str(i)
            driver.get(request_url)
            time.sleep(1)
            html = etree.HTML(driver.page_source)
            movie_list = html.xpath(movie_xpath)
            actor_list = html.xpath(actor_xpath)
            if len(movie_list) > 15:
                movie_list = movie_list[1:]
                actor_list = actor_list[1:]
            for movie, actor in zip(movie_list, actor_list):
                if actor.text is None:
                    continue
                print(actor.text)
                names = actor.text.split('/')
                if names[0].strip() == director:
                    names[0] = movie.text
                    fwriter.writerow(names)
                    print('OK')
            if len(movie_list) < 1:
                break


# 调用函数
load_data(director)
# 加载数据
with open('张艺谋.csv', mode = 'r', encoding = 'utf-8-sig', newline = '') as f:
    freader = csv.reader(f)
    data = []
    for names in freader:
        name_new = list(map(str.strip, names[1:]))
        data.append(name_new)
# 挖掘频繁项集和关联规则
itemset, rules = apriori(data, min_support = 0.1, min_confidence = 0.8)
print(itemset)
print(rules)
