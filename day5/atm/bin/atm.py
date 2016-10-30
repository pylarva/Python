# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

from src import atm_main

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

if __name__ == '__main__':
    atm_main.run()

