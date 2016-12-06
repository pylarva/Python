# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import shutil
import sys
import subprocess
import configparser
import socketserver
from conf import setting
from lib.decryption import decryption_pwd


def login():
    """
    FTP后台管理员登录
    :return:
    """
    while True:
        user_name = input('请输入管理员账号：')
        user_pwd = input('管理员密码：')
        user_pwd = decryption_pwd(user_pwd)

        config = configparser.ConfigParser()
        config.read(setting.USER_DB, encoding='utf-8')

        if user_name == 'admin' and config.get(user_name, 'password') == user_pwd:
            return True
        else:
            print('用户名或者密码错误...')


def user_add():
    """
    添加用户
    :return:
    """
    while True:
        user_name = input('输入新用户名：')

        config = configparser.ConfigParser()
        config.read(setting.USER_DB, encoding='utf-8')

        if config.has_section(user_name):
            print('用户名已经存在...')
            continue
        config.add_section(user_name)

        user_pwd = input('输入密码：')
        user_disk = input('磁盘配额(MB):')
        if user_pwd and user_disk:
            if not user_disk.isdigit():
                print('磁盘配额为数字...')
                break

            user_pwd = decryption_pwd(user_pwd)
            config.set(user_name, 'password', user_pwd)
            config.set(user_name, 'disk_limit', user_disk)
            if not os.path.exists(os.path.join(setting.USER_HOME, user_name)):
                os.mkdir(os.path.join(setting.USER_HOME, user_name))
            print('新建用户 \033[31;0m{}\033[0m 成功!'.format(user_name))
            config.write(open(setting.USER_DB, 'w'))
            break
        else:
            print('输入不能为空...')


def user_del():
    """
    删除用户
    :return:
    """
    while True:
        user_name = input('输入用户名：')

        config = configparser.ConfigParser()
        config.read(setting.USER_DB, encoding='utf-8')

        if not config.has_section(user_name):
            print('用户名不存在...')
            continue
        user_confirm = input('连同家目录一起删除? [Y|N]')
        if user_confirm.upper() == 'Y':
            config.remove_section(user_name)
            if os.path.exists(os.path.join(setting.USER_HOME, user_name)):
                shutil.rmtree(os.path.join(setting.USER_HOME, user_name))
            print('删除用户 \033[31;0m{}\033[0m 成功!'.format(user_name))
            config.write(open(setting.USER_DB, 'w'))
        break


def user_show():
    """
    展示所有用户
    :return:
    """
    config = configparser.ConfigParser()
    config.read(setting.USER_DB, encoding='utf-8')
    user_list = config.sections()

    for item in user_list:
        if item == 'admin': continue
        disk_limit = config.getfloat(item, 'disk_limit')
        print('用户：{} 总磁盘空间：{}MB'.format(item, disk_limit))


def main():
    """
    后台管理主函数
    :return:
    """
    print('  \033[32;0mFTP用户管理\033[0m  '.center(50, '-'))
    login()
    menu = '''\033[32;0m
          1、添加用户
          2、删除用户
          3、查看用户
          4、退出\033[0m'''

    while True:
        print('  \033[32;0mFTP用户管理\033[0m  '.center(50, '-'))
        print(menu)
        user_inp = input('选择>> ')
        if user_inp == '1':
            user_add()
        elif user_inp == '2':
            user_del()
        elif user_inp == '3':
            user_show()
        elif user_inp == '4':
            sys.exit()
        else:
            continue

