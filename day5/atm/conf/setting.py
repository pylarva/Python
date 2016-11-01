# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


import os
"""
获取当前程序运行的系统路径...
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMIN_DIR = os.path.join(BASE_DIR, 'db', 'admin')

USER_DIR = os.path.join(BASE_DIR, 'db', 'user')
