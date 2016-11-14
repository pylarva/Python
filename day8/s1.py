# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 面向对象的多态

# 类成员 字段


class Foo:
    # 字段（静态字段 保存在类里面）
    CC = 123

    def __init__(self, name):
        # 字段(普通的字段 保存在对象里面)
        self.name = name

    # 普通方法：对象调用执行 方法属于类
    def show(self):
        print(self.name)

    @staticmethod
    def f1():
        # 静态方法 由类调用执行
        print('f1')

    @classmethod
    def f2(cls):  # class 自动给类名传进去了
        # 类方法
        # cls 是类名 加()创建对象
        print(cls)

    def f3(self):
        return self.name[1]


T1 = Foo('alex')
# 普通字段只能通过对象访问
print(T1.name)
# 一般情况下访问静态字段 只能通过类来访问
print(Foo.CC)
# 也可以用对象来访问
print(T1.CC)

# 直接用类调用函数
Foo.f1()
Foo.f2()

obj = Foo('alex')
ret = obj.f3()
print(ret)