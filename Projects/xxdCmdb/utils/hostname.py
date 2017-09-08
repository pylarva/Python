# !/usr/bin/env python
# -*- coding:utf-8 -*-
import paramiko
import os


def change_host_name(host_ip, host_name):
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host_ip, port=22, username='root', password='xinxindai', timeout=3)

    # 开始更新主机名
    str_host = host_ip + '    ' + host_name
    cmd = "hostname %s && echo %s > /etc/hostname && \
                echo %s >> /etc/hosts && \
                sed -i s/HOSTNAME=.*/HOSTNAME=%s/g /etc/sysconfig/network && \
                service zabbix_agentd restart && \
                service rsyslog restart &" % (host_name, host_name, str_host, host_name)
    change_host_cmd = "ssh root@%s '%s'" % (host_ip, cmd)
    os.system(change_host_cmd)
    print(change_host_cmd)

    # ssh.exec_command(cmd)
    return True