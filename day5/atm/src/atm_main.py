# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import re
import time
import json
import sys
from src import log
from conf import setting

# 全局变量判断用户是否登陆正常
CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}


def login():
    """
    用户登陆：不允许冻结用户登陆
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
    """
    打印当前信用卡状态及余额信息
    :return:
    """
    print('  %s  '.center(40, '-') % CURRENT_USER_INFO['username'])
    if CURRENT_USER_INFO['status'] == 0:
        print('卡号：%(card_num)s\n当前状态：\033[32;0m正常\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)
    if CURRENT_USER_INFO['status'] == 1:
        print('卡号：%(card_num)s\n当前状态：\033[31;0m冻结\033[0m\n最高额度：%(card_limit)d\n当月剩余额度：%(balance)d\n'
              '储蓄余额： %(save)s ' % CURRENT_USER_INFO)


def write_log(message):
    """
    调用 logging 日志模块生成文件记录
    :param message:
    :return:
    """
    struct_time = time.localtime()
    log_obj = log.get_logger(CURRENT_USER_INFO['card_num'], struct_time)
    log_obj.info(message)


def dump_current_user_info():
    """
    更新用户数据库信息
    :return:
    """
    json.dump(CURRENT_USER_INFO, open(os.path.join(setting.USER_DIR, CURRENT_USER_INFO['card_num'], 'user_base.json'), 'w'))


def write_repay(repay_num):
    """
    还款成功 则记录日志并更新用户数据文件
    :param repay_num:
    :return:
    """
    write_log('repay ￥+%d save: %d balance: %d' % (
        repay_num, CURRENT_USER_INFO['save'], CURRENT_USER_INFO['balance']))
    dump_current_user_info()
    print('还款 \033[31;0m%d\033[0m 成功！' % repay_num)
    time.sleep(2)


def account_info():
    """
    信用卡信息查询
    :return:
    """
    account_show()
    qiut = input('[Enter] 返回...')


def account_repay():
    """
    还款 先偿还欠款记录 多余存入save储蓄
    :return:
    """
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
    """
    取款判断：储蓄账户取出不收取手续费 信用卡取出收取 5% 手续费
    :param amount:
    :return:
    """
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
    """
    取款入口
    :return:
    """
    account_show()
    amount = input('输入取款金额： ')
    ret, amount = withdraw_count(amount)
    if ret:
        print('取款 \033[031;0m%d\033[0m 成功！' % amount)
        time.sleep(2)


def account_transfer():
    """
    转账：确认转入用户账号后 转入对方储蓄账户
    :return:
    """
    while True:
        tans_card = input('转入账号： ')
        if not os.path.exists(os.path.join(setting.USER_DIR, tans_card)):
            print('账号不存在')
            time.sleep(1)
            break
        else:
            tans_card_dic = json.load(open(os.path.join(setting.USER_DIR, tans_card, 'user_base.json'), 'r'))
            print('要转入的账号用户名为：\033[031;0m%s\033[0m' % tans_card_dic['username'])
            user_commit = input('确认？ Y|N')

            if user_commit.upper() == 'Y':
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
    """
    账单打印
    :return:
    """
    struct_time = time.localtime()
    if struct_time.tm_mday < 23:
        file_name = 'Record-%s-%s-%d' % (struct_time.tm_year, struct_time.tm_mon, 22)
    else:
        file_name = 'Record-%s-%s-%d' % (struct_time.tm_year, struct_time.tm_mon+1, 22)
    # 一个 r' 转义问题折腾我5个小时...
    file_name = os.path.join("r'", setting.USER_DIR, CURRENT_USER_INFO['card_num'], 'record', file_name)
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            print(line)
    pause = input('[Enter]继续...')


def logout():
    """
    退出
    :return:
    """
    print('%s 安全退出成功...' % CURRENT_USER_INFO['username'])
    time.sleep(2)
    os.system("cls")
    run()


def main():
    """
    功能菜单打印
    :return:
    """
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


def shopping_withdraw(SHOPPING_CAR, sum_pay):
    """
    购物商城支付接口
    :param SHOPPING_CAR:
    :param sum_pay:
    :return:
    """
    ret = login()
    if ret:
        account_show()
        user_commit = input('确认支付? Y|N ')
        if user_commit.upper() == 'Y':
            if sum_pay > CURRENT_USER_INFO['balance']:
                print('余额不足 支付失败!')
                time.sleep(2)
            else:
                CURRENT_USER_INFO['balance'] -= sum_pay
                dump_current_user_info()
                write_log('购物消费：%d ' % sum_pay)
                for item in SHOPPING_CAR:
                    write_log('商品：%(name)s 数量：%(nums)d 合计：%(sum)d' % item)
                print('支付 \033[031;0m%d\033[0m 成功！' % sum_pay)
                time.sleep(2)