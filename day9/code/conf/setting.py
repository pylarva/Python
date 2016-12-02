# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

USER_DB = os.path.join(base_dir, 'db', 'user_db')
USER_HOME = os.path.join(base_dir, 'home')