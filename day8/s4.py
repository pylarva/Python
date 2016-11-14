# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 特殊成员


class Foo:
    """
    注释 __doc__
    """

    def __init__(self, name, age):  # 构造方法
        self.name = name
        self.age = age

    # 析构方法：在垃圾回收之前执行
    def __del__(self):
        pass

    def __call__(self, *args, **kwargs):
        print('call')

    def __str__(self):
        return '%s - %s ' % (self.name, self.age)

    def __getitem__(self, item):
        print('getitem')
        print(item.start, item.stop, item.step)

    def __setitem__(self, key, value):
        print('setitem')

    def __delitem__(self, key):
        print('delitem')


# p = Foo()
# print(p.__class__)
#
# # 对象后面加括号执行 __call__ 方法
# p()
# # 两个括号
# Foo()()

obj1 = Foo(name='alex', age=18)
obj2 = Foo(name='wusir', age=18)
# print(obj1)
# print(obj2)

# 手动str也会去执行类里面的 str方法
ret = str(obj1)
# print(ret)

# 获取对象中封装的数据返回一个字典
ret = obj1.__dict__
# print(ret)

# 全部的类方法
# print(Foo.__dict__)

# 中括号语法自动执行 getitem 方法
obj = Foo('alex', 100)
# obj['ab']
# obj['k1'] = 111
# del obj['k1']
ret1 = obj[1:6:2]
print(ret1)
