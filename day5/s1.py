#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

USER_INFO = {}


def login():
    user_name = input('请输入用户名： ')
    global USER_INFO
    USER_INFO['is_login'] = True
    return USER_INFO


def check_login(func):
    def inner(*args, **kwargs):
        if USER_INFO.get('is_login', None):
            ret = func(*args, **kwargs)
            return ret
        else:
            print('请登陆...')
    return inner


def check_admin(func):
    def inner(*args, **kwargs):
        if USER_INFO.get('user_type', None) == 2:
            ret = func(*args, **kwargs)
            return ret
        else:
            print('权限不足...')
    return inner


@check_login
@check_admin
def index():
    print('home')


def change_pwd():
    print('successed....')


def main():
    while True:
        print('1、登陆\n2、用户信息\n3、高级用户\n >>>')
        inp = input('请输入编号： ')
        if inp == '1':
            login()
        if inp == '2':
            index()


main()