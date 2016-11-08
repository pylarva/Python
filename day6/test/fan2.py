# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# import fan1
#
# user_input = input('输入编号：')
# if hasattr(fan1, user_input):
#     func = getattr(fan1, user_input)
#     func()
# else:
#     print('no module...')

user_input = input('请输入URL：')
k, v = user_input.split('/')
obj = __import__('lib.' + k, fromlist=True)
if hasattr(obj, v):
    func = getattr(obj, v)
    func()
else:
    print('no module...')

