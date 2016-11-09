# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import hashlib

def decryption_pwd(pwd):
    obj = hashlib.md5(bytes('sdfhiwe676sdf', encoding='utf-8'))
    obj.update(bytes(pwd, encoding='utf-8'))
    r = obj.hexdigest()
    return r
    # print(r)

# decryption_pwd('123')