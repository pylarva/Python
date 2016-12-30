# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import re
import pika
import random
import threading
from conf import setting

# rabbit 服务地址
rabbit_host_ip = setting.rabbit_host_ip
# 创建一个保存执行命令结果的字典
message_dic = {}


def publish_message(cmd):
    """
    发布消息 并且创建队列名称是 任务ID 的队列 用户接收返回的执行结果
    :param cmd:
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host_ip))
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
    """
    消息回调函数
    :param method:
    :param body:
    :return:
    """
    body = body.decode()
    # 我们需要得到 任务ID 将结果发回这个ID的队列
    routing_key = re.search('routing_key=\d+', str(method)).group()[-4:]
    global message_dic

    # 将消息添加进字典
    if not message_dic.get(routing_key):
        message_dic[routing_key] = []
        message_dic[routing_key].append(body)
    else:
        message_dic[routing_key].append(body)


def receive_message(arg):
    """
    接收命令执行结果
    :param arg:
    :return:
    """
    arg = str(arg)
    connection_1 = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host_ip))
    channel_1 = connection_1.channel()
    channel_1.queue_declare(queue=arg)
    channel_1.basic_consume(callback, queue=arg, no_ack=True)
    channel_1.start_consuming()


def check_task(task_id):
    """
    查看命令执行结果
    :param task_id:
    :return:
    """
    if not message_dic.get(task_id):
        print('Task get nothing...')
    else:
        for item in message_dic.get(task_id):
            print(item)


def main():
    """
    主函数 发布消息和 检查命令执行结果
    :return:
    """
    print('   \033[32;0m>> 主机管理 <<\033[0m   '.center(60, '-'))
    print('\033[32;0m命令示例：\033[0m \033[31;0m run "df -h" --hosts 192.168.3.55 10.4.3.4\033[0m\n'
          '\033[32;0m读取任务：\033[0m \033[31;0m check ID\033[0m')

    while True:
        inp = input('>>>: ')
        if not inp: continue

        # 命令结果查看
        if inp.split(' ')[0] == 'check':
            task_id = inp.split(' ')[1]
            check_task(task_id)
            continue

        # 命令有效性检查
        if not re.match('run \".*\" --hosts (25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}', inp):
            print('cmd error...')
        else:
            task_id = publish_message(inp)

            # 创建一个线程去接收命令执行结果 主线程继续运行
            t = threading.Thread(target=receive_message, args=(task_id,))
            t.start()




