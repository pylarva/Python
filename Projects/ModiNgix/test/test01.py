# !/usr/bin/env python
# -*- coding:utf-8 -*-

from crontab import CronTab
import paramiko

crontab_host = '192.168.33.110'

crontab_user = 'root'
crontab_pwd = 'xinxindai318'

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(crontab_host, 22, crontab_user, crontab_pwd, timeout=10)
#
# stdin, stdout, stderr = ssh.exec_command('crontab -l')
#
# stdout_res = stdout.read()
# stderr_res = stderr.read()

# t = paramiko.Transport(crontab_host, 22)
# t.connect(username=crontab_user, password=crontab_pwd)
# sftp = paramiko.SFTPClient.from_transport(t)
# src = '/var/spool/cron/root'
# des = '/opt/root'
# sftp.get(src, des)
# sftp.put(des, src)
# t.close()

file = '/opt/root'

with open(file, "a+") as f:
    f.write('22222\n')







