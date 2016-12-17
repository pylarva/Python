# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket

ip_port = ('127.0.0.1', 8001)

sk = socket.socket()
sk.connect(ip_port)


while True:
    data = sk.recv(1024)
    print(data.decode())
    inp = input('>>>:')
    sk.send(bytes(inp, encoding='utf-8'))
