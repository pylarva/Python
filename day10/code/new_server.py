# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import time
import json
import socket
import select
import threading

base_dir = os.path.dirname(os.path.abspath(__file__))


def task_put(conn , data):
    """
    执行用户上传文件方法
    :param args:
    :param kwargs:
    :return:
    """
    data = conn.recv(1024)
    data = json.loads(data.decode())
    print('---put')
    file_name = data['file_name']
    file_size = data['file_size']

    server_response = {'status': 200}
    conn.send(bytes(json.dumps(server_response), encoding='utf-8'))

    s = time.strftime('%Y-%m-%d %H-%M')
    new_name = '{}_{}'.format(s, file_name)
    f = open(os.path.join(base_dir, 'put', new_name), 'ab+')

    recv_size = 0
    while recv_size < file_size:
        data = conn.recv(4096)
        f.write(data)
        recv_size += len(data)
    print('File recv success!')
    f.close()


def task_pull(conn, data):
    """
    下载文件方法
    :param conn:
    :param data:
    :return:
    """
    file_name = data.split()[-1]
    file = os.path.join(base_dir, file_name)
    file_size = os.stat(file).st_size

    msg_data = {'file_size': file_size}

    conn.sendall(bytes(json.dumps(msg_data), encoding='utf-8'))

    server_confirm_msg = conn.recv(1024)
    confirm_data = json.loads(server_confirm_msg.decode())
    if confirm_data['status'] == 200:

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
            conn.send(file_data)
        f.close()

        print('下载文件 \033[31;0m{}\033[0m 成功!'.format(file_name))


def process(request, client_address):
    """
    每个线程对应一个客户端开始循环会话
    :param request:
    :param client_address:
    :return:
    """
    print(request, client_address)
    conn = request
    conn.sendall(bytes('hello...', encoding='utf-8'))

    while True:
        try:
            data = conn.recv(1024)
            data = data.decode()
            if len(data) == 0: continue
            if data.split()[0] == 'put':
                task_put(conn, data)
                continue
            if data.split()[0] == 'pull':
                task_pull(conn, data)
                continue
            else:
                conn.sendall(bytes(data, encoding='utf-8'))
        except Exception:
            break

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(('127.0.0.1', 8000))
sk.listen(5)

while True:
    r, w, e = select.select([sk, ], [], [], 1)
    if sk in r:
        request, client_address = sk.accept()
        t = threading.Thread(target=process, args=(request, client_address))
        t.daemon = False
        t.start()