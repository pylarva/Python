# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re
import pika
import random
import threading


def publish_message(cmd, host_list):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
    channel = connection.channel()
    channel.exchange_declare(exchange='server',
                             type='fanout')

    task_id = random.randrange(1000, 9999)
    message = '{} {}'.format(str(task_id), cmd)

    channel.basic_publish(exchange='server', routing_key='', body=message)

    print(" [x] Sent %r" % message)
    print(" [x] Task ID: %s" % task_id)
    return task_id


def callback(ch, method, properties, body):
    print(body)


def receive_message(arg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
    channel = connection.channel()

    channel.queue_declare(queue=arg)

    channel.basic_consume(callback,
                          queue=arg,
                          no_ack=True)
    channel.start_consuming()

print('   \033[32;0m>> 主机管理 <<\033[0m   '.center(60, '-'))
print('\033[32;0m命令示例：\033[0m \033[31;0m run "df -h" --hosts 192.168.3.55 10.4.3.4\033[0m')


host_list = []
while True:
    inp = input('>>>: ')
    if not inp: continue
    if not re.match('run \".*\" --hosts (25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}', inp):
        print('cmd error...')
    else:
        host_list = inp.split('hosts ')[-1].split(' ')
        task_id = publish_message(inp, host_list)
        t = threading.Thread(target=receive_message, args=(task_id, ))
        t.start()


