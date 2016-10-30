#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
#
# import requests
import json
#
# response = requests.get('http://wthrcdn.etouch.cn/weather_mini?city=上海')
# response.encoding = 'utf-8'
#
# dic = json.loads(response.text)
# print(dic, type(dic))

# 双引号和单引号在python中反序列化
li = '["kobe", "jordan"]' #  正确写法
#li = "['kobe', 'jordan']" #  错误写法
ret = json.loads(li)
print(ret, type(ret))