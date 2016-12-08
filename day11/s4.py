# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import threading
import time


NUM = 10


def func(l):
    global NUM
    l.acquire()
    NUM -= 1
    time.sleep(1)
    print(NUM)
    l.release()

# lock = threading.Lock()
lock = threading.RLock()

for i in range(10):
    t = threading.Thread(target=func, args=(lock, ))
    t.start()