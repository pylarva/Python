# !/usr/bin/env python
# -*- coding:utf-8 -*-

# 模拟登陆GitHub

import requests
from bs4 import BeautifulSoup

# 获取token
response = requests.get('https://github.com/login')
soup = BeautifulSoup(response.text, 'html.parser')
r1_token = soup.find(name='input', attrs={'name': 'authenticity_token'}).get('value')
r1_cookies_dict = response.cookies.get_dict()
# print(r1_token)

# 用户名密码访问 post
"""
commit: Sign in
utf8: ✓
authenticity_token: PH1VBp6IknyiYM6qFD+XlkTQ76GWshOv0Y1cTh++Dkfj3PVwSZKkShljrtw9yMaElZ9eFqB6Ufhd+haanDu2AA==
login: ssdf
password: sdf
"""
r2 = requests.post('https://github.com/session',
                   data={'commit': 'Sign in',
                         'utf-8': '✓',
                         'authenticity_token': r1_token,
                         'login': 'pylarva',
                         'password': '1'},
                   cookies=r1_cookies_dict)

r2_cookies_dict = r2.cookies.get_dict()

cookies_dict = {}
cookies_dict.update(r1_cookies_dict)
cookies_dict.update(r2_cookies_dict)

# 正式登陆 看是否成功返回页面
r3 = requests.get('https://github.com/settings/emails', cookies=cookies_dict)
print(r3.text)