# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

from __future__ import division

import os
import re
import sys
import time
import json
import math
import socket
import hashlib

# 客户端程序运行的本地目录
base_dir = os.path.dirname(os.path.abspath(__file__))


def connect_server():
    """
    客户端连接服务端：IP + PORT
    :return:
    """
    while True:
        ip_port = input('请输入服务端地址： ')
        if not re.match('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}:\d+$', ip_port):
            print('地址有误...')
            continue
        else:
            ip_port = (ip_port.split(':')[0], int(ip_port.split(':')[1]))
            return ip_port


def login(s):
    """
    FTP登陆 如果登陆不成功即不允许与服务端会话
    :param s:
    :return:
    """
    while True:
        send_data = input('>>: ').strip()
        if len(send_data) == 0: continue
        s.send(bytes(send_data, encoding='utf-8'))
        recv_data = s.recv(1024)
        print(recv_data.decode())

        if re.match('欢迎', recv_data.decode()):
            break


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


def file_md5(file_path):
    """
    文件的MD5校验
    :param file_path:
    :return:
    """
    f = open(file_path, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    md5_hash = md5obj.hexdigest()
    f.close()
    return str(md5_hash).upper()


def task_put(s, cmd_list):
    """
    执行上传文件put方法
    :param s:
    :param cmd_list:
    :return:
    """
    abs_filepath = cmd_list[1]
    if os.path.isfile(abs_filepath):
        file_size = os.stat(abs_filepath).st_size
        file_name = abs_filepath.split('\\')[-1]
        print('file:{} size:{}'.format(file_name, file_size))

        # 给服务端发送一个包含文件名 文件大小等信息的json文件
        msg_data = {"action": "put",
                    "file_name": file_name,
                    "file_size": file_size,
                    "file_path": abs_filepath}

        s.sendall(bytes(json.dumps(msg_data), encoding='utf-8'))

        # 接收服务端的确认信息
        server_confirm_msg = s.recv(1024)
        confirm_data = json.loads(server_confirm_msg.decode())

        if confirm_data['status'] == 200:

            # 如果服务端已有文件 得到文件大小 进行断点续传
            read_size = confirm_data['read_size']
            if read_size != 0:
                send_size = read_size
                print('服务器上检测到相同文件 已经启动断点续传...')
                time.sleep(0.5)
            else:
                send_size = 0
            print('Start sending file \033[31;0m{}\033[0m!'.format(msg_data['file_name']))

            # 打开文件 进行指针偏移 开始发送数据
            f = open(msg_data['file_path'], 'rb+')
            f.seek(read_size, 0)
            for line in f:
                s.send(line)
                send_size += len(line)
                progressbar(send_size, file_size)
            f.close()
            print('上传文件 \033[31;0m{}\033[0m 成功!'.format(file_name))

            # 上传成功后进行MD5校验
            print('正在校验 MD5 值...')
            md5_hash = file_md5(abs_filepath)
            ret = s.recv(1024)
            if md5_hash == ret.decode():
                print('MD5值 \033[31;0m{}\033[0m 校验成功!'.format(md5_hash))
            else:
                print('MD5值 \033[31;0m{}\033[0m 校验失败!'.format(md5_hash))

    else:
        print('\033[31;0m{}\033[0m文件不存在...'.format(abs_filepath))


def task_pull(s, cmd_list):
    """
    下载文件pull方法
    :param s:
    :param cmd_list:
    :return:
    """
    file_name = cmd_list[-1]

    file = os.path.join(base_dir, file_name)

    # 判断本地路径下是否有相同文件 得到该文件大小 方便断点续传
    if os.path.exists(file):
        recv_size = os.stat(file).st_size
        print('本地检测到相同文件 已经启动断点续传...')
    else:
        recv_size = 0

    # 发送请求给服务端
    msg_data = {"action": "pull", "file_name": file_name}
    s.send(bytes(json.dumps(msg_data), encoding='utf-8'))

    # 服务端收到下载请求 等待确认开始传输
    data = s.recv(1024)
    data = json.loads(data.decode())
    file_name = data.get('file_name')
    file_size = data.get('file_size')
    server_response = {'status': 200, "read_size": recv_size}
    s.send(bytes(json.dumps(server_response), encoding='utf-8'))
    f = open(os.path.join(base_dir, file_name), 'ab+')

    # 收到总的文件大小 开始循环接收
    while recv_size < file_size:
        data = s.recv(4096)
        f.write(data)
        recv_size += len(data)
        progressbar(recv_size, file_size)
    print('下载文件 \033[31;0m{}\033[0m 成功!\n本地路径：\033[31;0m{}\033[0m'.format(file_name, file))
    f.close()

    # 接受完成MD5校验
    print('正在校验 MD5 值...')
    md5_hash = file_md5(file)
    ret = s.recv(1024)
    if md5_hash == ret.decode():
        print('MD5值 \033[31;0m{}\033[0m 校验成功!'.format(md5_hash))
    else:
        print('MD5值 \033[31;0m{}\033[0m 校验失败!'.format(md5_hash))


def task_types(s, cmd_list):
    """
    对客户端命令进行有效性判断
    :param s:
    :param cmd_list:
    :return:
    """
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
    """
    向服务端发送一条消息并接收一条消息并打印
    :param s:
    :param msg_data:
    :return:
    """
    s.send(bytes(json.dumps(msg_data), encoding='utf-8'))
    recv_data = s.recv(1024)
    print(recv_data.decode())


def main():
    """
    客户端主程序函数：线路连接 + 循环会话
    :return:
    """
    print('  \033[32;0mFTP客户端程序\033[0m  '.center(50, '-'))

    while True:
        # 连接服务端
        ip_port = connect_server()
        # ip_port = ('10.0.0.150', 8000)
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

        # 开始循环会话
        while True:
            task_list = ['ls', 'put', 'pull', 'mkdir', 'rm', 'cd']
            send_data = input('>>: ').strip()
            if len(send_data) == 0: continue

            cmd_list = send_data.split()
            if cmd_list[0].upper() == 'HELP':
                print('''\033[32;0m
                --------- Help 帮助信息 ----------
                1. ls    浏览目录
                2. cd    切换目录
                3. rm    删除文件
                4. mkdir 新建文件夹
                5. put   上传文件
                6. pull  下载文件
                \033[0m''')
                continue
            if cmd_list[0] not in task_list:
                print('不支持的命令！[Help]查看帮助...')
                continue

            task_types(s, cmd_list)


if __name__ == '__main__':
    main()
