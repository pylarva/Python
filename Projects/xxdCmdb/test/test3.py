# !/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import os
import paramiko
import time
from multiprocessing import Pool
from conf import kvm_config


# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('192.168.38.200', port=22, username='root', key_filename=kvm_config.ssh_key_file, timeout=kvm_config.ssh_timeout)
# stdin, stdout, stderr = ssh.exec_command('ls')
# # stdin, stdout, stderr = ssh.exec_command("sed -i 's#111#222#g' /tmp/test.txt")
# result = stdout.read()
os.system("ssh root@192.168.38.200 'virt-copy-in -d a0-kvm-vhost-38-198.yh /opt/data/a0-kvm-vhost-38-198.yh/ifcfg-eth0 /etc/sysconfig/network-scripts/'")
# if not result:
#     print(result)
# else:
#     print(result)