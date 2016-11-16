# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 成员修饰符
# 私有
#     只有内部成员调用有效
# 共有
#     内部、外部均可调用

# 字段修饰符


class Foo:

    __cc = 123

    def __init__(self, name):
        self.__name = name  # 加两个下划线__表示私有字段 外部、继承都不能调用

    def f1(self):
        print(self.__name)

    @staticmethod
    def f3():
        print(Foo.__cc)


obj = Foo('kobe')
# print(obj.__name)  # 通过对象外部访问内部普通字段不成功
# obj.f1()

# print(Foo.__cc)  # 通过外部访问内部静态字段也不成功
obj.f3()

# 特殊访问方法
# print(obj._Foo__name)