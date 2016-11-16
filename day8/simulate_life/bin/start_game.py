# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.join(__file__)))
sys.path.append(base_dir)

from src import game

if __name__ == '__main__':
    game.main()