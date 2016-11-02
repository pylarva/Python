# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys
import os

print(__file__)  # 拿到路径名
print(os.path.abspath(__file__))  # 拿到绝对路径
print(os.path.dirname(os.path.abspath(__file__)))  # 上一级目录
