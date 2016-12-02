# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import subprocess
import configparser
import socketserver
from conf import setting
from lib.decryption import decryption_pwd


class MyServer(socketserver.BaseRequestHandler):

    USER_HOME = setting.USER_HOME

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
                conn.sendall(bytes('用户名或密码错误...', encoding='utf-8'))

    def login(self, user_name, user_pwd):
        config = configparser.ConfigParser()
        config.read(setting.USER_DB, encoding='utf-8')
        user_pwd = decryption_pwd(user_pwd)
        disk_limit = config.get(user_name, 'disk_limit')

        if config.has_section(user_name) and user_pwd == config.get(user_name, 'password'):
            self.USER_HOME = os.path.join(self.USER_HOME, user_name)
            return True, disk_limit

    def session(self):

        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            print('[%s] says: %s' % (self.client_address, data.decode()))

            cmd = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
            if not cmd_res:
                cmd_res = cmd.stderr.read()
            if len(cmd_res) == 0 :
                cmd_res = bytes('cmd has output...', encoding='utf-8')
            self.request.send(cmd_res)


def main():
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 8000), MyServer)
    server.serve_forever()
