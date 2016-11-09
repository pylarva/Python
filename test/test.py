# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import configparser

config = configparser.ConfigParser()
config.read('db', encoding='utf-8')
ret = config.sections()
ret1 = config.get('teacher1', 'pw')

ret2 = config.get('student1', 'pw')
ret3 = config.has_option('student2', 'pw')

print(ret)
print(ret1)
print(ret2)
print(ret3)
