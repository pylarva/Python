# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


class Foo:

    def f1(self):
        return 100

    def f2(self, value):
        print(value)

    def f3(self):
        print('300')

    # 类属性定义
    Foo = property(fget=f1, fset=f2, fdel=f3)

obj = Foo()

# 取值
ret = obj.Foo
print(ret)

# 赋值
obj.Foo = 200

# 删除
del obj.Foo
