# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 关键字 生产者

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs_test_1',
                         type='direct')

severity = 'error'
message = '123'

# severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
# message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(exchange='direct_logs_test_1',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()
