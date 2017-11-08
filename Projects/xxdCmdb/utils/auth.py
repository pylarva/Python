#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import hashlib
# from AutoCmdb.settings import ASSET_AUTH_HEADER_NAME
# from AutoCmdb.settings import ASSET_AUTH_KEY
# from AutoCmdb.settings import ASSET_AUTH_TIME
from django.http import JsonResponse

ENCRYPT_LIST = [
    # {'encrypt': encrypt, 'time': timestamp
]
ASSET_AUTH_TIME = ''
ASSET_AUTH_KEY = '299095cc-1330-11e5-b06a-a45e60bec08b'


def api_auth_method(request):
    auth_key = request.META.get('HTTP_AUTH_KEY')
    if not auth_key:
        return False
    sp = auth_key.split('|')
    if len(sp) != 2:
        return False
    encrypt, timestamp = sp
    timestamp = float(timestamp)
    limit_timestamp = time.time() - ASSET_AUTH_TIME
    print(limit_timestamp, timestamp)
    if limit_timestamp > timestamp:
        return False
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s|%f" % (ASSET_AUTH_KEY, timestamp), encoding='utf-8'))
    result = ha.hexdigest()
    print(result, encrypt)
    if encrypt != result:
        return False

    exist = False
    del_keys = []
    for k, v in enumerate(ENCRYPT_LIST):
        print(k, v)
        m = v['time']
        n = v['encrypt']
        if m < limit_timestamp:
            del_keys.append(k)
            continue
        if n == encrypt:
            exist = True
    for k in del_keys:
        del ENCRYPT_LIST[k]

    if exist:
        return False
    ENCRYPT_LIST.append({'encrypt': encrypt, 'time': timestamp})
    return True


def api_auth(func):
    def inner(request, *args, **kwargs):
        if not api_auth_method(request):
            return JsonResponse({'code': 1001, 'message': 'API授权失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)
    return inner


def api_auths_method(request):
    """
    对比 HTTP_AUTH_KEY MD5值
    :param request:
    :return:
    """
    # print(request.environ)
    auth_key = request.META.get('HTTP_AUTH')
    ha = hashlib.md5(ASSET_AUTH_KEY.encode('utf-8'))
    ha.update(bytes("%s" % ASSET_AUTH_KEY, encoding='utf-8'))
    result = ha.hexdigest()
    if auth_key != result:
        return False
    else:
        return True


def api_auths(func):
    """
    客户端上报资产HTTP认证
    1000 认证成功
    1001 授权失败
    1002 资产已存在
    :param func:
    :return:
    """
    def inner(request, *args, **kwargs):
        if not api_auths_method(request):
            return JsonResponse({'code': 1001, 'message': 'API授权失败'}, json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)
    return inner