# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time, sys

CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}


def login():
    """
    用户登陆
    :return:
    """
    while True:
        username = input('请输入用户名： ')
        password = input('请输入密码: ')


def user_create():
    pass


def user_del():
    pass


def user_freeze():
    pass


def user_unfreeze():
    pass


def show():
    print('1、信用卡开户\n2、信用卡删除\n3、信用卡冻结\n4、信用卡解冻\n5、退出')
    while True:
        user_select = input('请输入编号：')
        if user_select == '1':
            user_create()
        if user_select == '2':
            user_del()
        if user_select == '3':
            user_freeze()
        if user_select == '4':
            user_unfreeze()
        if user_select == '5':
            print('退出系统成功.')
            time.sleep(2)
            sys.exit()
        else:
            print('出入不正确...')


