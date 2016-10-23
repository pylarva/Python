#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time

LOGIN_USER = {'is_login': False}
USER_LEVEL = ''
USER_NAME = ''

def login(user_db):
    while True:
        USER_NAME = input('请输入用户名： ')
        user_pwd = input('请出入密码: ')
        for line in user_db:
            if USER_NAME in line:
                if user_pwd == line.split('|')[1]:
                    print('%s,登陆成功.'% USER_NAME)
                    LOGIN_USER = True
                    USER_LEVEL = int(line.split('|')[4])
                    print(USER_LEVEL)
                    return USER_NAME, LOGIN_USER, USER_LEVEL
        print('用户或者密码错误...')
        time.sleep(2)
        continue


def outer(func):
    def inner(user_db, USER_LEVEL, user_name):
        if LOGIN_USER['is_login']:
            r = func(user_db, USER_LEVEL, user_name)
            return r
        else:
            (USER_NAME, ret, USER_LEVEL) = login(user_db)
            if ret:
                r = func(user_db, USER_LEVEL, USER_NAME)
                return r
    return inner


def db_read():
    user_file = 'user_db'
    user_db = []
    with open(user_file, 'r') as db:
        for line in db:
            user_db.append(line)
    return user_db


@outer
def user_info(user_db, USER_LEVEL, USER_NAME):
    print('-'.center(50, '-'))
    print('用户名 密码 手机 邮箱 级别')
    if USER_LEVEL == 2:
        for line in user_db:
            if USER_NAME == line.split('|')[0]:
                print(line.replace('|', '  '))


def change_pwd():
    pass


def user_add():
    pass


def user_del():
    pass


def user_levelup():
    pass


def user_search():
    pass


def main():
    print('-'.center(50, '-'))
    print('用户管理后台：\n1、查看用户信息\n2、修改密码\n3、添加用户\n4、删除用户\n5、用户提权\n6、搜索用户')
    print('-'.center(50, '-'))
    user_db = db_read()
    #print(user_db)
    #print(user_db[0].split('|'))
    while True:
        user_select = input('输入编号： ')
        if user_select == '1':
            user_info(user_db, USER_LEVEL, USER_NAME)
        if user_select == '2':
            change_pwd()
        if user_select == '3':
            user_add()
        if user_select == '4':
            user_del()
        if user_select == '5':
            user_levelup()
        if user_select == '6':
            user_search()
main()