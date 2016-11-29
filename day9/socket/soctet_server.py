# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import socket
import subprocess

# 以元组形式定义一个IP地址个一个端口号
ip_port = ('127.0.0.1', 9999)

# 创建socket对象
s = socket.socket()
# 绑定上面创建的IP地址和端口
s.bind(ip_port)
# 开始监听
s.listen(5)

# 与客户端建立连接并开始会话
while True:
    conn, addr = s.accept()  # conn 表示客户端与服务端连接的专有线路

    while True:
        try:
            recv_data = conn.recv(1024)  # 接受客户端发来的消息
            if str(recv_data, encoding='utf-8') == 'exit':
                break
            p = subprocess.Popen(str(recv_data, encoding='utf-8'), shell=True, stdout=subprocess.PIPE)
            ret = p.stdout.read()

            if len(ret) == 0:
                send_data = 'cmd error...'
                ret = bytes(send_data, encoding='utf-8')
                conn.send(ret)  # 发送消息
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

    conn.close()