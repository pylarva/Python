#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 常见格式化

# s = "numbers: {0:b},{0:o},{0:d},{0:x},{0:X}, {0:%}".format(15)
# print(s)

# s = " I am %s 百分号: %% " % 'kobe'
# print(s)

# s = '%(name)-10s %(age) 10d %(p).2f' % {'name': 'kobe', 'age': 30, 'p': 1.1234}
# print(s)
#
# s1 = 'sdfsdf{0}23s{0}df{1}'.format(123, 'cool')
# print(s1)
#
# s2 = "----{name:s}_____{age:d}======{name:s}".format(name='cool', age=123)
# print(s2)
#
# s3 = "---{:#^20s}===={:+d}====={:#b}".format('cool', 123, 15)
# print(s3)
#
# s4 = "abc {:.2%}".format(0.234567)
# print(s4)

# li = [11, 22, 33, 44]
# result = filter(lambda x: x > 22, li)
# print(result)  # 具有生成指定条件数据的能力的一个对象


# 生成器
# 生成器，使用函数创造

# 普通函数
# def func():
#     return '123'
# ret = func()


# def func():
#     print('123')
#     yield 1
#     yield 2
#     yield 3
#
# ret = func()
# print(ret.__next__())
# print(ret.__next__())
# print(ret.__next__())


# for i in ret:
#     print(i)

# r1 = ret.__next__()  # 进入函数找到yield，获取yield后面的数据
# print(r1)
# r2 = ret.__next__()
# print(r2)
# r3 = ret.__next__()
# print(r3)


# def myrange(arg):
#     start = 0
#     while True:
#         if start > arg:
#             return
#         yield start
#         start += 1
#
# ret = myrange(10)
# print(list(ret))


#  递归
# def func(n):
#     n += 1
#     if n >= 4:
#         return 'end'
#     print(n)
#     return func(n)
#
# r = func(1)
# print(r)


# 模块
# import sys
#
# # lib.commons.f1()
# # sys.path.append('E:\\')  # 添加系统路径
# for item in sys.path:  # python系统路径
#     print(item)

# from s1 import * # 适合导入嵌套在文件夹下的模块

# 第三方模块
# requests pip3 源码
# 1、系列化相关
import json
dic = {'k1': 'v1'}
# result = json.dumps(dic)  # 序列化 将python的基础数据类型转化成字符串形式
# print(result, type(result))
# s1 = '{"k1": 123}'
# dic1 = json.loads(s1)  # 反序列化 将字符串类型转换成python数据类型
# print(s1, type(dic1))

json.dump(dic, open('test', 'w'))
result = json.load(open('test', 'r'))
print(result, type(result))


