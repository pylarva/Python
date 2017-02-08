# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import redis

r = redis.Redis(host='10.0.0.111', port=6379)
r.set('foo', 'Bar')
print(r.get('foo'))

