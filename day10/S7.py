# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 多线程

import time
import threading


def f1(i):
    time.sleep(5)
    print(i)

# f1(1)
# f1(2)

t = threading.Thread(target=f1, args=(123, ))
# 设置主线程不等此线程
t.setDaemon(True)
# 线程被创建并准备好 等待CPU来调度
t.start()
# join 表示主线程到此进入等待状态 直到所有子线程执行完毕
# join(2) 最多等待2秒
t.join()
# f1(111)
print('end')

