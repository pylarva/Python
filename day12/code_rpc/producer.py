# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import pika
# connection 一个TCP的连接、
connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.111'))

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

connection = pika.BlockingConnection(pika.ConnectionParameters('10.0.0.111'))
channel = connection.channel()
channel.queue_declare(queue='hello_1')


def callback(ch, method, properties, body):
    print("---->", ch, method, properties)
    print(" [x] Received %r" % body)
    connection.close()

channel.queue_declare(queue='hello_1')

# 开始消费消息
channel.basic_consume(callback,
                      queue='hello_1',
                      no_ack=True  # 不确认消息
                      )

channel.start_consuming()

