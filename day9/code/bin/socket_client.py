# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import re
import sys
import socket

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


def connect_server():

    while True:
        ip_port = input('请输入服务端地址： ')
        if not re.match('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}:\d+$', ip_port):
            print('地址有误...')
            continue
        else:
            ip_port = (ip_port.split(':')[0], int(ip_port.split(':')[1]))
            return ip_port


def main():

    print('  \033[32;0mFTP客户端程序\033[0m  '.center(50, '-'))

    while True:
        # ip_port = connect_server()
        ip_port = ('10.0.0.150', 8000)
        s = socket.socket()
        s.settimeout(2)
        ret = s.connect_ex(ip_port)
        if ret != 0:
            print('服务器：\033[31;0m{}\033[0m 端口：\033[31;0m{}\033[0m 连接失败...'.format(ip_port[0], ip_port[1]))
            print('请检查IP和端口并重试!\n')
            continue

        welcome_msg = s.recv(1024)
        print(welcome_msg.decode())

        while True:
            send_data = input('>>: ').strip()
            if len(send_data) == 0: continue
            s.send(bytes(send_data, encoding='utf-8'))

            recv_data = s.recv(1024)
            print(recv_data.decode())

if __name__ == '__main__':
    main()
