# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 类属性


class Pager:

    def __init__(self, all_count):
        self.all_count = all_count

    @property
    def all_pager(self):
        a1, a2 = divmod(self.all_count, 10)
        if a2 == 0:
            return a1
        else:
            return a1 + 1

    @all_pager.setter
    def all_pager(self, value):
        print(value)

    @all_pager.deleter
    def all_pager(self):
        print('del all_pager')


p = Pager(101)
# print(p.all_count)  # 字段
# ret = p.all_pager()  # 方法
# print(ret)

# 使用字段的调用来调用方法
ret = p.all_pager
print(ret)

# 想设置数值
p.all_pager = 100

# 删除属性
del p.all_pager



