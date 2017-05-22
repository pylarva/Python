#!/usr/bin/env python
# coding: utf-8

# 666
import json
import time
import requests

auth_key = 'vLCzbZjGVNKWPxqd'

# response = requests.get(
#     url='http://127.0.0.1:8005/api/asset',
#     headers={'key': key}
# )
# time = time.strftime('%Y%m%d %H:%M')

msg = {'id': 110, 'msg': 'a test message...'}
msg = json.dumps(msg)
response = requests.post(
    url='http://127.0.0.1:8005/api/release',
    headers={'key': auth_key},
    json=msg,
)

print(response.text)