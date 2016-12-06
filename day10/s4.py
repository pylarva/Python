# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket

sk = socket.socket()
sk.connect(('127.0.0.1', 9999))

recv_bytes = sk.recv(1024)
recv_str = str(recv_bytes, encoding='utf-8')
print(recv_str)

while True:
    inp = input(">>>:")
    sk.sendall(bytes(inp, encoding='utf-8'))
    print(str(sk.recv(1024), encoding='utf-8'))
    if inp == 'q':
        break
