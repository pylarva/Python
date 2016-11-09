# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 继承原理就是优先使用自己的self 如果自己没有再去复制


class S1:

    def F1(self):
        self.F2()

    def F2(self):
        pass


class S2(S1):

    def F3(self):
        self.F1()

    def F2(self):
        pass

obj = S2()
obj.F3()


# 多继承

class C0:

    def f2(self):
        pass


class C1(C0):

    def f2(self):
        pass


class C2:

    def f2(self):
        pass


class C3(C1, C2):

    def f3(self):
        pass

obj = C3()
obj.f2()