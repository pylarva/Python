# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import threading


def func(i, e):
    print(i)
    e.wait()
    print(i + 100)

event = threading.Event()

for i in range(10):
    t = threading.Thread(target=func, args=(i, event,))
    t.start()

event.clear()

inp = input('>>>')
if inp == '1':
    event.set()


