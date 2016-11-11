# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import pickle


class Teacher:
    def __init__(self, name, age, asset):
        self.name = name
        self.age = age
        self.asset = asset
        self.list = []

    def F1(self):
        print('F1')

# T1 = Teacher(name='li', age=18, asset=0)
# li = []
# li.append(T1)
# pickle.dump(li, open('a', 'wb'))
r = pickle.load(open('a', 'rb'))
# r[0].list = [1, 2, 3]
# pickle.dump(r, open('a', 'wb'))
print(r[0].list)
