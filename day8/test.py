# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


# 面向对象编程
class Foo:  # 创建类

    def __init__(self, name, age):  # Foo接收到两个参数后会封装在自己类内部
        self.name = name
        self.age = age


obj = Foo('kobe', 18)  # 创建一个对象 传两个参数
print(obj.name, obj.age)  # 外面调用封装好的参数