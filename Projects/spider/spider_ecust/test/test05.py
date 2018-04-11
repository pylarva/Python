# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

# s1 = '/wEPDwUKMTYwMjE5Mzg2Ng9kFgJmD2QWFAIDDw8WAh4EVGV4dAUJ6buO5om/5YW1ZGQCBQ9kFgJmD2QWAmYPDxYCHwAFAzY0MGRkAgsPFgIeB1Zpc2libGVoZAINDxYCHwFoZAIPDxYCHwFoZAIRDxYCHwFoZAIVDxYCHwFoZAIXDxYCHwFoZAIZDxYCHwFoFgICAQ8WAh4LXyFJdGVtQ291bnQCBBYIZg9kFgRmDxUBATFkAgEPDxYCHgtOYXZpZ2F0ZVVybAUhc3VwZXJ2aXNlL3NtYW5jb3Vyc2UuYXNweD90eXBlPTM5FgIeB29uY2xpY2sFHXNob3dfdGl0bGUoIuS4u+S/ruexu+ivvueoiyIpFgJmDw8WAh8ABQ/kuLvkv67nsbvor77nqItkZAIBD2QWBGYPFQEBMmQCAQ8PFgIfAwUhc3VwZXJ2aXNlL3NtYW5jb3Vyc2UuYXNweD90eXBlPTQwFgIfBAUdc2hvd190aXRsZSgi6L6F5L+u57G76K++56iLIikWAmYPDxYCHwAFD+i+heS/ruexu+ivvueoi2RkAgIPZBYEZg8VAQEzZAIBDw8WAh8DBSFzdXBlcnZpc2Uvc21hbmNvdXJzZS5hc3B4P3R5cGU9NDEWAh8EBSBzaG93X3RpdGxlKCLlhazlhbHns7vliJforrLluqciKRYCZg8PFgIfAAUS5YWs5YWx57O75YiX6K6y5bqnZGQCAw9kFgRmDxUBATRkAgEPDxYCHwMFIXN1cGVydmlzZS9zbWFuY291cnNlLmFzcHg/dHlwZT00MhYCHwQFGnNob3dfdGl0bGUoIuS4k+S4muiusuW6pyIpFgJmDw8WAh8ABQzkuJPkuJrorrLluqdkZAIbDxYCHgZvbmxvYWQFE2NoYW5nZUZyYW1lSGVpZ2h0KClkZNS/s1A3o5MP5gjS1YnvZsg1evG6wG2i8C3uGdMWujkJ'
# s2 = 'CA0B0334'
s3 = '4251'
s4 = '240550'

url = 'http://222.73.34.165:88/student/schapter.aspx?chapterid=4251&add=1'


headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0",
           "Connection": "keep-alive",
           "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Content-Length": '696',
           "Content-Type": "application/x-www-form-urlencoded",
           "Upgrade-Insecure-Requests": "1",
           'Origin': 'http://222.73.34.165:88',
           'Cache-Control': 'max-age=0',
           'Referer': url,
           'Host': '222.73.34.165:88'}

cookies_dict = {'ASP.NET_SessionId': '1deslfvwfx3r3ges5rxqfocu'}

# r1 = requests.post(url,
#                    cookies=cookies_dict)
#
# soup = BeautifulSoup(r1.text, 'html.parser')
# s1 = soup.find(id="__VIEWSTATE").get('value')
# s2 = soup.find(id="__VIEWSTATEGENERATOR").get('value')
# s3 = soup.find(id="hchapterid").get('value')
# s4 = soup.find(id="huserid").get('value')

s1 = '/wEPDwUKMTM1ODI5MTYyMA9kFgICAw9kFgICAQ9kFg4CAQ8PFgIeBFRleHQFBlVuaXQgN2RkAgMPDxYCHwAFLHVuaXQmbmJzcDs3Jm5ic3A7Y29tcHV0ZXImbmJzcDtjb21tdW5pY2F0aW9uZGQCBQ8PFgIfAAUCMjdkZAIHDw8WAh8ABQkw5YiGNTXnp5JkZAIRDw8WAh8ABQbkuLvnq5lkZAITD2QWBAIBDw8WBB8ABQfplZzlg48xHgtOYXZpZ2F0ZVVybAUlL3N0dWRlbnQvc2NoYXB0ZXIuYXNweD9jaGFwdGVyaWQ9NDI1MWRkAgMPDxYEHwAFB+mVnOWDjzIfAQU2L3N0dWRlbnQvc2NoYXB0ZXIuYXNweD9jaGFwdGVyaWQ9NDI1MSZhZGQ9MSZtaXJyb3Jubz0xZGQCFw8WAh4Dc3JjBTdodHRwOi8vMjIyLjczLjMzLjI1MDo4OC9maWxlcy9WaWRlby9qc2p5eTE0L2NvbnRlbnQuaHRtZGTiJHLLXkItXpX40cRRuBXLKLAGaDUo3slGvJ/9Am38qA=='
s2 = '8C48877A'
print(s1, s2, s3, s4)
print(cookies_dict)
r2 = requests.post(url=url,
                   headers=headers,
                   data={'__VIEWSTATE': s1,
                         '__VIEWSTATEGENERATOR': s2,
                         'Button2': '结束学习',
                         'hchapterid': s3,
                         'huserid': s4,
                         'hlearntime': '3000'},
                   cookies=cookies_dict)
print(r2.text)



