# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src import db_conn, views

"""
堡垒机管理员一键初始化数据库函数
"""
if __name__ == '__main__':
    try:
        # 删除表
        db_conn.drop_db()
        # 新建表
        db_conn.init_db()
        # 添加数据
        views.run()
        print('初始化数据库成功...')
        print('新建数据成功...')
    except Exception:
        print('YML配置文件中有错误...')