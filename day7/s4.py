# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 封装对象


# class c1:
#
#     def __init__(self, name, obj):
#         self.name = name
#         self.obj = obj
#
#
# class c2:
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def show(self):
#         print(self.name)
#
#
# c2_obj = c2('aa', 11)
# c1_obj = c1('kobe', c2_obj)
# c2_obj.show()
# print(c1_obj.obj.name)


# 继承

class F1():  # 父类 基类
    def show(self):
        print('show')

    def foo(self):
        print(self.name)


class F2(F1):  # 子类 派生类
    def __init__(self, name):
        self.name = name

    def bar(self):
        print('bar')
    # def show(self):
    #     print('F2.show')


class F3(F2):
    pass

obj = F2('alex')
obj.foo()
# obj.bar()
# obj.show()
