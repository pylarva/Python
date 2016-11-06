# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import test
#
# def run():
#     innp = 'qing: '
#     if innp == 'man':
#         test.man()
#     elif innp == 'woman':
#         test.woman()
#     elif innp == 'cat':
#         test.cat()
#     else:
#         print('no')
# run()

def run():
    innp = input('a:')
    # obj = __import__(innp, fromlist=True)
    if hasattr(test, innp):
        func = getattr(test, innp)
        func()
    else:
        print('no')
run()