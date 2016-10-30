#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


# 三元运算
if 1==1:
    name = "kobe"
else:
    name = "jordan"

name = "kobe" if 1 == 1 else "jordan"


# lambda表达式
def f1(a1):
    return a1 + 100

f2 = lambda a1, a2: a1 + a2

ret = f1(10)
ret2 = f2(100,10)
print(ret,ret2)