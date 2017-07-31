#!/usr/bin/env python
# coding: utf-8

# 666
import os
import json
import requests
import subprocess
import urllib.request

cmd = 'cd /Users/pylarva/github/Python/Projects/xxdCmdb/scr/ && python2.6 cdn.py Action=RefreshObjectCaches ObjectType=File ObjectPath=https://download-cdn.xinxindai.com/'
ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
out, err = ret.communicate()
url = str(out, encoding='utf-8')
cmd = 'curl -I %s' % url
print(cmd)
# os.system(cmd)

ret = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
out, err = ret.communicate()
print(out)

# f = urllib.request.urlopen(url)
# print(f.read())