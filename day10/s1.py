# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# python中无块级作用域
# python以函数为作用域

# if 1 == 1:
#     name = 'alex'
# print(name)
#
# for i in range(10):
#     name = i
# print(name)

# Python作用域链 由内向外找

# name = '1'
# def f1():
#     name = '2'
#     def f2():
#         name = '3'
#         print(name)
#     f2()
# f1()

# 在函数执行之前 Python已经确定好了所有作用域
# 不会因为函数的嵌套 而改变作用域链

# name = 'alex'
# def f1():
#     print(name)
# def f2():
#     name = 'eric'
#     f1()
# f2()

# name = 'alex'
# def f1():
#     print(name)
# def f2():
#     name = 'eric'
#     return f1
# ret = f2()
# ret()

# 特殊的语法

li = [x+100 for x in range(10) if x > 6]
print(li)
li = [lambda :x for x in range(10)]
# li列表中的元素： [函数, 函数,...]
# 函数在没有执行前 内部代码不执行
# for 循环执行完成后 生成了10个函数 函数里面有定义了一个x
# 由于生成的函数一旦被执行 就会去找for循环最后生成的 x值 9
ret = li[0]()
print(ret)


# li = []
# for i in range(10):
#     def f1():
#         return i
#     li.append(f1)
# li[0]()
# li[1]()

# x被执行了

# li = []
# for i in range(10):
#     def f1(x=i):
#         return x
#     li.append(f1)
# print(li[0]())
# print(li[1]())
# print(li[2]())

# Python多继承 经典类(一条道走到黑) 新式类
