# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# IO多路复用

import os
import json
import queue
import socket
import select

base_dir = os.path.dirname(os.path.abspath(__file__))

# 创建一个socket对象并绑定IP端口
sk = socket.socket()
sk.bind(('127.0.0.1', 8000,))
sk.listen(5)

# 创建一个新客户端列表 有消息状态改变的客户端列表和一个存储具体消息的字典
inputs = [sk, ]
outputs = []
message = {}
size = {}

while True:

    # 开始监听sk(服务端)对象 如果sk发生变化 表示有客户端来连接 此时rlist里面的值为[sk,]
    # 监听conn对象 如果conn发生变化 表示客户端有消息过来了 此时rlist的值为[客户端, ]
    rlist, wlist, elist, = select.select(inputs, outputs, [], 1)

    # 遍历rlist 查看发生状态改变的链接
    for r in rlist:
        if r == sk:
            # 新客户端来连接
            conn, address = r.accept()
            conn.sendall(bytes('hello', encoding='utf-8'))
            # conn是什么? 其实是socket对象 连接成功后添加进客户端列表rlist
            inputs.append(conn)
            # 以该客户端为键添加字典元素
            # message[conn] = []
            message[conn] = queue.Queue()
            size[conn] = {'size': 0, 'flag': False}
        else:
            # 有人给我发了消息
            try:
                ret = r.recv(1024)
                # r.send(ret)
                if not ret:
                    raise Exception('断开连接')
                else:
                    # 如果是已经建立连接的客户端发来消息 添加进消息客户端列表wlist
                    outputs.append(r)
                    # 具体消息写入字典
                    # message[r].append(ret)
                    message[r].put(ret)
                    # print(message)
            except Exception as e:
                # 如果客户端异常断开 清理列表
                inputs.remove(r)
                del message[r]

    # 读写分离 专门负责发消息
    for w in wlist:
        # 读取字典的最后消息
        # msg = message[w].pop()
        # msg = message[w][-1]
        try:
            msg = message[w].get_nowait()
        except queue.Empty:
            print("client [%s]" % w.getpeername()[0], "queue is empty..")
            outputs.remove(w)

        try:
            msg = json.loads(msg.decode())

            if size[w]['flag'] is False and msg['action'] == 'put':
                size[w]['file_name'] = msg['file_name']
                size[w]['file_size'] = msg['file_size']

                server_response = {'status': 200}
                w.send(bytes(json.dumps(server_response), encoding='utf-8'))
                size[w]['flag'] = True

                outputs.remove(w)

            if msg['action'] == 'pull':
                file = os.path.join(base_dir, msg['file_name'])
                file_size = os.stat(file).st_size
                server_response = {'file_size': file_size}
                w.sendall(bytes(json.dumps(server_response), encoding='utf-8'))

                f = open(file, 'rb+')
                send_size = 0
                buffer_size = 1024
                while send_size < file_size:
                    if file_size - send_size < buffer_size:
                        file_data = f.read(file_size - send_size)
                        send_size = file_size
                    else:
                        file_data = f.read(buffer_size)
                        send_size += buffer_size
                    w.send(file_data)
                f.close()
                print('传输完成...')

        except Exception:
            if size[w]['flag'] is True:

                f = open(os.path.join(base_dir, 'put', size[w]['file_name']), 'ab+')
                f.write(msg)
                f.close()
                size[w]['size'] += len(msg)
                outputs.remove(w)

                if size[w]['size'] == size[w]['file_size']:
                    size[w]['flag'] = False
                    print('传输完成...')



