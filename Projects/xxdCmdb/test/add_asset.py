#!/usr/bin/env python
# coding: utf-8

import re
import json
import hashlib
import requests

ASSET_AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'
ASSET_API = "http://cmdb.xxd.com/api/asset"
# ASSET_API = "http://0.0.0.0:8005/api/asset"


def auth_key():
    """
    接口认证
    :return:
    """
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s" % ASSET_AUTH_KEY, encoding='utf-8'))
    encryption = ha.hexdigest()
    result = "%s" % encryption
    # 返回字典key好像只能是AUTH 否则request.environ里面添加失败
    return {"AUTH": result}


def post_api(ip):
    """
    向cmdb.xxd.com添加 容器资产IP
    calback: 1000成功 1001 API授权失败 1002 IP已存在
    :param ip:
    :return:
    """
    headers = {}
    headers.update(auth_key())
    try:
        response = requests.post(
            url=ASSET_API,
            headers=headers,
            json=json.dumps({'docker': ip})
        )
        print(json.loads(response.text)['message'])
    except Exception as e:
        print('[%s]连接失败...' % ASSET_API)
        return False

while True:
    print('------ cmdb.xxd.com添加容器资产 ------')
    ip = input('输入新增docker容器的IP地址[0 退出]:')
    if ip == "0":
        exit()
    if not re.match('^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$', ip):
        print('IP地址非法...')
        continue
    post_api(ip) if ip else print('重新输入')



