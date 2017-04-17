# !/usr/bin/env python
# -*- coding:utf-8 -*-

from multiprocessing import Process
from multiprocessing import queues
import multiprocessing
import queue

import time
from multiprocessing import Pool


def f1(a, b):
    time.sleep(1)
    print(a, b)

if __name__ == '__main__':
    pool = Pool(5)

    for i in range(5):
        pool.apply(func=f1, args=(i, i))
        # 异步执行 一部到位
        # pool.apply_async(func=f1, args=(i,))

    # close 表示所有的子进程任务执行完毕
    pool.close()
    # time.sleep(1)
    # terminate 表示立即终止所有子进程
    # pool.terminate()
    pool.join()