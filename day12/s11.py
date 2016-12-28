# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# sqlalchemy 操作数据库

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/t1", max_overflow=5)


# 执行SQL
cur = engine.execute(
    "INSERT INTO hosts (host, color_id) VALUES ('1.1.1.22', 3)"
)

# 新插入行自增ID
# cur.lastrowid

# 执行SQL
# cur = engine.execute(
#     "INSERT INTO hosts (host, color_id) VALUES(%s, %s)",[('1.1.1.22', 3),('1.1.1.221', 3),]
# )

# 执行SQL
# cur = engine.execute(
#     "INSERT INTO hosts (host, color_id) VALUES (%(host)s, %(color_id)s)",
#     host='1.1.1.99', color_id=3
# )

# 执行SQL
# cur = engine.execute('select * from hosts')

# 获取第一行数据
# cur.fetchone()
# 获取第n行数据
# cur.fetchmany(3)
# 获取所有数据
# row = cur.fetchall()
# print(row)