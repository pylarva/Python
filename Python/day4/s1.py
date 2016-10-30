#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


# def f1(a, b):
#     return a + b

# 1、定义的函数是否可以被调用执行
# a = 100
# b = 10
# print(callable(f1))

# 2、ACSII码转换数字
# print(chr(65))
# print(ord('A'))

# 3、生成随机验证码
import random
li = []
for i in range(6):
    r = random.randrange(0, 5)
    if r == 2 or r == 4:
        num = random.randrange(0, 9)
        li.append(str(num))
    else:
        temp = random.randrange(65, 91)
        c = chr(temp)
        li.append(c)
result = "".join(li)  # 使用join时元素必须是字符串
print(result)

# 4、Python先编译后执行
# 编译， 单行single, 表达式eval, 和Python一样的格式exec
# 将字符串编译成Python代码
# compile()
# 执行
# eval()
# exec()
# s = "print(123)"
# r = compile(s, "<string>", "exec")  # 将字符串编译成Python代码
# exec(r)

# exec 和 eval 都可以执行，通常exec功能更强大（可以接受代码或者字符串）
# 但是 eval 有返回值，exec没有
# s = "8*8"
# ret = eval(s)
# print(ret)

# 5、查看对象提供的功能
#print(dir(dict))
#help(list) # 读模块源码

# 6、共97，每页显示10条，需要最少页
# r = divmod(97, 10)
# n1, n2 = divmod(97, 10)
# print(n1, n2)

# 7、判断某一对象是否是某类的实例
# s = [1, 2, 3]
# print(isinstance(s, list))

# 8、筛选函数filter
# 函数返回True，将元素添加到结果中
# filter(函数， 可迭代对象)
# 循环第二个参数，让每一个参数去执行函数，如果返回True，表示元素合法
# def f2(a):
#     if a > 22:
#         return True
# li = [11, 22, 33]
# ret = filter(f2, li)
# result = filter(lambda a: a > 22, li)
# print(list(ret))
# print(list(result))

# lambda 会自动 return
# f1 = lambda a: a > 30
# ret = f1(90)
# print(ret)

# 8、筛选函数 map
# 将函数返回值添加到结果中
# 对可迭代对象内的元素做统一操作
# li = [11, 22, 33, 44]
# result = map(lambda a: a+100, li)
# print(list(result))

# 9、所有的全局变量、局部变量
# NAME = 'AAA'
# def show():
#     a = 123
#     b = 456
#     print(locals())
#     print(globals())
# show()

# 10、hash值
# 将一个对象转换成他的hash值
# s = 'hhh'
# print(hash(s))

# 11、len长度计算
# python 3 里面按照字符查找，返回2
# Python 2 里面按照字节查找，返回6
# s = '李杰'
# print(len(s))

# 12、round
# print(round(1.4))
# print(round(1.8))

# 13、zip 并行迭代
# l1 = ["kobe", 11, 22, 33]
# l2 = ["is", 11, 22]
# l3 = ["boy", 11, 22, 33]
# r = zip(l1, l2, l3)
# tmp = list(r)[0]
# print(" ".join(tmp))
