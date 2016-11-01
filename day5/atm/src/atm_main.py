# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import re
import time
import json
from src import log
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
                if user_dict['status'] == 1:
                    print('\033[31;0m\033[0m该信用卡被冻结！')
                    time.sleep(2)
                    continue
                else:
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
    if CURRENT_USER_INFO['status'] == 0:
        print('卡号：%(card_num)s\n当前状态：\033[32;0m正常\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)
    if CURRENT_USER_INFO['status'] == 1:
        print('卡号：%(card_num)s\n当前状态：\033[31;0m冻结\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)


def write_log(message):
    struct_time = time.localtime()
    log_obj = log.get_logger(CURRENT_USER_INFO['card_num'], struct_time)
    log_obj.info(message)


def dump_current_user_info():
    json.dump(CURRENT_USER_INFO, open(os.path.join(setting.USER_DIR, CURRENT_USER_INFO['card_num'], 'user_base.json'), 'w'))


def write_repay(repay_num):
    write_log('repay ￥+%d save: %d balance: %d' % (
        repay_num, CURRENT_USER_INFO['save'], CURRENT_USER_INFO['balance']))
    dump_current_user_info()
    print('还款 \033[31;0m%d\033[0m 成功！' % repay_num)
    time.sleep(2)


def account_info():
    account_show()
    qiut = input('[Enter] 返回...')


def account_repay():
    pass
    account_show()
    while True:
        repay_num = input('输入还款金额： ')
        if re.match('^[0-9.]+$', repay_num):
            repay_num = float(repay_num)
            if CURRENT_USER_INFO['balance'] < CURRENT_USER_INFO['card_limit']:
                tmp = CURRENT_USER_INFO['card_limit'] - CURRENT_USER_INFO['balance']
                if repay_num <= tmp:
                    CURRENT_USER_INFO['balance'] += repay_num

                    write_repay(repay_num)
                    break
                else:
                    CURRENT_USER_INFO['balance'] = CURRENT_USER_INFO['card_limit']
                    CURRENT_USER_INFO['save'] = (repay_num - tmp)

                    write_repay(repay_num)
                    break
            else:
                CURRENT_USER_INFO['save'] += repay_num
                write_repay(repay_num)
                break
        else:
            print('输入错误...')
            continue


def withdraw_count(amount):
    if re.match('^[0-9.]+$', amount):
        amount = int(amount)
        if amount <= CURRENT_USER_INFO['save']:
            CURRENT_USER_INFO['save'] -= amount

            write_log('withdraw -￥%d save: %d balance: %d' % (
                amount, CURRENT_USER_INFO['save'], CURRENT_USER_INFO['balance']))
            dump_current_user_info()
            return True, amount
        else:
            tmp = amount - CURRENT_USER_INFO['save']
            if CURRENT_USER_INFO['balance'] >= (tmp + tmp * 0.05):
                CURRENT_USER_INFO['save'] = 0
                CURRENT_USER_INFO['balance'] -= tmp
                CURRENT_USER_INFO['balance'] -= tmp * 0.05

                write_log('withdraw -￥%d save: %d balance: %d' % (
                    amount, CURRENT_USER_INFO['save'], CURRENT_USER_INFO['balance']))
                dump_current_user_info()
                return True, amount
            else:
                print('余额不足 操作失败！')
    else:
        print('输入有误...')


def account_withdraw():
        account_show()
        amount = input('输入取款金额： ')
        ret, amount = withdraw_count(amount)
        if ret:
            print('取款 \033[031;0m%d\033[0m 成功！' % amount)
            time.sleep(2)


def account_transfer():
    while True:
        tans_card = input('转入账号： ')
        if not os.path.exists(os.path.join(setting.USER_DIR, tans_card)):
            print('账号不存在')
            time.sleep(1)
            break
        else:
            tans_card_dic = json.load(open(os.path.join(setting.USER_DIR, tans_card, 'user_base.json'), 'r'))
            print('要转入的账号用户名为：\033[031;0m%s\033[0m' % tans_card_dic['username'])
            user_commit = input('确认？ y|n')

            if user_commit == 'y':
                account_show()
                tans_num = input('输入转账金额： ')
                ret, tans_num = withdraw_count(tans_num)
                if ret:
                    tans_card_dic['save'] += tans_num
                    json.dump(tans_card_dic,
                              open(os.path.join(setting.USER_DIR, tans_card_dic['card_num'], 'user_base.json'),
                                   'w'))
                    print('转账 \033[031;0m%s\033[0m 成功！ ' % tans_num)
                    time.sleep(2)
                    break
            else:
                break


def account_bill():
    pass


def logout():
    print('%s 安全退出成功...' % CURRENT_USER_INFO['username'])
    time.sleep(2)
    os.system("cls")
    run()


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