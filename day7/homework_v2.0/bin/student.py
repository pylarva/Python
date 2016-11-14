# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.join(__file__)))
sys.path.append(base_dir)

from src import student

"""
学生登陆入口 测试账号 li / 123
"""
if __name__ == '__main__':
    student.main()