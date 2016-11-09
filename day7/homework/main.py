# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import configparser
from decryption import decryption_pwd


def login():
    config = configparser.ConfigParser()
    config.read('adm_db', encoding='utf-8')

    while True:
        user_name = input('请输入用户名： ')
        user_password = input('请输入密码： ')
        if config.has_option(user_name, 'password'):
            user_password = decryption_pwd(user_password)
            if config.get(user_name, 'password') == user_password:
                return True
            else:
                print('密码错误...')
        else:
            print('用户名不存在...')
            continue


def admin():
    ret = login()
    if ret:
        pass


def student():
    pass


def register():
    config = configparser.ConfigParser()
    config.read('db', encoding='utf-8')
    print('-----------  学生注册  -----------')

    while True:
        user_name = input('请输入新用户名： ')
        user_pwd = input('请出入用户密码： ')

        if user_name and user_pwd:
             if not config.has_section(user_name):
                 config.add_section(user_name)
                 user_pwd = decryption_pwd(user_pwd)
                 config.set(user_name, 'password', user_pwd)
                 config.write(open('db', 'w'))
                 print('注册成功！')
                 return
             else:
                 print('用户已经存在...')
                 continue
        else:
            print('用户名或密码不能为空...')
            continue


def out():
    pass


def main():
    show_menu = '''
    \033[35;0m-------------- 选课中心 ---------------\033[0m
    \033[32;0m1、管理登陆
    2、学生登陆
    3、学生注册
    4、退出
    \033[0m'''
    print(show_menu)
    show_dic = {
        '1': admin,
        '2': student,
        '3': register,
        '4': out
    }
    while True:
        user_select = input('输入编号 >> ')
        if user_select in show_dic:
            show_dic[user_select]()
        else:
            continue

if __name__ == '__main__':
    main()