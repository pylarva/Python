# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 反射

# def run():
#     inp = input('请输入要访问的url:')
#     if inp == 'login':
#         commons.login()
#     elif inp == 'logout':
#         commons.logout()
#     elif inp == 'home':
#         commons.home()
#     else:
#         print('404')


def run():
    inp = input('请输入要访问的url:')
    # inp字符串类型 inp = "login"
    # commons.inp() # commons.login
    # 利用字符串的形式去(模块)中操作(寻找)成员
    # hasattr 检查模块中成员是否存在
    # delattr
    # setattr
    m, f = inp.split('/')
    obj = __import__('lib.' + m, fromlist=True)  # __import__在导入模块的时候路径拼接只能到第一个参数lib

    if hasattr(obj, f):
        func = getattr(obj, f)
        func()
    else:
        print('404')
run()