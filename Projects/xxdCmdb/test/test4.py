#!/usr/bin/env python
# coding: utf-8

import time
import random, string


# def random_str(randomlength=16):
#     """
#     生成随机字符串
#     :param randomlength:
#     :return:
#     """
#     a = list(string.ascii_letters)
#     random.shuffle(a)
#     return ''.join(a[:randomlength])
#
# s = random_str()
# print(s)
#
# t = time.strftime('%Y-%m-%d %H:%M:%S')
# print(t)

import datetime
from pytz import timezone
# from django.utils import timezone
# utc_zone = timezone("utc")
# my_zone = timezone("Asia/Shanghai")
# my_time = datetime.datetime.utcnow().replace(tzinfo=utc_zone)
# out_time = my_time.astimezone(my_zone)
# print(my_time)
# print(out_time)

# my_time = timezone.now()
# print(my_time)
# print(out_time.strftime('%Y-%m-%d %H:%M:%S'))

import os
import time
import subprocess
cmd = "ssh root@192.168.31.15 'virsh list --all'"
result = os.popen(cmd).readlines()
# result = subprocess.call(cmd, shell=True)
# print(result)

for item in result:
    print(item)