# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import sys
import socket
import select
import getpass
import paramiko
import threading
import db_conn

from paramiko.py3compat import u


try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):

    sys.stdout.write("终端启动成功...\r\n\r\n")

    # 获取原tty属性
    old_tty = termios.tcgetattr(sys.stdin)
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
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


def windows_shell(chan):
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


def run():
    print('\033[32;0m----------  堡垒机  -----------\033[0m')

    # while True:
    #     host = input('输入主机地址：')
    #     if not host: continue
    #     username = input('输入用户名：')
    #     if not username: continue
    #     break
    # user_name = getpass.getuser()
    # print(user_name)
    user_name = 'user01'
    pwd = '123'
    ret = db_conn.session.query(db_conn.FortUser).filter_by(user_name=user_name).all()
    host_list = []
    for obj in ret:
        # print(obj)

        # 单独主机
        if obj.host_user_id:
            # host_ret = db_conn.session.query(db_conn.Host).filter_by()
            # print(obj.host_user.host.hostname, obj.host_user.host.ip, obj.host_user.user_name, obj.host_user.pwd)
            host_list.append([obj.host_user.host.hostname, obj.host_user.host.ip, obj.host_user.user_name, obj.host_user.pwd])

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
                    # print(obj.host.hostname, obj.host.ip, obj.user_name, obj.pwd)
                    host_list.append([obj.host.hostname, obj.host.ip, obj.user_name, obj.pwd])

    # print(host_list)
    for i, j in enumerate(host_list):
        print(i + 1, j)


    inp = input('选择主机： ')
    tran = paramiko.Transport((host, 22))
    tran.start_client()

    while True:
        pwd = getpass.getpass('输入主机[%s] 用户[%s] 密码: ' % (username, host))
        if len(pwd) == 0:
            print('密码不能为空...')
            continue
        else:
            tran.auth_password(username, pwd)
            break

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



