# !/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas
import requests
from bs4 import BeautifulSoup

r = requests.get('https://book.douban.com/subject/1084336/comments/').text

comments = []
soup = BeautifulSoup(r, 'lxml')
pattern = soup.find_all('p', 'comment-content')
for item in pattern:
    print(item.string)
    comments.append(item.string)

s = pandas.DataFrame(comments)
s.to_csv('comments.csv', encoding='utf-8')