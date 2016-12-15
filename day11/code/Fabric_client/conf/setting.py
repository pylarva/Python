# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

HOST_LIST = os.path.join(base_dir, 'db', 'host_list')
USER_HOME = os.path.join(base_dir, 'home')

# master地址
master_address = '10.0.0.1'