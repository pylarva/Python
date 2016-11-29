# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket
ip_port = ('10.0.0.150', 8009)

s = socket.socket()
s.connect(ip_port)

welcome_msg = s.recv(1024)
print('From Server :', welcome_msg.decode())

while True:
    send_data = input('>>: ').strip()
    if len(send_data) == 0: continue
    s.send(bytes(send_data, encoding='utf-8'))

    recv_data = s.recv(1024)
    print(recv_data.decode())

s.close()