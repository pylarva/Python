# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 进程锁

from multiprocessing import Process
from multiprocessing import Array
from multiprocessing import RLock, Lock, Event, Condition, Semaphore
import time


def foo(i, lis, lc):
    lc.acquire()
    lis[0] = lis[0] - 1
    time.sleep(1)
    print('say hi', lis[0])
    lc.release()

if __name__ == '__main__':
    li = Array('i', 1)
    li[0] = 10
    lock = RLock()
    for i in range(10):
        p = Process(target=foo, args=(i, li, lock))
        p.start()

