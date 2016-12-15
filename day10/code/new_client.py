# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys
import time
import json
import math
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
    """
    上传文件方法
    :param sk:
    :param inp:
    :return:
    """
    sk.sendall(bytes(inp, encoding='utf-8'))

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
            progressbar(send_size, file_size)

        f.close()
        print('上传文件 \033[31;0m{}\033[0m 成功!'.format(file_name))


def file_pull(sk, inp):
    """
    下载文件方法
    :param sk:
    :param inp:
    :return:
    """
    file_name = inp.split()[-1]
    sk.sendall(bytes(inp, encoding='utf-8'))

    data = sk.recv(1024)
    data = json.loads(data.decode())

    file_size = data['file_size']

    server_response = {'status': 200}
    sk.send(bytes(json.dumps(server_response), encoding='utf-8'))

    s = time.strftime('%Y-%m-%d %H-%M')
    new_name = '{}_{}'.format(s, file_name)
    f = open(os.path.join(base_dir, 'pull', new_name), 'ab+')
    # f = open(os.path.join(base_dir, 'pull', '%s_%s' % roll, file_name), 'ab+')

    recv_size = 0
    while recv_size < file_size:
        data = sk.recv(1024)
        f.write(data)
        recv_size += len(data)
        progressbar(recv_size, file_size)
    print('下载文件 \033[31;0m{}\033[0m 成功!'.format(new_name))
    f.close()


ip_port = ('127.0.0.1', 8000)
sk = socket.socket()
sk.connect(ip_port)
sk.settimeout(5)

data = sk.recv(1024)
data = data.decode()
print('Receive: %s' % data)
print('''\033[32;0m
            上传文件 put + 文件名
            下载文件 pull + 文件名
            \033[0m''')

while True:

    inp = input(">>>:")
    if len(inp) == 0: continue
    if inp.split()[0] == 'put':
        file_put(sk, inp)
        continue
    if inp.split()[0] == 'pull':
        file_pull(sk, inp)
        continue
    if inp == 'q':
        break
    else:
        sk.send(bytes(inp, encoding='utf-8'))
        ret = sk.recv(1024)
        print(ret.decode())

sk.close()