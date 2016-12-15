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


def file_md5(file_path):
    """
    文件MD5校验
    :param file_path:
    :return:
    """
    f = open(file_path, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    md5_hash = md5obj.hexdigest()
    f.close()
    return str(md5_hash).upper()