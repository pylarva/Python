#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# s = '%(name)-10s %(age)-10d %(p).2f' % {'name': 'kobe', 'age': 30, 'p': 1.1234}
# print(s)
#
# s1 = 'sdfsdf{0}23s{0}df{1}'.format(123, 'cool')
# print(s1)
#
# s2 = "----{name:s}_____{age:d}======{name:s}".format(name='cool', age=123)
# print(s2)
#
# s3 = "---{:a^20s}===={:+d}====={:#b}".format('cool', 123, 15)
# print(s3)
#
# s4 = "sdfsdfsdf {:.2%}".format(0.234567)
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


def func():
    print('123')
    yield 1
    yield 2
    yield 3

ret = func()
# for i in ret:
#     print(i)

r1 = ret.__next__()  # 进入函数找到yield，获取yield后面的数据
print(r1)
r2 = ret.__next__()
print(r2)
r3 = ret.__next__()
print(r3)


def myrange(arg):
    start = 0
    while True:
        if start > arg:
            return
        yield start
        start += 1

ret = myrange(10)
