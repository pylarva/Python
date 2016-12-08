# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import time
import queue
import threading

q = queue.Queue(20)


def productor(arg):
    while True:
        q.put(str(arg) + '包子')


def consumer(arg):
    while True:
        print(arg, q.get())
        time.sleep(2)

for i in range(3):
    t = threading.Thread(target=productor, args=(i, ))
    t.start()

for j in range(20):
    t = threading.Thread(target=consumer, args=(j, ))
    t.start()