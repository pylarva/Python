#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import re

dic = {'1':['name'],'2':[{'name':1,'age':2},{'name':3,'age':4}]}
dicc = dic['2']
print(dicc)
for k,v in enumerate(dicc):
    print('%-5s'% k,end='')
    print(dicc[k]['name'],'  ',dicc[k]['age'])
# print(dic.get('2'))
# ret = dic.get('2')
# print(ret)
# if ret == None:
#     dic.setdefault('2', [5, 6])
# else:
#     dic['2'].append(7)
#
# print(dic)

# with open('text_a','r') as file:
#     for line in file:
#         #line = re.split('\s+', line)
#         line = line.split()
#         print(line)
#         print(type(line))