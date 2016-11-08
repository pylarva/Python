# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 封装对象


class c1:

    def __init__(self, name, obj):
        self.name = name
        self.obj = obj


class c2:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(self.name)


c2_obj = c2('aa', 11)
c1_obj = c1('kobe', c2_obj)
c2_obj.show()
print(c1_obj.obj.name)