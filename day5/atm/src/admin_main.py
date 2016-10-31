# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time, sys, os, json, shutil
from conf import setting
from lib import encryption

CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}


def outer(func):
    def inner():
        if not CURRENT_USER_INFO['is_authenticated']:
            print('请先登陆...')
            login()
        func()
    return inner


def login():
    """
    管理员登陆
    :return:
    """
    while True:
        username = input('管理员用户名： ')
        password = input('管理员密码: ')

        if not os.path.exists(os.path.join(setting.ADMIN_DIR, username)):
            print('用户名不存在')
        else:
            user_dict = json.load(open(os.path.join(setting.ADMIN_DIR, username), 'r'))
            if username == user_dict['username'] and encryption.md5(password) == user_dict['password']:
                CURRENT_USER_INFO['is_authenticated'] = True
                CURRENT_USER_INFO['current_user'] = username
                print('欢迎 %s ,登陆成功...' % username)
                return True
            else:
                print('用户名或者密码错误...')


@outer
def user_create():
    while True:
        username = input('请输入新卡用户名： ')
        password = input('请输入新卡密码： ')
        card_num = input('请输入新卡卡号： ')
        card_limit = input('请输入新卡额度： ')
        if not card_limit.isdigit():
            print('额度必须为数字...')
            break
        card_limit = int(card_limit)
        print('用户名：%s\n密码：%s\n卡号：%s\n额度：%d' % (username, password, card_num, card_limit))
        user_commit = input('是否创建？ y|n')
        if all([username, password, card_limit, card_num]) and user_commit == 'y':
            user_info = {
                'username': username,
                'password': password,
                'card_num': card_num,
                'card_limit': card_limit,
                'balance': card_limit,
                'status': 0,
                'debt': []
            }
            if not os.path.exists(os.path.join(setting.USER_DIR, card_num)):
                os.makedirs(os.path.join(setting.USER_DIR, card_num, 'record'))
                json.dump(user_info, open(os.path.join(setting.USER_DIR, card_num, 'user_base.json'), 'w'))
                print('卡号 %s 创建成功!' % card_num)
                time.sleep(2)
                break
            else:
                print('卡号已经存在')
                time.sleep(1)
                break
        else:
            break


@outer
def user_del():
    while True:
        card_num = input('输入要删除的卡号： ')
        if card_num:
            if os.path.exists(os.path.join(setting.USER_DIR, card_num)):
                shutil.rmtree(os.path.join(setting.USER_DIR, card_num))
                print('删除卡号 %s 成功!' % card_num)
                time.sleep(2)
                break
            else:
                print('卡号不存在')
                break
        else:
            continue


@outer
def user_freeze():
    card_num = input('要冻结的卡号： ')

    if os.path.exists(os.path.join(setting.USER_DIR, card_num)):
        user_dic = json.load(open(os.path.join(setting.USER_DIR, card_num, 'user_base.json')))
        user_dic['status'] = "1"
        json.dump(user_dic, open(os.path.join(setting.USER_DIR, card_num, 'user_base.json'), 'w'))
        print('卡号 \033[31;0m%s\033[0m 冻结成功！' % card_num)
        time.sleep(2)
    else:
        print('卡号不存在...')


@outer
def user_unfreeze():
    card_num = input('要解冻的卡号： ')

    if os.path.exists(os.path.join(setting.USER_DIR, card_num)):
        user_dic = json.load(open(os.path.join(setting.USER_DIR, card_num, 'user_base.json')))
        user_dic['status'] = "0"
        json.dump(user_dic, open(os.path.join(setting.USER_DIR, card_num, 'user_base.json'), 'w'))
        print('卡号 \033[31;0m%s\033[0m 解冻成功！' % card_num)
        time.sleep(2)
    else:
        print('卡号不存在...')


def user_exit():
    print('退出成功！')
    time.sleep(1)
    sys.exit()


def show():
    show_menu = '''
    ----------- 信用卡管理 -----------
    \033[32;0m1.  信用卡开户
    2.  信用卡删除
    3.  信用卡冻结
    4.  信用卡解冻
    5.  退出
    \033[0m'''
    show_dic = {
        '1': user_create,
        '2': user_del,
        '3': user_freeze,
        '4': user_unfreeze,
        '5': user_exit
    }
    while True:
        print(show_menu)
        user_select = input('输入编号>>: ')
        if user_select in show_dic:
            show_dic[user_select]()
        else:
            print('输入错误...')


