# -*- coding:utf-8 -*-
import requests

s1 = '/wEPDwULLTEwMTQ2MjE4MjhkZC0kr8EqVmReGz8wShIStvlReqepxl2ifQoJhTN8zjbL'
s2 = 'C2EE9ABB'
c1 = {'JSESSIONID': 'B72DDBA8B6E199D9006D9F4C72B675B4', 'ASP.NET_SessionId': 'no0qatloubof1dmj0jzjbycr'}

r1 = requests.post('http://222.73.34.165:88/student/allcourse.aspx',
                   data={'__VIEWSTATE': s1,
                         '__VIEWSTATEGENERATOR': s2,
                         '__EVENTTARGET': '',
                         '__EVENTARGUMENT': '',
                         'Button1': '确认登陆',
                         'username': '26160554',
                         'pwd': 'Bingo_1991',
                         'gtpath': ''},
                   cookies=c1)

print(r1.text)