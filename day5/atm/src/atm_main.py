# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import time
import json
from conf import setting


CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}


def login():
    """
    用户登陆
    :return:
    """
    while True:
        print('用户登陆'.center(40, '-'))
        card_num = input('输入信用卡卡号： ')
        password = input('输入信用卡密码: ')

        if not os.path.exists(os.path.join(setting.USER_DIR, card_num)):
            print('用户不存在')
        else:
            user_dict = json.load(open(os.path.join(setting.USER_DIR, card_num, 'user_base.json'), 'r'))
            if card_num == user_dict['card_num'] and password == user_dict['password']:
                # CURRENT_USER_INFO['is_authenticated'] = True
                # CURRENT_USER_INFO['current_user'] = username
                user_base = json.load(open(os.path.join(setting.USER_DIR, card_num, "user_base.json")))
                CURRENT_USER_INFO.update(user_base)
                print('欢迎 \033[31;0m%s\033[0m ,登陆成功...' % user_base['username'])
                time.sleep(1)
                return True
            else:
                print('用户名或者密码错误...')


def main():
    show_menu = '''
    ----------- 信用卡中心 -----------
    \033[32;0m1.  信用卡查询
    2.  信用卡还款
    3.  信用卡取款
    4.  信用卡转账
    5.  账单打印
    6、 注销
    \033[0m'''
    print(show_menu)
    # show_dic = {
    #     '1': card_,
    #     '2': user_del,
    #     '3': user_freeze,
    #     '4': user_unfreeze,
    #     '5': user_exit
    # }


def run():
    ret = login()
    if ret:
        print(CURRENT_USER_INFO)
        main()