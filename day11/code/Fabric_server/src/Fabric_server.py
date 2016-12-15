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
from lib.decryption import file_md5

# 客户端程序运行的本地目录
base_dir = os.path.dirname(os.path.abspath(__file__))

GROUP_DIC = {}
HOST_NUM = 0
HOST_LIST = []


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


def task_put(s, cmd_list):
    """
    执行上传文件put方法
    :param s:
    :param cmd_list:
    :return:
    """
    abs_filepath = cmd_list.split()[-1]
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
    file_name = os.path.basename(cmd_list.split()[-1])

    # file = os.path.join(base_dir, file_name)
    file = cmd_list.split()[-1]

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
    print(base_dir)
    pull_path = os.path.join(base_dir, file_name)
    # f = open(os.path.join(base_dir, file_name), 'ab+')
    f = open(pull_path, 'ab+')

    # 收到总的文件大小 开始循环接收
    while recv_size < file_size:
        data = s.recv(4096)
        f.write(data)
        recv_size += len(data)
        progressbar(recv_size, file_size)
    print('下载文件 \033[31;0m{}\033[0m 成功!\n本地路径：\033[31;0m{}\033[0m'.format(file_name, pull_path))
    f.close()

    # 接受完成MD5校验
    print('正在校验 MD5 值...')
    md5_hash = file_md5(pull_path)
    ret = s.recv(1024)
    if md5_hash == ret.decode():
        print('MD5值 \033[31;0m{}\033[0m 校验成功!'.format(md5_hash))
    else:
        print('MD5值 \033[31;0m{}\033[0m 校验失败!'.format(md5_hash))


def host_show():
    """
    程序一运行读取主机列表文件并展示
    :return:
    """
    print('%-8s%-7s%-13s%-10s' % ('序号', '主机名', 'IP地址', '主机组'))
    config = configparser.ConfigParser()
    config.read(setting.HOST_LIST, encoding='utf-8')
    host_list = config.sections()
    host_num = 1
    host_add = []
    global GROUP_DIC
    GROUP_DIC = {}
    for host in host_list:
        print('%-10s%-10s%-15s%-10s' % (host_num, host, config.get(host, 'ip'), config.get(host, 'group')))
        host_num += 1
        host_tuple = (host, config.get(host, 'ip'))
        host_add.append(host_tuple)
        ret = GROUP_DIC.get(config.get(host, 'group'))
        if not ret:
            GROUP_DIC[config.get(host, 'group')] = [host]
        else:
            GROUP_DIC[config.get(host, 'group')].append(host)
    global HOST_NUM
    global HOST_LIST
    HOST_NUM = host_num
    HOST_LIST = host_add
    return host_num, host_add


def host_test():
    """
    创建多线程去连接主机
    :return:
    """
    for i in range(HOST_NUM - 1):
        t = threading.Thread(target=link_test, args=(i, HOST_LIST,))
        t.start()
        t.join()
    user_inp = input('[b返回]>>')
    if user_inp: pass


def link_test(*args):
    """
    连接主机 如果超时2秒就判断为离线
    :param args:
    :return:
    """
    i = args[0]
    host_name = args[1][i][0]
    host_ip = args[1][i][1]
    ip_port = (host_ip, 8000)
    s = socket.socket()
    s.settimeout(2)
    ret = s.connect_ex(ip_port)
    if ret != 0:
        print('{} {} [\033[31;0m离线\033[0m]'.format(host_name, host_ip))
    else:
        print('{} {} [\033[32;0m正常\033[0m]'.format(host_name, host_ip))


def host_manager():
    """
    添加节点主机 如果远程主机连接成功返回其主机名 deny表示master_address地址不对 拒绝访问
    :return:
    """

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
                time.sleep(1)
                break
            else:
                print('主机 \033[31;0m %s \033[0m已经存在..' % host_name)
                time.sleep(1)


def main():
    """
    服务端主函数
    :return:
    """
    while True:
        print('  \033[32;0mFabric主机管理\033[0m  '.center(50, '-'))
        host_show()
        group_show()
        print('''\033[32;0m\nj. 添加主机\nd. 删除主机\ng. 主机组\nc. 测试\nq. 退出
        \033[0m''')
        print('''帮助信息：
    1. 操作主机：     salt  主机名    cmd.命令 (如：salt web01 cmd.ls)
    2. 操作主机组：   salts 主机组名  cmd.命令  (如：salts web cmd.ls)
    3. 上传\下载命令：put.文件绝对路径 pull.文件绝对路径 (如： salt web01 cmd.put F:\one.txt)
        ''')
        user_mode = {
            'c': host_test,
            'q': system_exit,
            'd': host_remove,
            'j': host_manager,
            'g': group_manager,
        }

        while True:
            user_inp = input('[b返回]>>>:')
            user_cmd = user_inp.split()[0]

            if user_cmd == 'salt':
                salt_moder(user_inp)
            if user_cmd == 'salts':
                salts_moder(user_inp)
            if user_inp in user_mode:
                user_mode[user_inp]()
                break
            if user_cmd == 'b':
                break


def salt_moder(cmd):
        """
        单线程连接主机并远程执行命令
        :param cmd:
        :return:
        """
        try:
            config = configparser.ConfigParser()
            config.read(setting.HOST_LIST, encoding='utf-8')
            host_name = cmd.split()[1]
            host_ip = config.get(host_name, 'ip')
            ip_port = (host_ip, 8000)
            s = socket.socket()
            s.connect(ip_port)
            s.recv(1024)
        except Exception:
            print('输入有误...')
            return

        user_cmd = cmd.split('cmd.')[-1]

        if user_cmd.split()[0] == 'put':
            task_put(s, user_cmd)
        elif user_cmd.split()[0] == 'pull':
            task_pull(s, user_cmd)
        else:
            s.send(bytes(user_cmd, encoding='utf-8'))
            ret = s.recv(1024)
            print('\033[32;0m-- {} {}--\033[0m'.format(host_name, host_ip))
            print(ret.decode())


def salts_moder(cmd):
    """
    批量远程执行命令时启用多线程
    :param cmd:
    :return:
    """
    host_list = GROUP_DIC.get(cmd.split()[1])
    host_len = len(host_list)

    for i in range(host_len):
        new_cmd = re.sub(cmd.split()[1], host_list[i], cmd, 1)
        t = threading.Thread(target=salt_moder, args=(new_cmd, ))
        t.start()
        t.join()


def group_show():
    """
    统计主机组函数
    :return:
    """
    for key in GROUP_DIC:
        if key == 'None':
            continue
        else:
            print('[\033[32;0m{}组 计数：{}\033[0m]'.format(key, len(GROUP_DIC[key])))
            for item in GROUP_DIC[key]:
                print(item)


def group_manager():
    """
    创建主机组或者添加新组成员
    :return:
    """
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


def host_remove():
    """
    主机节点移除
    :return:
    """
    config = configparser.ConfigParser()
    config.read(setting.HOST_LIST, encoding='utf-8')

    inp = input('输入要删除的主机：')
    if config.has_section(inp):
        config.remove_section(inp)
        config.write(open(setting.HOST_LIST, 'w'))
        print('删除主机\033[31;0m{}\033[0m成功!'.format(inp))
        time.sleep(1)
    else:
        print('主机不存在...')
        time.sleep(1)


def system_exit():
    sys.exit()


if __name__ == '__main__':
    main()
