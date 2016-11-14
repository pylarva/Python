# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import pickle
import time


class F1:
    def __init__(self, name):
        self.name = name
        self.list = []


class F2:
    def __init__(self, name):
        self.name = name
        self.list = []

# li = []
#
# a = 1
# T1 = F1(name='S1')
# T1.list.append(a)
# print(T1.list)
#
# T2 = F2(name='S2')
# T2.list.append(T1)
# print(T2.list[0].list)
#
# li.append(T2)

# pickle.dump(li, open('db', 'wb'))


# li = pickle.load(open('db', 'rb'))

# b = 2
# c = 3
# T1.list.append(c)

# T3 = li[0].list[0].list.append(b)
# print(li[0].list[0].list)
#
# pickle.dump(li, open('db', 'wb'))

print(time.strftime('%Y-%m-%d %H:%m'))


