# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import yaml

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# f = os.path.join(base_dir, 'db', 'new_host.yml')

f = open('new_host.yml')
file = yaml.load(f)
print(file)