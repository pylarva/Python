# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src import admin_main

"""
信用卡后台管理入口
"""
if __name__ == '__main__':
    admin_main.show()