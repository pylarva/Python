# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import hashlib


def decryption_pwd(pwd):
    """
    用户密码加密
    :param pwd:
    :return:
    """
    obj = hashlib.md5(bytes('sdfsd234fddf', encoding='utf-8'))
    obj.update(bytes(pwd, encoding='utf-8'))
    ret = obj.hexdigest()

    return ret