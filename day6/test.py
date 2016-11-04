
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import re

s = '2*(-8)-9'

# 取第一个括号内容
s1 = re.search('\(([0-9 *+-/]+)\)', s).groups()
print(s1)

# 处理乘除
s1 = s1[0]
# if s1

s_before = re.split('\(-*\d+[*/]\d+\)', s, 1)[0]
s_back = re.split('\(-*\d+[*/]\d+\)', s, 1)[1]
print(s_before, s_back)


f = re.search('-*\d+[*/]\d+', s1).group()  # 乘表达式
print(f)
t1 = re.split('[*]', f)[0]
t2 = re.split('[*]', f)[1]
print(t1, t2)
t = int(t1) * int(t2)  # 乘的结果
print(t)
t = str(t)
if int(t) < 0:
    s = s_before + '(' + t + ')' + s_back
else:
    s = s_before + t + s_back
print(s)

# 处理加减
# s1 = s1[0]
# f = re.search('-*\d+[+-]\d+', s1).group()  # 加减表达式
# print(f)

