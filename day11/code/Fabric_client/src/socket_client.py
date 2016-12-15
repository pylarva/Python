# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import json
import subprocess
import socketserver
from conf import setting
from lib.decryption import file_md5


class MyServer(socketserver.BaseRequestHandler):
    """
    多用户socket会话类
    """
    # 静态字段 用户上传文件默认路径
    CURRENT_PATH = '/tmp/'

    def handle(self):
        """
        主 handle 函数：用户连接
        :return:
        """
        conn = self.request
        if self.client_address[0] == setting.master_address:
            cmd = subprocess.Popen('hostname'.format(self.CURRENT_PATH), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            cmd_res = cmd.stdout.read()
            print(cmd_res.decode())
            conn.send(cmd_res)
            self.session()
        else:
            conn.send(bytes('deny', encoding='utf-8'))

    def breakpoint(self, file_name):
        """
        断点续传判断文件存在及大小
        :param file_name:
        :return:
        """
        file = os.path.join(self.CURRENT_PATH, file_name)
        if os.path.exists(file):
            read_size = os.stat(file).st_size
        else:
            read_size = 0
        return read_size

    def task_put(self, *args, **kwargs):
        """
        执行用户上传文件方法
        :param args:
        :param kwargs:
        :return:
        """
        print('---put', args, kwargs)
        file_name = args[0].get('file_name')
        file_size = args[0].get('file_size')

        read_size = self.breakpoint(file_name)
        if read_size != 0 :
            recv_size = read_size
        else:
            recv_size = 0

        server_response = {'status': 200, 'read_size': read_size}
        self.request.send(bytes(json.dumps(server_response), encoding='utf-8'))
        print(server_response)
        f = open(os.path.join(self.CURRENT_PATH, file_name), 'ab+')

        while recv_size < file_size:
            data = self.request.recv(4096)
            f.write(data)
            recv_size += len(data)
        print('File recv success!')
        f.close()

        md5_hash = file_md5(os.path.join(self.CURRENT_PATH, file_name))
        self.request.send(bytes(md5_hash, encoding='utf-8'))

    def task_pull(self, *args):
        """
        执行用户下载文件方法
        :param args:
        :return:
        """
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

            read_size = confirm_data['read_size']
            if read_size != 0:
                recv_size = read_size
            else:
                recv_size = 0

            if confirm_data['status'] == 200:
                print('Start sending file \033[31;0m{}\033[0m!'.format(msg_data['file_name']))
                f = open(file, 'rb')
                f.seek(recv_size, 0)
                for line in f:
                    self.request.send(line)
                print('Send file done!')

                md5_hash = file_md5(file)
                self.request.send(bytes(md5_hash, encoding='utf-8'))

        else:
            print('\033[31;0m{}\033[0m文件不存在...'.format(file_name))

    def session(self):
        """
        用户登陆验证成功后开始会话
        :return:
        """
        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            print('[%s] says: %s' % (self.client_address, data.decode()))

            try:
                task_data = json.loads(data.decode())
                task_action = task_data.get('action')

            except Exception:
                cmd = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                cmd_res = cmd.stdout.read()
                if not cmd_res:
                    cmd_res = cmd.stderr.read()
                if len(cmd_res) == 0:
                    cmd_res = bytes('cmd has output...', encoding='utf-8')
                self.request.send(cmd_res)
            else:
                if task_action == 'put':
                    self.task_put(task_data)
                elif task_action == 'pull':
                    self.task_pull(task_data)


def main():
    """
    多用户连接方法对象创建
    :return:
    """
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 8000), MyServer)
    server.serve_forever()
