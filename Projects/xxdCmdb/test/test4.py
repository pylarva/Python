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

# import os
import time
import subprocess
# cmd = "ssh root@192.168.31.15 'virsh list --all'"
# result = os.popen(cmd).readlines()
# result = subprocess.call(cmd, shell=True)
# print(result)

# for item in result:
#     print(item)

import jenkins

jenkins_server_url = 'http://192.168.31.80:8080'
user_id = 'sa'
api_token = '9e235779d590f7c63d45201bb8c969be'

server = jenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)
info = server.get_whoami()['fullName']
print(info)

param_dict = {"pkgUrl": '/data/packages/infra/cmdb/112/infra_test_112.zip', "git_url": 'http://gitlab.xxd.com/service/v6_batch.git', 'branch': 'master'}

build_name = 'template-tomcat'

# ret = server.build_job(build_name, parameters=param_dict)
# time.sleep(15)
LastBuild = server.get_job_info(build_name)['lastBuild']['number']
result = server.get_build_info(build_name, LastBuild)['url']
log = server.get_build_console_output(build_name, LastBuild)

# while result is None:
#     time.sleep(5)
#     result = server.get_build_info(build_name, LastBuild)['result']

print(LastBuild, result)
# print(log)
# print(ret)