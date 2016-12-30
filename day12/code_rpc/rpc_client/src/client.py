# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re
import pika
import subprocess
from conf import setting

# 本地IP地址 rabbitmq服务地址
host = setting.host_ip
rabbit_host_ip = setting.rabbit_host_ip


def main():
    """
    客户端主函数 监听rabbitmq
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host_ip))
    channel = connection.channel()

    channel.exchange_declare(exchange='server', type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='server',
                       queue=queue_name)

    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)
    channel.start_consuming()


def execute_cmd(cmd):
    """
    调用 subprocess 执行命令
    """
    inp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_ret = inp.stdout.read()
    return cmd_ret


def publish_result(task_id, ret):
    """
    开始处理消息 将处理完成的消息结果重新发布回已经创建的 task_id 这个消息队列
    :param task_id: 任务ID
    :param ret:
    :return:
    """
    connection_ret = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host_ip))
    channel_ret = connection_ret.channel()
    channel_ret.queue_declare(queue=task_id)
    channel_ret.basic_publish(exchange='', routing_key=task_id, body=ret)

    print(" [x] Sent %r" % ret)
    print(" [x] Task ID: %s" % task_id)


def callback(ch, method, properties, body):
    """
    消息队列回调函数 接收到消息开始处理消息
    :param body:
    :return:
    """
    cmd_str = body.decode()
    task_id = cmd_str.split(' ')[0]
    print(cmd_str)
    print(task_id)

    # 监听到消息后 如果主机地址列表里面没有自己 则忽略该消息
    if host in cmd_str:
        cmd = re.search('\".*\"', cmd_str).group()[1:-1]
        ret = execute_cmd(cmd)
        publish_result(task_id, ret)


