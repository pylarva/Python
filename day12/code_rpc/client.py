# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re
import pika
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
channel = connection.channel()

channel.exchange_declare(exchange='server', type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='server',
                   queue=queue_name)

host = '10.0.0.1'
# host = bytes(host, encoding='utf-8')

print(' [*] Waiting for logs. To exit press CTRL+C')


def execute_cmd(cmd):
    inp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_ret = inp.stdout.read()
    return cmd_ret


def publish_result(task_id ,ret):

    connection_ret = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
    channel_ret = connection_ret.channel()
    channel.queue_declare(queue=task_id)
    channel_ret.basic_publish(exchange='', routing_key=task_id, body=ret)

    print(" [x] Sent %r" % ret)
    print(" [x] Task ID: %s" % task_id)


def callback(ch, method, properties, body):
    cmd_str = body.decode()
    task_id = cmd_str.split(' ')[0]
    print(cmd_str)
    print(task_id)
    if host in cmd_str:
        cmd = re.search('\".*\"', cmd_str).group()[1:-1]
        ret = execute_cmd(cmd)
        publish_result(task_id, ret)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()