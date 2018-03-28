# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.autohome.com.cn/all/')
r.encoding = 'gbk'
soup = BeautifulSoup(r.text, 'html.parser')
li_list = soup.find(id='auto-channel-lazyload-article').find_all(name='li')
for i in li_list:
    print('------------')
    h3 = i.find('h3')
    if not h3:
        continue
    intro = i.find('p').text
    url = i.find('a').get('href')
    img = i.find('img').get('src')

    print(h3.text)
    print(intro)
    print(url)
    print(img)

    img_url = 'http://%s' % str(img).split('//')[1]
    # print(img_url)
    res = requests.get(img_url)
    file_name = '/Users/pylarva/github/Python/Projects/spider/spider_wu/img/%s.jpg' % h3.text
    try:
        with open(file_name, 'wb') as f:
            f.write(res.content)
    except FileNotFoundError as e:
        continue

