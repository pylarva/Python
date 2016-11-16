# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 类迭代属性


class Bar:
    pass


class Foo(Bar):

    def __iter__(self):
        # return iter([11, 22, 33, 44])
        yield 1
        yield 2


obj = Foo()
for item in obj:
    print(item)

# 查看 obj 是否是 Foo 的实例
ret = isinstance(obj, Foo)
# 也可以查看是否是 父类 的实例
# ret = isinstance(obj, Bar)
print(ret)
# 查看 Foo 是否为 Bar 的子类
ret1 = issubclass(Foo, Bar)
print(ret1)

