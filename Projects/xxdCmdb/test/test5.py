#!/usr/bin/env python3.6
# coding: utf-8

RET_ERROR_CHECK_SERVICE_FAILED = 100
CHECK_SERVICE_TIMEOUT = 10
retCode = 0

import os
import time
import urllib
import subprocess
from urllib import request


def checkApiService(ip):
    # retCode = RET_ERROR_CHECK_SERVICE_FAILED
    cmd = 'ps -ef | grep java | wc -l'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    out, err = p.communicate()
    out = str(out, encoding='utf-8')
    print(out.split()[0])
    if out.split()[0] == '2':
        print('no start...')
        return RET_ERROR_CHECK_SERVICE_FAILED
    else:
        # curl 检查服务是否正常
        total_time = CHECK_SERVICE_TIMEOUT
        while total_time > 0:
            total_time -= 1
            time.sleep(1)
            cmd = "curl -I -m 2 %s:8080" % ip
            ret = os.system(cmd)
            if ret == 0:
                return 0
            else:
                continue
        return RET_ERROR_CHECK_SERVICE_FAILED

if __name__ == '__main__':
    ret = checkApiService('192.168.33.110')
    print(ret)

# u = urllib.request.urlopen('http://www.lichengbing.cn', data=None, cafile=None, capath=None, cadefault=False, context=None)
# ret_code = u.getcode()
# print(ret_code)

# cmd = "curl -I -m 2 192.168.34.110:8080"
# ret = os.system(cmd)
# print(ret)





