# -*- coding:utf-8 -*-
import requests

s1 = '/wEPDwUKMTM1ODI5MTYyMA9kFgICAw9kFgICAQ9kFg4CAQ8PFgIeBFRleHQFBlVuaXQgMWRkAgMPDxYCHwAFFkNvbXB1dGVyJm5ic3A7T3ZlcnZpZXdkZAIFDw8WAh8ABQIzMGRkAgcPDxYCHwAFCTfliIYyNuenkmRkAhEPDxYCHwAFBuS4u+ermWRkAhMPZBYEAgEPDxYEHwAFB+mVnOWDjzEeC05hdmlnYXRlVXJsBSUvc3R1ZGVudC9zY2hhcHRlci5hc3B4P2NoYXB0ZXJpZD00MjM4ZGQCAw8PFgIeB1Zpc2libGVoZGQCFw8WAh4Dc3JjBTZodHRwOi8vMjIyLjczLjMyLjU4Ojg4L2ZpbGVzL1ZpZGVvL2pzanl5MDEvY29udGVudC5odG1kZIVrh7CEzPV1Gt6qMgHb7uo99SCEjRbq5r4YnK8xehtK'
s2 = '8C48877A'
c1 = {'JSESSIONID': 'B72DDBA8B6E199D9006D9F4C72B675B4', 'ASP.NET_SessionId': 'o0qatloubof1dmj0jzjbycr'}

r2 = requests.post('http://222.73.34.165:88/student/scourse.aspx?courseid=142',
                   data={'__VIEWSTATE': s1,
                         '__VIEWSTATEGENERATOR': s2,
                         'Button2': '结束学习',
                         'hchapterid': '4242',
                         'huserid': '240550',
                         'hlearntime': 300},
                   cookies=c1)

print(r2.text)