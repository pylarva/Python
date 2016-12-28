# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# SSHclient 封装 transport

import paramiko

transport = paramiko.Transport(('www.lichengbing.cn', 22))
transport.connect(username='root', password='123456')

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('df')
print(stdout.read())

transport.close()