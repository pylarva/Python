# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.join(__file__)))
sys.path.append(base_dir)

from src import admin

"""
管理员登陆入口： 测试账号:admin 密码:admin
"""
if __name__ == '__main__':
    # admin.login()
    admin.main()