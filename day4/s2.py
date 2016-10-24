#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


# def outer(func):
#     def inner():
#         print('log')
#         return func()
#     return inner
#
#
# @outer
# def f1():
#     print('F1')
#
#
# @outer
# def f2():
#     print('F2')


li = ['1|2|3', '4|5|6']
for line in li:
    if '1' in line.split('|'):
        print('yes')



