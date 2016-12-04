# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import re
import sys
import json
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


def login(s):

    while True:
        send_data = input('>>: ').strip()
        if len(send_data) == 0: continue
        s.send(bytes(send_data, encoding='utf-8'))
        recv_data = s.recv(1024)
        print(recv_data.decode())

        if re.match('欢迎', recv_data.decode()):
            break


def task_put(s, cmd_list):

    abs_filepath = cmd_list[1]
    if os.path.isfile(abs_filepath):
        file_size = os.stat(abs_filepath).st_size
        file_name = abs_filepath.split('\\')[-1]
        print('file:{} size:{}'.format(file_name, file_size))
        msg_data = {"action": "put",
                    "file_name": file_name,
                    "file_size": file_size,
                    "file_path": abs_filepath}

        s.sendall(bytes(json.dumps(msg_data), encoding='utf-8'))

        server_confirm_msg = s.recv(1024)
        confirm_data = json.loads(server_confirm_msg.decode())

        if confirm_data['status'] == 200:
            print('Start sending file \033[31;0m{}\033[0m!'.format(msg_data['file_name']))
            f = open(msg_data['file_path'], 'r+')
            i = 0
            num, last_size = divmod(file_size, 1024)
            while i <= num:


            print('Send file done!')
    else:
        print('\033[31;0m{}\033[0m文件不存在...'.format(abs_filepath))


def task_pull(s, cmd_list):
    file_name = cmd_list[-1]
    msg_data = {"action": "pull", "file_name": file_name}
    s.send(bytes(json.dumps(msg_data), encoding='utf-8'))

    data = s.recv(1024)
    data = json.loads(data.decode())
    file_name = data.get('file_name')
    file_size = data.get('file_size')
    server_response = {'status': 200}
    s.send(bytes(json.dumps(server_response), encoding='utf-8'))
    f = open(os.path.join(base_dir, file_name), 'wb')
    recv_size = 0

    while recv_size < file_size:
        data = s.recv(4096)
        f.write(data)
        recv_size += len(data)
    print('File recv success!')
    f.close()


def task_types(s, cmd_list):

    if len(cmd_list) == 1:
        if cmd_list[0] == 'mkdir':
            print('ERROR: mkdir + 文件夹名...')
        if cmd_list[0] == 'rm':
            print('ERROR: rm + 文件夹名...')
        else:
            msg_data = {"action":  cmd_list[0],
                        "file_name": None}
            msg_send(s, msg_data)

    if len(cmd_list) == 2:
        task_type = cmd_list[0]
        if task_type == 'put':
            task_put(s, cmd_list)
        if task_type == 'pull':
            task_pull(s, cmd_list)
        if task_type in ['cd', 'ls', 'mkdir', 'rm']:
            msg_data = {"action": cmd_list[0], "file_name": cmd_list[-1]}
            msg_send(s, msg_data)


def msg_send(s, msg_data):
    s.send(bytes(json.dumps(msg_data), encoding='utf-8'))
    recv_data = s.recv(1024)
    print(recv_data.decode())


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
        login(s)

        while True:
            task_list = ['ls', 'put', 'pull', 'mkdir', 'rm', 'cd']
            send_data = input('>>: ').strip()
            if len(send_data) == 0: continue

            cmd_list = send_data.split()
            if cmd_list[0] not in task_list:
                print('不支持的命令！[Help]查看帮助...')
                continue
            task_types(s, cmd_list)


if __name__ == '__main__':
    main()
