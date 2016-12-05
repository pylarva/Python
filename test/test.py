# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

from __future__ import division
import math
import sys
import time


def progressbar(cur, total):
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ( '=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    if cur == total:
        sys.stdout.write('\n')

if __name__ == '__main__':

    file_size = 102400
    size = 0
    while file_size >= size:
        # progressbar(size*10/file_size, 10)
        progressbar(size, file_size)
        size += 1024
        time.sleep(0.1)
