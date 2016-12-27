# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import pika
# connection 一个TCP的连接、
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

#  channel 是建立在TCP连接中的一个虚拟连接
channel = connection.channel()

# 创建一个queue
channel.queue_declare(queue='hello')

# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()