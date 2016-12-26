# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 上下文管理

import contextlib

free_list = []
current_thread = 'a'


@contextlib.contextmanager
def worker_state(state_list, worker_thread):
    state_list.append(worker_state)
    try:
        yield
    finally:
        state_list.remove(worker_thread)

with worker_state(free_list, current_thread):
    print('123')
    print('456')


# 利用上下文管理 自动关闭socket

import socket


def context_socket(host, port):
    sk = socket.socket()
    sk.bind((host, port))
    sk.listen(5)
    try:
        # 将 sk 返回
        yield sk
    finally:
        sk.close()

with context_socket('127.0.0.1', 8888) as sock:
    print(socket)
