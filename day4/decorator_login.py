#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time

LOGIN_USER = {'is_login': False}
USER_LEVEL = ''
USER_NAME = ''


def login(user_db):
    while True:
        global USER_NAME
        global LOGIN_USER
        global USER_LEVEL
        USER_NAME = input('请先登陆，用户名： ')
        user_pwd = input('请出入密码: ')
        for line in user_db:
            if USER_NAME in line:
                if user_pwd == line.split('|')[1]:
                    print('%s,登陆成功.'% USER_NAME)
                    LOGIN_USER = {'is_login': True}
                    USER_LEVEL = int(line.split('|')[4])
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
    if USER_LEVEL == 1:
        for line in user_db:
            if USER_NAME == line.split('|')[0]:
                print(line.replace('|', '  '))
    if USER_LEVEL == 2:
        for line in user_db:
            print(line.replace('|', '  '))


@outer
def change_pwd(user_db, USER_LEVEL, USER_NAME):
    flag = True
    while flag:
        change_user = input('请输入要修改的用户名： ')
        new_pwd_first = input('请输入新密码： ')
        new_pwd_second = input('请再次输入新密码： ')
        user_exit = False
        if change_user != USER_NAME and USER_LEVEL != 2:
            print('只有管理员权限才能修改...')
            time.sleep(1)
            flag = False
            continue
        if new_pwd_first == new_pwd_second:
            user_file = 'user_db'
            for line in user_db:
                if change_user in line.split('|'):
                    user_exit = True
                    break
            if user_exit:
                with open(user_file, 'w+') as db:
                    for line in user_db:
                        if change_user == USER_NAME and change_user == line.split('|')[0]:
                            line = line.split('|')
                            line[1] = new_pwd_first
                            line = '|'.join(line)
                            db.write(line)
                            continue
                        if change_user != USER_NAME and USER_LEVEL == 2 and change_user == line.split('|')[0]:
                            line = line.split('|')
                            line[1] = new_pwd_first
                            line = '|'.join(line)
                            db.write(line)
                            continue
                        else:
                            db.write(line)
                    print('修改成功！')
                    time.sleep(1)
                    flag = False
            else:
                print('用户不存在！')
        if new_pwd_first != new_pwd_second:
            print('两次密码不一样...')
            time.sleep(1)
            continue
        else:
            continue


@outer
def user_add(user_db, USER_LEVEL, USER_NAME):
    if USER_LEVEL == 1:
        print('只有管理员权限才能添加用户！')
        time.sleep(1)
    else:
        while True:
            add_list = []
            user_level = '1'
            user_name = input('添加用户，请输入用户名：')
            if len(user_name) != 0:
                user_pwd = input('请输入用户密码： ')
                if len(user_pwd) !=0:
                    user_phone = input('请输入电话号码： ')
                    user_mail = input('请输入Email： ')
                    user_confirm = input('用户名：%s 密码：%s 电话：%s 邮箱：%s 确认添加吗？【Y|N】 ' %
                                         (user_name, user_pwd, user_phone, user_mail))
                    if user_confirm == 'y' or user_confirm == 'Y':
                        add_list.append(user_name)
                        add_list.append(user_pwd)
                        add_list.append(user_phone)
                        add_list.append(user_mail)
                        add_list.append(user_level)
                        s = '|'.join(add_list)
                        f = open('user_db', 'a+')
                        f.write('\n' + s)
                        f.close()
                        print('添加成功！')
                        time.sleep(1)
                        return
                    else:
                        return
                else:
                    print('密码不能为空..')
            else:
                print('用户名不能为空..')

def user_del():
    pass


def user_levelup():
    pass


def user_search():
    pass


def main():
    while True:
        print('-'.center(50, '-'))
        print('用户管理后台：\n1、查看用户信息\n2、修改密码\n3、添加用户\n4、删除用户\n5、用户提权\n6、搜索用户\n7、退出登陆')
        print('-'.center(50, '-'))
        user_db = db_read()
        user_select = input('输入编号： ')
        if user_select == '1':
            user_info(user_db, USER_LEVEL, USER_NAME)
        if user_select == '2':
            change_pwd(user_db, USER_LEVEL, USER_NAME)
        if user_select == '3':
            user_add(user_db, USER_LEVEL, USER_NAME)
        if user_select == '4':
            user_del()
        if user_select == '5':
            user_levelup()
        if user_select == '6':
            user_search()
        if user_select == '7':
            global LOGIN_USER
            LOGIN_USER = {'is_login': False}
            print('退出成功')
            time.sleep(1)

main()