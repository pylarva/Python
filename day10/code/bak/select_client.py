# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys
import math
import json
import socket

base_dir = os.path.dirname(os.path.abspath(__file__))


def progressbar(cur, total):
    """
    上传文件或者下载文件过程中的进度条显示
    :param cur:
    :param total:
    :return:
    """
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-50s] %s' % ('=' * int(math.floor(cur * 50 / total)), percent))
    sys.stdout.flush()
    if cur == total:
        sys.stdout.write('\n')


def file_put(sk, inp):
    file_name = inp.split()[-1]
    file = os.path.join(base_dir, file_name)
    file_size = os.stat(file).st_size

    msg_data = {
        'action': 'put',
        'file_name': file_name,
        'file_size': file_size,
    }

    sk.sendall(bytes(json.dumps(msg_data), encoding='utf-8'))

    server_confirm_msg = sk.recv(1024)
    confirm_data = json.loads(server_confirm_msg.decode())

    if confirm_data['status'] == 200:
        print('Start sending file \033[31;0m{}\033[0m!'.format(msg_data['file_name']))

        f = open(file, 'rb+')
        buffer_size = 1024
        send_size = 0

        while send_size < file_size:
            if file_size - send_size < buffer_size:
                file_data = f.read(file_size - send_size)
                send_size = file_size
            else:
                file_data = f.read(buffer_size)
                send_size += buffer_size
            sk.send(file_data)
        f.close()
        print(send_size)
        print('上传文件 \033[31;0m{}\033[0m 成功!'.format(file_name))


def file_pull(sk, inp):
    file_name = inp.split()[-1]

    msg_data = {
        'action': 'pull',
        'file_name': file_name,
    }

    sk.sendall(bytes(json.dumps(msg_data), encoding='utf-8'))

    ret = sk.recv(1024)
    ret = json.loads(ret.decode())

    file_size = ret['file_size']

    recv_size = 0
    f = open(os.path.join(base_dir, 'pull', file_name), 'ab+')
    while recv_size < file_size:
        data = sk.recv(1024)
        f.write(data)
        recv_size += len(data)
    f.close()
    print('下载完成....')


def main():
    sk = socket.socket()
    sk.connect(('127.0.0.1', 8000))

    recv_bytes = sk.recv(1024)
    recv_str = str(recv_bytes, encoding='utf-8')
    print(recv_str)

    while True:
        print('''\033[32;0m
        上传文件 put + 文件名
        下载文件 pull + 文件名
        \033[0m''')
        inp = input(">>>:")
        if len(inp) == 0: continue
        if inp.split()[0] == 'put':
            file_put(sk, inp)
        if inp.split()[0] == 'pull':
            file_pull(sk, inp)
        if inp == 'q':
            break

if __name__ == '__main__':
    main()