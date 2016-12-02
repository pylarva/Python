# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import hashlib


def decryption_pwd(pwd):

    obj = hashlib.md5(bytes('sdfsd234fddf', encoding='utf-8'))
    obj.update(bytes(pwd, encoding='utf-8'))
    ret = obj.hexdigest()

    return ret

# ret = decryption_pwd('123')
# print(ret)