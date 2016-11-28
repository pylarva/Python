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
        # 解决粘包问题
        ready_tag = s.recv(1024)
        if str(ready_tag, encoding='utf8').startswith('ready'):
            msg_size = int(str(ready_tag, encoding='utf8').split('|')[-1])
            s.send(bytes('start', encoding='utf8'))

            recv_msg = b''
            recv_size = 0
            while recv_size < msg_size:
                recv_data = s.recv(1024)
                recv_msg += recv_data
                recv_size += len(recv_data)
                print('MSG_SIZE:{} (RECV:{})'.format(msg_size, recv_size))

            recv_data = str(recv_msg, encoding='utf-8')
            print(recv_data)
        else:
            print(str(ready_tag, encoding='utf8'))

# 挂电话
s.close()