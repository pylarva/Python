# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    '10.0.0.111'))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
channel.queue_declare(queue='hello')


# ch 管道内存地址
# 回调函数
def callback(ch, method, properties, body):
    print("---->", ch, method, properties)
    print(" [x] Received %r" % body)

    channel.queue_declare(queue='hello_1')

    channel.basic_publish(exchange='',
                          routing_key='hello_1',
                          body='hello_1!')
    print(" [x] Sent 'hello_1'")

# 开始消费消息
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True  # 不确认消息
                      )
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


channel.queue_declare(queue='hello_1')

channel.basic_publish(exchange='',
                      routing_key='hello_1',
                      body='hello_1!')
print(" [x] Sent 'hello_1'")