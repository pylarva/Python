# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import re
import json
import subprocess
import configparser
import socketserver
from conf import setting
from lib.decryption import decryption_pwd


class MyServer(socketserver.BaseRequestHandler):

    USER_HOME = setting.USER_HOME
    CURRENT_PATH = USER_HOME

    def handle(self):
        conn = self.request
        conn.sendall(bytes('连接成功!请登陆...\n输入用户名', encoding='utf-8'))

        while True:
            user_name = conn.recv(1024)
            conn.sendall(bytes('输入密码', encoding='utf-8'))
            user_pwd = conn.recv(1024)
            ret, disk_limit = self.login(user_name.decode(), user_pwd.decode())

            if ret:
                conn.sendall(bytes('欢迎 \033[31;0m{}\033[0m ...\n'
                                   '您的家目录为 \033[31;0m{}\033[0m\n'
                                   '磁盘空间为 \033[31;0m{}MB\033[0m'.format(user_name.decode(), self.USER_HOME,
                                                                        disk_limit), encoding='utf-8'))
                self.session()
                break
            else:
                conn.sendall(bytes('用户名或密码错误...\n请重新输入用户名：', encoding='utf-8'))

    def login(self, user_name, user_pwd):
        config = configparser.ConfigParser()
        config.read(setting.USER_DB, encoding='utf-8')
        user_pwd = decryption_pwd(user_pwd)

        if config.has_section(user_name) and user_pwd == config.get(user_name, 'password'):
            disk_limit = config.get(user_name, 'disk_limit')
            self.USER_HOME = os.path.join(self.USER_HOME, user_name)
            self.CURRENT_PATH = self.USER_HOME
            return True, disk_limit
        else:
            return False, False

    def task_put(self, *args, **kwargs):
        print('---put', args, kwargs)
        file_name = args[0].get('file_name')
        file_size = args[0].get('file_size')
        server_response = {'status': 200}
        self.request.send(bytes(json.dumps(server_response), encoding='utf-8'))
        f = open(os.path.join(self.CURRENT_PATH, file_name), 'wb')
        recv_size = 0

        while recv_size < file_size:
            data = self.request.recv(4096)
            f.write(data)
            recv_size += len(data)
        print('File recv success!')
        f.close()

    def task_pull(self, *args):

        file_name = args[0].get('file_name')
        file = os.path.join(self.CURRENT_PATH, file_name)
        if os.path.isfile(file):
            file_size = os.stat(file).st_size
            print('file:{} size:{}'.format(file_name, file_size))
            msg_data = {
                        "file_name": file_name,
                        "file_size": file_size}

            self.request.send(bytes(json.dumps(msg_data), encoding='utf-8'))

            server_confirm_msg = self.request.recv(1024)
            confirm_data = json.loads(server_confirm_msg.decode())

            if confirm_data['status'] == 200:
                print('Start sending file \033[31;0m{}\033[0m!'.format(msg_data['file_name']))
                f = open(file, 'rb')
                for line in f:
                    self.request.send(line)
                print('Send file done!')
        else:
            print('\033[31;0m{}\033[0m文件不存在...'.format(file_name))

    def task_ls(self, *args, **kwargs):
        print('---ls', args, kwargs)
        path_name = args[0].get('file_name')
        print(self.CURRENT_PATH)
        if not path_name:
            cmd = subprocess.Popen('ls -lh {}'.format(self.CURRENT_PATH), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
            self.request.send(cmd_res)
            return

    def task_cd(self, *args, **kwargs):
        conn = self.request
        print('---cd', args, kwargs)
        path_name = args[0].get('file_name')

        if not path_name:
            cmd = subprocess.Popen('cd {}'.format(self.USER_HOME), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
            self.CURRENT_PATH = self.USER_HOME
            if len(cmd_res) == 0:
                conn.send(bytes(self.CURRENT_PATH, encoding='utf-8'))
            else:
                conn.send(cmd_res)
            return

        if path_name == '.':
            conn.send(bytes(self.CURRENT_PATH, encoding='utf-8'))
        if path_name == '..':
            upper_dir = os.path.dirname(self.CURRENT_PATH)
            if not re.match(self.USER_HOME, upper_dir):
                conn.send(bytes('未授权路径...', encoding='utf-8'))
            if re.match(self.USER_HOME, upper_dir):
                self.CURRENT_PATH = os.path.dirname(self.CURRENT_PATH)
                conn.send(bytes(self.CURRENT_PATH, encoding='utf-8'))
            print(self.CURRENT_PATH)

        new_path = os.path.join(self.CURRENT_PATH, path_name)
        if not os.path.exists(new_path):
            conn.send(bytes('文件夹\033[31;0m{}\033[0m不存在...'.format(path_name), encoding='utf-8'))
        if os.path.exists(new_path) and os.path.basename(new_path) != '..':
            self.CURRENT_PATH = new_path
            conn.send(bytes(self.CURRENT_PATH, encoding='utf-8'))

    def task_mkdir(self, *args):
        conn = self.request
        file_name = args[0].get('file_name')
        cmd = subprocess.Popen('mkdir {}'.format(os.path.join(self.CURRENT_PATH, file_name)), shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_res = cmd.stdout.read()
        if len(cmd_res) == 0:
            conn.send(bytes('创建成功!', encoding='utf-8'))
        else:
            conn.send(cmd_res)

    def task_rm(self, *args):
        conn = self.request
        file_name = args[0].get('file_name')
        file_path = os.path.join(self.CURRENT_PATH, file_name)
        if not os.path.isfile(file_path):
            conn.send(bytes('文件不存在...', encoding='utf-8'))
            return
        else:
            cmd = subprocess.Popen('rm -f {}'.format(os.path.join(self.CURRENT_PATH, file_name)), shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
        if len(cmd_res) == 0:
            conn.send(bytes('删除成功!', encoding='utf-8'))
        else:
            conn.send(cmd_res)

    def session(self):

        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            print('[%s] says: %s' % (self.client_address, data.decode()))

            task_data = json.loads(data.decode())
            task_action = task_data.get('action')

            print(self.CURRENT_PATH)
            if hasattr(self, 'task_%s' % task_action):
                self.func = getattr(self, 'task_%s' % task_action)
                self.func(task_data)
                continue
            else:
                print('Task action is not supported...', task_action)
                self.request.send(bytes('不支持的远程命令\033[31,0m{}\033[0m...'.format(task_action), encoding='uft-8'))
                continue
            # cmd = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # cmd_res = cmd.stdout.read()
            # if not cmd_res:
            #     cmd_res = cmd.stderr.read()
            # if len(cmd_res) == 0 :
            #     cmd_res = bytes('cmd has output...', encoding='utf-8')
            # self.request.send(cmd_res)


def main():
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 8000), MyServer)
    server.serve_forever()
