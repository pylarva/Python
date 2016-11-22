# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket
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
            send_data = recv_data.upper()
            conn.send(send_data)
        except Exception:
            break

    # 挂电话
    conn.close()