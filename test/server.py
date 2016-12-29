# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re

s = 'run \"1\" --hosts 10.0.0.1 10.0.0.2'
#
# if not re.match('run \".*\" --hosts (25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}', s):
# # if not re.match('run \".*\" --hosts .*', s):
#     print('cmd error...')
# else:
#     print(s)

# s = "-"
# if not re.match('-', s):
#     print('no')
# else:
#     print('yes')
#
# li = re.compile(' (25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}')
# print(li.findall(s))

print(s.split(' ')[3:], len(s.split(' ')))
print()






