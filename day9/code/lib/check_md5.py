# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import hashlib


def file_md5(file_path):
    f = open(file_path, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    md5_hash = md5obj.hexdigest()
    f.close()
    return str(md5_hash).upper()