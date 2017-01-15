# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import paramiko
import sys
import os
import socket
import getpass
import termios
import tty
import select
from paramiko.py3compat import u


def interactive_shell(chan):
    # 获取原tty属性
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        # 为tty设置新属性
        # 默认当前tty设备属性：
        # 输入一行回车，执行
        # CTRL+C 进程退出，遇到特殊字符，特殊处理。

        # 这是为原始模式，不认识所有特殊符号
        # 放置特殊字符应用在当前终端，如此设置，将所有的用户输入均发送到远程服务器
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        log = open('handle.log', 'a+', encoding='utf-8')
        flag = False
        temp_list = []

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    # 如果用户上一次点击的是tab键，则获取返回的内容写入在记录中
                    if flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            temp_list.append(x)
                        flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                # 读取用户在终端数据每一个字符
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                # 如果用户点击TAB键
                if x == '\t':
                    flag = True
                else:
                    # 未点击TAB键，则将每个操作字符记录添加到列表中，以便之后写入文件
                    temp_list.append(x)

                # 如果用户敲回车，则将操作记录写入文件
                if x == '\r':
                    log.write(''.join(temp_list))
                    log.flush()
                    temp_list.clear()
                chan.send(x)

    finally:
        # 重新设置终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def run():
    db_dict = {
        '10.0.0.111': {
            'root': {'user': 'root', 'auth': 'r', "cert": 'key路径'},
            'alex': {'user': 'root', 'auth': 'p', "cert": '123456'},
        },
        'c2': {
            'root': {'user': 'root', 'auth': 'r', "cert": 'key路径'},
            'alex': {'user': 'alex', 'auth': 'p', "cert": '密码'},
        },

    }

    for row in db_dict.keys():
        print(row)

    hostname = input('请选择主机: ')
    tran = paramiko.Transport((hostname, 22,))
    tran.start_client()

    for item in db_dict[hostname].keys():
        print(item)

    username = input('请输入用户: ')

    user_dict = db_dict[hostname][username]
    if user_dict['auth'] == 'r':
        key = paramiko.RSAKey.from_private_key_file(user_dict['cert'])
        tran.auth_publickey(username, key)
    else:
        pw = user_dict['cert']
        tran.auth_password('root', pw)

    # 打开一个通道
    chan = tran.open_session()
    # 获取一个终端
    chan.get_pty()
    # 激活器
    chan.invoke_shell()

    interactive_shell(chan)

    chan.close()
    tran.close()


if __name__ == '__main__':
    run()