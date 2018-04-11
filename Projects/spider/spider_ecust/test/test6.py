# !/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

s1 = '/wEPDwUKMTM1ODI5MTYyMA9kFgICAw9kFgICAQ9kFg4CAQ8PFgIeBFRleHQFFeS6keiuoeeul+W6lOeUqOeOsOeKtmRkAgMPDxYCHwAFJ+S6keiuoeeul+eahOW6lOeUqOeOsOeKtuS7i+e7jeS4juWIhuaekGRkAgUPDxYCHwAFAjEzZGQCBw8PFgIfAAUJMuWIhjI056eSZGQCEQ8PFgIfAAUG5Li756uZZGQCEw9kFgQCAQ8PFgQfAAUH6ZWc5YOPMR4LTmF2aWdhdGVVcmwFJS9zdHVkZW50L3NjaGFwdGVyLmFzcHg/Y2hhcHRlcmlkPTI1NTNkZAIDDw8WBB8ABQfplZzlg48yHwEFNi9zdHVkZW50L3NjaGFwdGVyLmFzcHg/Y2hhcHRlcmlkPTI1NTMmYWRkPTEmbWlycm9ybm89MWRkAhcPFgIeA3NyYwU9aHR0cDovLzIyMi43My4zMy4yNTA6ODgvZmlsZXMvVmlkZW8vanNqeGtxeWpzanMwMy9jb250ZW50Lmh0bWRkiTKfrScRjGuAl3jBaxx9548jpwdSDpxiDhZb6E9ea84='
s2 = '8C48877A'
s3 = '4553'
s4 = '240550'

url = 'http://222.73.34.165:88/student/schapter.aspx?chapterid=4553&add=1'
cookies_dict = {'ASP.NET_SessionId': '0clwle1b5egoaznsofmutnji'}

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
           "Connection": "keep-alive",
           "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           # "Content-Length": '696',
           "Content-Type": "application/x-www-form-urlencoded",
           "Upgrade-Insecure-Requests": "1",
           'Origin': 'http://222.73.34.165:88',
           'Cache-Control': 'max-age=0',
           'Referer': url,
           'Host': '222.73.34.165:88'}

headers1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            'Referer': url,
            'Host': '222.73.34.165:88'}


# r1 = requests.get(url=url,
#                   headers=headers1,
#                   cookies=cookies_dict)

# soup = BeautifulSoup(r1.text, 'html.parser')
# s1 = soup.find(id="__VIEWSTATE").get('value')
# s2 = soup.find(id="__VIEWSTATEGENERATOR").get('value')
# s3 = soup.find(id="hchapterid").get('value')
# s4 = soup.find(id="huserid").get('value')

print(s1, s2, s3, s4)
r2 = requests.post(url=url,
                   headers=headers,
                   data={'__VIEWSTATE': s1,
                         '__VIEWSTATEGENERATOR': s2,
                         'Button2': '结束学习',
                         'hchapterid': s3,
                         'huserid': s4,
                         'hlearntime': '1000'},
                   cookies=cookies_dict)

print(r2.text)

