# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys
import time
import yaml
import socket
import select
import getpass
import paramiko
import threading
from src import db_conn

from paramiko.py3compat import u

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, user_name, host):
    if has_termios:
        posix_shell(chan, user_name, host)
    else:
        windows_shell(chan, user_name, host)


def posix_shell(chan, user_name, host):

    sys.stdout.write("终端启动成功...\r\n\r\n")

    # 获取原tty属性
    old_tty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

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
                    # 开始写入日志
                    times = time.strftime('%Y-%m-%d %H:%M')
                    obj = db_conn.HistoryLog(time=times, user_name=user_name, host=host, cmd=''.join(temp_list))
                    db_conn.session.add(obj)
                    db_conn.session.commit()
                    temp_list.clear()
                chan.send(x)

    finally:
        # 重新设置终端属性
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


def windows_shell(chan, user_name, host):
    sys.stdout.write("终端启动成功...\r\n\r\n")

    def write_all(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(str(data, encoding='utf-8'))
            sys.stdout.flush()

    writer = threading.Thread(target=write_all, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        pass


def login():

    while True:
        fort_username = input('输入用户名 >>:')
        if not fort_username: continue
        ret = db_conn.session.query(db_conn.FortUser).filter_by(user_name=fort_username).all()
        if not ret:
            print('用户不存在...')
            continue

        # 读取用户组
        hosts_file = os.path.join(base_dir, 'db', 'new_fort_user.yml')
        f = open(hosts_file)
        source = yaml.load(f)
        if source:

            for key, val in source.items():
                if key == fort_username:
                    group_name = val.get('group')
                    if not group_name:
                        group_name = None

        obj = ret[0]
        pwd = obj.pwd
        # inp_pwd = getpass.getpass('输入密码 >>:')
        inp_pwd = input('输入密码 >>:')
        if not pwd: continue
        if pwd == inp_pwd:
            return fort_username, group_name
        else:
            print('密码错误...')


def run():
    print('''\033[32;0m
    #########################################################
                        欢迎使用堡垒机

      * 使用说明：
            1. 直接登陆您的堡垒机账户
            2. 选择已经授权主机远程登陆
            3. 修改授权请联系管理员

      * 注意：  您的所有操作将被记录
    ##########################################################

    \033[0m''')

    user_name, group_name = login()
    print('\033[32;0m欢迎[\033[31;0m%s\033[0m]\033[32;0m!!! \n当前所属用户组\033[0m[\033[31;0m%s\033[0m]...\033[0m' %
          (user_name, group_name))

    ret = db_conn.session.query(db_conn.FortUser).filter_by(user_name=user_name).all()
    host_list = []
    for obj in ret:
        # print(obj)

        # 单独主机
        if obj.host_user_id:
            host_list.append([obj.host_user.host.hostname, obj.host_user.host.ip, obj.host_user.user_name,
                              obj.host_user.pwd, obj.host_user.host.port])

        # 用户组主机
        else:
            # 由主机组反向查找主机用户组里面所有属于该组的机器 并添加进列表
            group_ret = db_conn.session.query(db_conn.Group).filter_by(id=obj.group_id).all()
            group_name = group_ret[0].group_name
            group_obj = db_conn.session.query(db_conn.Group).filter(db_conn.Group.group_name == group_name).first()
            for item in group_obj.g:
                host_id = item.id
                host_user_ret = db_conn.session.query(db_conn.HostUser).filter_by(id=host_id).all()
                for obj in host_user_ret:
                    host_list.append([obj.host.hostname, obj.host.ip, obj.user_name, obj.pwd, obj.host.port])

    # print(host_list)
    print('%-8s %-7s %-13s %-10s' % ('序号', '主机名', 'IP地址', '用户名'))
    for i, j in enumerate(host_list):
        print('%-10s %-10s %-15s %-10s' % (i + 1, j[0], j[1], j[2]))

    while True:

        inp = input('选择主机编号 >>:')
        if not inp: continue
        try:
            inp = int(inp)
            route_user = host_list[inp-1][-3]
            host = host_list[inp-1][1]
            host_port = host_list[inp-1][-1]
            pwd = host_list[inp-1][-2]
        except Exception:
            print('输入错误...')
            continue

        try:
            tran = paramiko.Transport((host, host_port))
            tran.start_client()
            tran.auth_password(route_user, pwd)
            break
        except Exception:
            print('连接失败, 请检查用户名或者密码是否正确...')
            continue

    chan = tran.open_session()
    chan.get_pty()
    chan.invoke_shell()

    interactive_shell(chan, user_name, host)

    chan.close()
    tran.close()
    sys.exit()

if __name__ == '__main__':
    run()



