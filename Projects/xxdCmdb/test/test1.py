#!/usr/bin/env python
# coding: utf-8

import os
import subprocess


cmd = "ssh root@192.168.31.80 'python /opt/autopublishin.py %s %s'" % ('/data/packages/infra/cmdb/77/infra_cmdb_77.war', '77')
# ret = os.system(cmd)
# rett = os.popen(cmd)
# msg = rett.read()
# print(msg)

ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True, preexec_fn=os.setsid)

out, err = ret.communicate()
err = str(err, encoding='utf-8')
print(err)