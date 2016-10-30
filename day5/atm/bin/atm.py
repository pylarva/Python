# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

from src import main

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

if __name__ == '__main__':
    main.run()

