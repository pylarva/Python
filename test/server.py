# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import math
import sys
import time
import re
import random
import time
import queue
import socket
import select

ip_port = ('127.0.0.1', 8001)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

inputs = [sk, ]
outputs = []
message = {}

while True:
    r_list, w_list, e_list, = select.select(inputs, outputs, [])

    for r in r_list:
        if r == sk:
            conn, addr = r.accept()
            conn.sendall(bytes('hello...', encoding='utf-8'))
            inputs.append(conn)
            message[conn] = queue.Queue()
        else:
            try:
                ret = r.recv(1024)
                if not ret:
                    raise Exception('断开连接...')
                else:
                    outputs.append(r)
                    message[r].put(ret)
            except Exception as e:
                inputs.remove(r)
                del message[r]

    for w in w_list:
        try:
            msg = message[w].get_nowait()
        except queue.Empty:
            print('The queue is empty...')
            inputs.remove(w)
        else:
            print(msg.decode())
            while True:
                inp = input('>>>:')
                if not inp: continue
                w.send(bytes(inp, encoding='utf-8'))
                break
            outputs.remove(w)





