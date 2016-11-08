
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import re
a = 'hello'

b = 'world'

# c = a + b
# c = '%s %s'% (a,b)
# dic = {'name': 'hello', 'name_2': 'world'}
# c = '{name:s} {name_2:s}'.format(name='hello', name_2='world')

# print(c)

# dic = {'name': 'kobe'}
# print(dic['name'])


# a =  lambda  x,y : x +y

# def sum(x, y):
#     return x + y

# def change(**kwargs):
#     if kwargs['sex'] == 'F':
#         print(kwargs['count'])
#     elif kwargs['sex'] == 'M':
#         print(kwargs['count'], kwargs['name'])
#
# innp = change(sex='M', count=23, name='hah')

# def outer_2():
#
#
# def outer(func):
#     def inner(user, num):
#         if 1 == 1:
#             func(user, num)
#         else:
#             print('permission deny')
#             return
#     return inner
#
#
# @outer
# def func1(user, num):
#     print(" welcome")
#
# func1('kobe', 2)

def out2(kaiguan):
    def outer(func):
        def inner(*args):
            if kaiguan == 1:
                return func(*args)
            else:
                print('permission deny')
        return inner
    return outer


@out2(2)
def func1():
    print(" welcome")

func1()

# def man():
#     print(" man is strong")
#
#
# def woman():
#     print("woman is beautiful")
#
#
# def cat():
#     print("cat miao miao ")
#
# dic = {'name': 'kobe', 'age': 18}
# print(dic.get('age'))
#
# name = 'kobe' if 1 == 1 else 'jordan'
# print(name)
#
# f = lambda a1, a2: a1 + a2
# r = f(1, 2)
# print(r)

