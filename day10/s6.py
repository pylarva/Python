# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket

# 创建一个socket实例
sk = socket.socket()
sk.connect(('127.0.0.1', 9999))

# 连接成功后打印服务端发送的消息
recv_bytes = sk.recv(1024)
recv_str = str(recv_bytes, encoding='utf-8')
print(recv_str)

# 开始循环交互发送数据
while True:
    inp = input(">>>:")
    sk.sendall(bytes(inp, encoding='utf-8'))
    ret = sk.recv(1024)
    print(ret)
sk.close()