
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import re

s = '8+2'
s1 = '-8'

# t = re.split('(\d+[*/]\d+)', s, 1)
# print(t)

t = re.search('(.*)', s).groups()
print(t)

print(int(s1))