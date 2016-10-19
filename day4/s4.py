#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


def outer(func):
    def inner(*args, **kwargs):
        print('123')
        r = func(*args, **kwargs)
        print('456')
        return r
    return inner


# @ + 函数名
# 功能：
#      1. 自动执行outer函数并将下面的函数名f1当作参数传递
#      2. 将outer函数的返回值，重新赋值给f1
@outer
def f1(arg):
    print('F1')
    return 'hahha'

@outer
def f2(arg1, arg2):
    print('F2')
    return 'heheh'