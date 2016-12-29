# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.0.0.111'))
channel = connection.channel()

channel.exchange_declare(exchange='server', type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='server',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()