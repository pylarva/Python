# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 进程池

import time
from multiprocessing import Pool


def f1(arg):
    time.sleep(1)
    print(arg)

if __name__ == '__main__':
    pool = Pool(5)

    for i in range(30):
        # pool.apply(func=f1, args=(i, ))
        # 异步执行 一部到位
        pool.apply_async(func=f1, args=(i, ))

    # close 表示所有的子进程任务执行完毕
    pool.close()
    # time.sleep(1)
    # terminate 表示立即终止所有子进程
    # pool.terminate()
    pool.join()