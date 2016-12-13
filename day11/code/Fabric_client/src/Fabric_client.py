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
import threading
import configparser
from conf import setting

# 客户端程序运行的本地目录
base_dir = os.path.dirname(os.path.abspath(__file__))

GROUP_DIC = {}

def connect_server():
    """
    客户端连接服务端：IP + PORT
    :return:
    """
    while True:
        ip_port = input('请输入主机地址[ip:port]： ')
        if not re.match('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}:\d+$', ip_port):
            print('地址有误[ip:port]...')
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


def main1():
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


def host_show():
    print('%-8s%-7s%-13s%-10s' % ('序号', '主机名', 'IP地址', '主机组'))
    config = configparser.ConfigParser()
    config.read(setting.HOST_LIST, encoding='utf-8')
    host_list = config.sections()
    host_num = 1
    host_add = []
    for host in host_list:
        print('%-10s%-10s%-15s%-10s' % (host_num, host, config.get(host, 'ip'), config.get(host, 'group')))
        host_num += 1
        host_tuple = (host, config.get(host, 'ip'))
        host_add.append(host_tuple)
        global GROUP_DIC
        ret = GROUP_DIC.get(config.get(host, 'group'))
        if not ret:
            GROUP_DIC[config.get(host, 'group')] = [host]
        else:
            GROUP_DIC[config.get(host, 'group')].append(host)
    return host_num, host_add


def link_test(*args):
    i = args[0]
    host_name = args[1][i][0]
    host_ip = args[1][i][1]
    ip_port = (host_ip, 8000)
    s = socket.socket()
    s.settimeout(2)
    ret = s.connect_ex(ip_port)
    if ret != 0:
        print('{} {} [\033[31;0m失败\033[0m]'.format(host_name, host_ip))
    else:
        print('{} {} [\033[32;0m成功\033[0m]'.format(host_name, host_ip))


def host_manager():

    while True:
        # 连接服务端
        ip_port = connect_server()
        # ip_port = ('10.0.0.104', 8000)
        s = socket.socket()
        s.settimeout(2)
        ret = s.connect_ex(ip_port)
        if ret != 0:
            print('服务器：\033[31;0m{}\033[0m 端口：\033[31;0m{}\033[0m 连接失败...'.format(ip_port[0], ip_port[1]))
            print('请检查IP和端口并重试!\n')
            continue

        host_msg = s.recv(1024)
        if host_msg.decode() == 'deny':
            print('\033[31;0m{}\033[0m 拒绝访问...'.format(ip_port[0]))
            continue
        else:
            host_name = host_msg.decode().split('\n')[0]
            config = configparser.ConfigParser()
            config.read(setting.HOST_LIST, encoding='utf-8')
            if not config.has_section(host_name):
                config.add_section(host_name)
                config.set(host_name, 'IP', ip_port[0])
                config.set(host_name, 'GROUP', 'None')
                config.write(open(setting.HOST_LIST, 'w'))
                print('主机\033[31;0m %s \033[0m添加成功..' % host_name)
                break
            else:
                print('主机 \033[31;0m %s \033[0m已经存在..' % host_name)


def main():

    while True:
        print('  \033[32;0mFabric主机管理\033[0m  '.center(50, '-'))
        host_num, host_list = host_show()
        group_show()
        print('''\033[32;0m\nj. 添加主机\nd. 删除主机\ng. 创建组\nc. 连接\nq. 退出
        \033[0m''')
        user_select = input('>>>:')

        if user_select == 'j':
            host_manager()

        if user_select == 'g':
            group_manager()

        if user_select == 'c':
            for i in range(host_num - 1):
                t = threading.Thread(target=link_test, args=(i, host_list, ))
                t.start()
                t.join()

        if user_select == 'd':
            # host_del = input('输入要删除的主机名：')
            pass

        if user_select == 'q':
            break


def group_show():
    # print(GROUP_DIC)
    # print('-- 主机组 --')
    for key in GROUP_DIC:
        if key == 'None':
            continue
        else:
            print('[\033[32;0m{}组\033[0m]'.format(key))
            for item in GROUP_DIC[key]:
                print(item)


def group_manager():
    config = configparser.ConfigParser()
    config.read(setting.HOST_LIST, encoding='utf-8')

    group_name = input('输入组名：')
    if group_name:
        host_num, host_list = host_show()
        while True:
            user_select = input('选择主机[b返回]:')
            if user_select == 'b':
                break
            try:
                user_select = int(user_select)
                host_name = host_list[user_select - 1][0]
                config.set(host_name, 'group', group_name)
                config.write(open(setting.HOST_LIST, 'w'))
                print('\033[31;0m{}\033[0m添加成功!'.format(host_name))
            except Exception:
                print('输入错误!')
                continue


def main2():
    print('  \033[32;0mFabric主机管理\033[0m  '.center(50, '-'))
    print('1. 主机管理\n2. 主机组管理\n3.退出')
    user_inp = input('>>>')
    if user_inp == '1':
        host_manager()
    if user_inp == '2':
        group_manager()
    if user_inp == 'q':
        sys.exit()


if __name__ == '__main__':
    main()
