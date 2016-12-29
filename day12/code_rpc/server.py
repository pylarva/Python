# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re
import pika


def publish_message(cmd, host_list):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
    channel = connection.channel()
    channel.exchange_declare(exchange='server',
                             type='fanout')
    severity = host_list

    channel.basic_publish(exchange='server', routing_key='', body=cmd)
    print(" [x] Sent %r" % cmd)

print('   \033[32;0m>> 主机管理 <<\033[0m   '.center(60, '-'))
print('\033[32;0m命令示例：\033[0m \033[31;0m run "df -h" --hosts 192.168.3.55 10.4.3.4\033[0m')

host_list = []
while True:
    inp = input('>>>: ')
    if not inp: continue
    if not re.match('run \".*\" --hosts (25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}', inp):
        print('cmd error...')
    else:
        host_list = inp.split(' ')[3:]
        publish_message(inp, host_list)

