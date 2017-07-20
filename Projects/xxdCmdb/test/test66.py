#!/usr/bin/env python
# coding: utf-8

# 666
import json
import requests

auth_key = 'vLCzbZjGVNKWPxqd'

msg = {'id': 353, 'msg': 'a test message...'}
msg = json.dumps(msg)
response = requests.post(
    url='http://127.0.0.1:8005/api/release',
    headers={'key': auth_key},
    json=msg,
)

print(response.text)