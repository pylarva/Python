#!/usr/bin/env python
# coding: utf-8

import os
import sys
import subprocess
import paramiko
# from netaddr import IPNetwork

# ipaddr = IPNetwork('192.168.31.223/24')[50:60]
# for ip in ipaddr:
#     print(ip)
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


# if not os.path.exists('/tmp/aa/bb'):
#     os.makedirs('/tmp/aa/bb')
#
# os.chdir('/tmp/aa/bb')
# os.system('git init && \
#            git config remote.origin.url http://gitlab.xxd.com/service/v6_batch.git && \
#            git fetch --tags --progress http://gitlab.xxd.com/service/v6_batch.git +refs/heads/*:refs/remotes/origin/*')
# cmd = 'git rev-parse origin/master'
# ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
# out, err = ret.communicate()
# if err:
#     err = str(err, encoding='utf-8')
#     print('ERROR-->', err)
# else:
#     out = str(out, encoding='utf-8')
#     os.system('git checkout -f %s' % out)

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('192.168.31.80', port=22, username='root', password='xinxindai318', timeout=3)


# cmd = "ssh root@192.168.31.80 'python /opt/autopublishing.py /data/packages/infra/cmdb/107/v6_batch.war " \
#       "107 http://gitlab.xxd.com/service/v6_batch.git master cmdb infra'"

# cmd = "python /opt/autopublishing.py /data/packages/infra/cmdb/107/infra_cmdb_107.war 107 http://gitlab.xxd.com/service/v6_batch.git master cmdb infra"
# cmd = "python /opt/autopublishing.py /data/packages/infra/cmdb/107/v6_batch.war 107 http://gitlab.xxd.com/service/v6_batch.git master cmdb infra"

# stdin, stdout, stderr = ssh.exec_command(cmd)
#
# result = stdout.read()
# print(result)


# ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
# out, err = ret.communicate()
# print(out, err)
# ret = os.system(cmd)
# print(ret)
# ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

# ret = os.path.dirname('/data/packages/infra/cmdb/107/infra_cmdb_107.war')
# print(ret)

# pack_cmd = 'hhehehehe'
# pack_cmd = '"' + pack_cmd + '"'
# print(pack_cmd)
# pack_cmd = '/usr/local/maven/bin/mvn clean package -Dmaven.test.skip=true'
# pack_cmd = '"' + pack_cmd + '"'
# cmd = "python2.6 {0} {1} {2} {3} {4} {5} {6} {7}".format('/opt/autopublishing.py', '/data/packages/test2/v6_batch/145/v6_batch.war', '145', 'http://gitlab.xxd.com/service/v6_batch.git', '170615N', 'v6_batch', 'test2', pack_cmd)
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect('192.168.31.80', port=22, username='root', password='xinxindai318', timeout=3)
# stdin, stdout, stderr = ssh.exec_command(cmd)
# result_1 = stdin
# result_2 = stdout.read()
# result_3 = stderr.read()
#
# print(result_1, result_2, result_3)

s = 'tag/1.1.1'
if 'tag' in s:
    print('ok')