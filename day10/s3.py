# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket

sk = socket.socket()
sk.bind(('127.0.0.1', 9999,))
sk.listen(5)
while True:
    conn, address = sk.accept()
    conn.sendall(bytes('hello', encoding='utf-8'))
    while True:
        try:
            ret = conn.recv(1024)
            if len(ret) == 0: break
            if ret.decode() == 'q':
                break
            conn.send(ret)
        except Exception:
            break