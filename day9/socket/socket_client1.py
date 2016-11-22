# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com
import socket
ip_port = ('127.0.0.1', 9999)

# 买手机
s = socket.socket()

# 拨号
s.connect(ip_port)

# 发消息
while True:
    send_data = input('>>: ').strip()
    if not send_data:
        continue
    else:
        s.send(bytes(send_data, encoding='utf-8'))
        if send_data == 'exit':
            break
        # 收消息
        recv_data = s.recv(1024)
        recv_data = str(recv_data, encoding='utf-8')

        print(recv_data)

# 挂电话
s.close()