# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 获取查询数据

import pymysql

conn = pymysql.connect(host='10.0.0.111', port=3306, user='root', passwd='123', db='t1')

cursor = conn.cursor()

# 字典
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

cursor.execute("select * from hosts")

# 获取第一行数据
# row_1 = cursor.fetchone()

# 获取前n行数据
# row_2 = cursor.fetchmany(3)

# 获取所有数据
row_3 = cursor.fetchall()
print(row_3)

conn.commit()
cursor.close()
conn.close()