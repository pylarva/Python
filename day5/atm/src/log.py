# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import logging
import os
from conf import setting


def get_logger(card_num, struct_time):
    if struct_time.tm_mday < 23:
        log_name = 'Record-%s-%s-%d' % (struct_time.tm_year, struct_time.tm_mon, 22)
    else:
        log_name = 'Record-%s-%s-%d' % (struct_time.tm_year, struct_time.tm_mon+1, 22)

    logger = logging.Logger('user_logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join(setting.USER_DIR, card_num, 'record', log_name), encoding='utf-8')

    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
