# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
import os
import json

from conf import setting
from src import log


def main():
    struct_time = time.localtime()
    user_list = os.listdir(setting.USER_DIR)

    for user in user_list:
        user_dic = json.load(open(os.path.join(setting.USER_DIR, user, 'user_base.json'), 'r'))
        for item in user_dic['debt']:
            if item['left_debt'] != 0:
                interest = item['total_debt'] * 0.0005
                user_dic['save'] -= (interest + item['left_debt'])
                item['left_debt'] = user_dic['save']
            logger_obj = log.get_logger(user, struct_time)
            logger_obj.info("欠款利息：%.2f (账单日期：%s 总欠款：%.2f 未还款：%.2f)" %
                            (interest, item['date'], item['total_debt'], item['left_debt']))

            json.dump(user_dic, open(os.path.join(setting.USER_DIR, user, 'user_base.json'), 'w'))

        if struct_time.tm_mday == 11 and user_dic['balance'] < user_dic['card_limit']:
            date = time.strftime('%Y-%m-%d')
            dic = {
                'date': date,
                'total_debt': user_dic['card_limit'] - user_dic['balance'],
                'left_debt': user_dic['card_limit'] - user_dic['balance']
            }
            user_dic['debt'].append(dic)
            user_dic['balance'] = user_dic['card_limit']
            json.dump(user_dic, open(os.path.join(setting.USER_DIR, user, 'user_base.json'), 'w'))
            print('ok')