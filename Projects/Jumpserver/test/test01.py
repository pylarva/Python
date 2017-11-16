# !/usr/bin/env python3.6
# -*- coding:utf-8 -*-]

import docker

image = 'centos'
# host = '172.16.1.136'
host = '192.168.38.56'

c = docker.Client(base_url='tcp://%s:2375' % host, version='auto', timeout=10)

containers_list = c.containers(quiet=False, all=False, trunc=True, latest=False, since=None,
                               before=None, limit=-1)
# for i in containers_list:
#     print(i['Id'])

host_config = c.create_host_config(binds={'/opt/docker': {'bind': '/data', 'ro': False},
                                          '/var/www': {'bind': '/mnt/vol1', 'ro': True}},
                                   mem_limit='1g', cpu_period=100000, cpu_quota=200000)

c_ret = c.create_container(image, command='/bin/bash', hostname='dev-ubuntu', user=None,
                           detach=True, stdin_open=True, tty=True,
                           ports=None, environment=None, dns=None,
                           volumes=['/opt/docker', '/var/www'],
                           host_config=host_config,
                           volumes_from=None, network_disabled=False, name='ubuntu01',
                           entrypoint=None, cpu_shares=None, working_dir=None)

c.start(c_ret['Id'])
