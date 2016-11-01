# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
import os
import json

from conf import setting


def main():
    struct_time = time.localtime()
    user_list = os.listdir(setting.USER_DIR)

    for user in user_list:
        user_dic = json.load(open(os.path.join(setting.USER_DIR, user, 'user_base.json'), 'r'))
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