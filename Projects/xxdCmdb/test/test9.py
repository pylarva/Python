# !/usr/bin/env python
# -*- coding:utf-8 -*-
import queue
import subprocess
from netaddr import IPNetwork
from conf import kvm_config
from concurrent.futures import ThreadPoolExecutor

host_machine = '192.168.38.200'
q = queue.Queue()


def func_get_ip(ip):
    """
    多线程抓取IP
    :param url:
    :return:
    """
    # host_machine = '192.168.38.200'

    # print(host_machine, ip)
    s = subprocess.call("ssh root@%s 'ping -c1 -W 1 %s > /dev/null'" % (host_machine, ip), shell=True)
    if s != 0:
        q.put(ip)
        return ip


def callback1(ip):
    if ip:
        q.put(ip)

pool = ThreadPoolExecutor(10)
ipaddr = IPNetwork('%s/24' % host_machine)[kvm_config.kvm_range_ip[0]:kvm_config.kvm_range_ip[1]]
for ip in ipaddr:
    v = pool.submit(func_get_ip, str(ip))
    # v.add_done_callback(callback1)

pool.shutdown(wait=True)
try:
    new_ip = q.get(block=True, timeout=10)
    if new_ip:
        print(new_ip)
except Exception as e:
    print('not find....')

# pool.shutdown(wait=True)





