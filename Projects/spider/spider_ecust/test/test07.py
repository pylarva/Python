# !/usr/bin/env python
# -*- coding:utf-8 -*-


d1 = {'a': '', 'b': '', 'c': ''}
d2 = {'e': '4', 'b': '2', 'a': '1'}

for i in d1.keys():
    if i in d2.keys():
        d1[i] = d2.get(i)

print(d1)