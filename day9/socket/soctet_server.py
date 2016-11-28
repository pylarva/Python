# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket
import subprocess

ip_port = ('127.0.0.1', 9999)

# 买手机
s = socket.socket()

# 买手机卡
s.bind(ip_port)

# 开机
s.listen(5)

# 等待电话
while True:
    conn, addr = s.accept()  # conn 客户端与服务端连接的专有线路

    # 收消息
    while True:
        try:
            recv_data = conn.recv(1024)
            if str(recv_data, encoding='utf-8') == 'exit':
                break
            # 发消息
            p = subprocess.Popen(str(recv_data, encoding='utf-8'), shell=True, stdout=subprocess.PIPE)
            ret = p.stdout.read()

            if len(ret) == 0:
                send_data = 'cmd error...'
                ret = bytes(send_data, encoding='utf-8')
                conn.send(ret)
            else:
                ret = str(ret, encoding='gbk')
                ret = bytes(ret, encoding='utf8')
                read_tag = 'ready|%s' % len(ret)
                conn.send(bytes(read_tag, encoding='utf8'))
                freedback = conn.recv(1024)
                if str(freedback, encoding='utf8') == 'start':
                    conn.send(ret)

        except Exception:
            break

    # 挂电话
    conn.close()