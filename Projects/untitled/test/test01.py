# !/usr/bin/env python
# -*- coding:utf-8 -*-
import os

file = '/opt/live.conf'

if os.path.exists(file):
    f = open(file, 'r+')
    r = f.read()
    pos = r.find("still_range")
    if pos != -1:
        content = '6666'
        f.write(content)
        f.close()