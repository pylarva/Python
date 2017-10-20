#!/usr/bin/env python
# coding: utf-8

import os
import re

print(os.popen('who', 'r').read())
with os.popen('who', 'r') as f:
    for line in f:
        print(re.split(r'\s\s+', line.strip()))

