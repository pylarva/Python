# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import re
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
        print('  用户登陆  '.center(40, '-'))
        card_num = input('输入信用卡卡号： ')
        password = input('输入信用卡密码: ')

        if not os.path.exists(os.path.join(setting.USER_DIR, card_num)):
            print('用户不存在')
        else:
            user_dict = json.load(open(os.path.join(setting.USER_DIR, card_num, 'user_base.json'), 'r'))
            if card_num == user_dict['card_num'] and password == user_dict['password']:
                user_base = json.load(open(os.path.join(setting.USER_DIR, card_num, "user_base.json")))
                CURRENT_USER_INFO['is_authenticated'] = True
                CURRENT_USER_INFO['current_user'] = user_base['username']
                CURRENT_USER_INFO.update(user_base)
                print('欢迎 \033[31;0m%s\033[0m ,登陆成功...' % user_base['username'])
                time.sleep(1)
                return True
            else:
                print('用户名或者密码错误...')


def account_show():
    print('  %s  '.center(40, '-') % CURRENT_USER_INFO['username'])
    if CURRENT_USER_INFO['status'] == '0':
        print('卡号：%(card_num)s\n当前状态：\033[32;0m正常\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)
    if CURRENT_USER_INFO['status'] == '1':
        print('卡号：%(card_num)s\n当前状态：\033[31;0m冻结\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)


def account_info():
    account_show()
    qiut = input('[Enter] 返回...')


def account_repay():
    account_show()
    while True:
        repay_num = input('输入还款金额： ')
        if re.match('^[0-9.]+$', repay_num):
            repay_num = float(repay_num)
            if CURRENT_USER_INFO['balance'] < CURRENT_USER_INFO['card_limit']:


        else:
            print('输入错误...')
            continue


def account_withdraw():
    pass


def account_transfer():
    pass


def account_bill():
    pass


def logout():
    pass


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
    show_dic = {
        '1': account_info,
        '2': account_repay,
        '3': account_withdraw,
        '4': account_transfer,
        '5': account_bill,
        '6': logout
    }
    while True:
        print(show_menu)
        user_select = input('输入编号>>: ')
        if user_select in show_dic:
            show_dic[user_select]()
        else:
            print('输入错误...')


def run():
    ret = login()
    if ret:
        main()