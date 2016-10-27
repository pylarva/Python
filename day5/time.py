# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
#
# print(time.time())
# print(time.ctime(time.time()-86400))
# time_obj = time.gmtime()
# print(time_obj.tm_year, time_obj.tm_mon, time_obj.tm_mday)
# print(time.localtime())
# print(time.mktime(time_obj))  # 转时间戳
#
# # 将struct_time格式转换成指定格式
# print(time.strftime("%Y-%m-%d %H:%S", time.localtime()))
#
# # 与strftime相反
# tm = time.strptime("2016-10-10 10:50", "%Y-%m-%d %H:%M")
# print(tm)


import datetime

print(datetime.date.today())
print(datetime.date.fromtimestamp(time.time()-86400))  # 将时间戳转换成格式化日期
print(datetime.datetime.now())  # 显示当前时间

# 时间加减
print(datetime.datetime.now() + datetime.timedelta(days=10))  # 比现在加10天
print(datetime.datetime.now() - datetime.timedelta(days=10))  # 比现在晚10天
print(datetime.datetime.now() + datetime.timedelta(hours=10))  # 加10小时
current_time = datetime.datetime.now()
print(current_time.replace(2015, 10, 10))  # 直接替换时间
print(datetime.datetime.strptime("09/10/15 11:40", "%d/%m/%y %H:%M"))

