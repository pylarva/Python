#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
from netaddr import IPNetwork

ipaddr = IPNetwork('192.168.31.223/24')[50:60]
for ip in ipaddr:
    print(ip)
# ip_list = list(ipaddr)
# print(ip_list)
#     s = subprocess.call("ssh root@192.168.31.110 'ping -c1 -W 1 %s > /dev/null'" % ip, shell=True)
#     print(s)


# cmd = "ssh root@192.168.31.80 'python /opt/autopublishin.py %s %s'" % ('/data/packages/infra/cmdb/77/infra_cmdb_77.war', '77')
# ret = os.system(cmd)
# rett = os.popen(cmd)
# msg = rett.read()
# print(msg)

# ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True, preexec_fn=os.setsid)
#
# out, err = ret.communicate()
# err = str(err, encoding='utf-8')
# print(err)

# user = 'admin'
# cmd = '/usr/local/tomcat/bin/shutdown.sh'
# cmd = "su - %s -c '%s'" % (user, cmd)
# popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
#                          stderr=subprocess.STDOUT, shell=True, preexec_fn=os.setsid)
# killProc = lambda pid: os.killpg(pid, signal.SIGKILL)
# timer = Timer(timeout, killProc, [popen.pid])
# timer.start()
# popen.wait()
# output = popen.stdout.read()
# timer.cancel()

