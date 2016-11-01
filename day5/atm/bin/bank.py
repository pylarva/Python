# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os, sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src import atm_bank

"""
银行结算入口：每月22号出账单 每月10号为还款日 过期未还 按欠款总额 万分之五每日计息
"""
if __name__ == '__main__':
    atm_bank.main()