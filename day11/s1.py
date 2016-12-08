# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 自定义线程类

import threading

# 方法一

# def f1(arg):
#     print(arg)
#
# t = threading.Thread(target=f1, args=(123, ))
# t.start()

# 方法二
# 线程被创建准备好后 被cpu调度会去执行threading.Thread里面的 run 方法


class MyThread(threading.Thread):

    def __init__(self, func, args):
        self.func = func
        self.args = args
        super(MyThread, self).__init__()

    def run(self):
        self.func(self.args)


def f2(arg):
    print(arg)

obj = MyThread(f2, 123)
obj.start()