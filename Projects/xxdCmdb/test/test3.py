# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re

import time
from multiprocessing import Pool

a = 'abc!'

v = re.search('[>()$%&!]', a)
if v:
    print(v)