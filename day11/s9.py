# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# ["进程间数据共享三种方式"]

# 进程间数据不能共享

# from multiprocessing import Process
#
# li = []
#
#
# def foo(i,):
#     li.append(i)
#     print('say hi', li,)
#
#
# if __name__ == '__main__':
#     for i in range(10):
#         p = Process(target=foo, args=(i, ))
#         p.start()
#         p.join()
#     print('end', li)

# 方式一 queues

from multiprocessing import Process
from multiprocessing import queues
import multiprocessing


def foo(i, arg):
    arg.put(i)
    print('say hi', i, arg.qsize())

if __name__ == '__main__':
    li = queues.Queue(20, ctx=multiprocessing)
    for i in range(10):
        p = Process(target=foo, args=(i, li, ))
        p.start()

# 方式二 Array数据

# from multiprocessing import Process
# from multiprocessing import Array
#
#
# def foo(i, arg):
#     arg[i] = i + 100
#     for item in arg:
#         print(item)
#     print('=========')
#
#
# if __name__ == '__main__':
#     li = Array('i', 10)
#     for i in range(10):
#         p = Process(target=foo, args=(i, li, ))
#         p.start()
#         p.join()

# 方式三 dict

# from multiprocessing import Process
# from multiprocessing import Manager
# import time
#
#
# def foo(i, arg):
#     arg[i] = 100 + i
#     print(arg.values())
#
# if __name__ == '__main__':
#     obj = Manager()
#     li = obj.dict()
#     for i in range(10):
#         p = Process(target=foo, args=(i, li, ))
#         p.start()
#         p.join()

    # 主进程结束后 和子进程之间的链接就会断开
    # time.sleep(2)