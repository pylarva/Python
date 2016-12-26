# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# memcached 操作

import memcache

# debug=True 表示显示运行时错误信息 上线后可移除
# mc = memcache.Client([('10.0.0.104:11211', 1), ('10.0.0.111:11211', 1)], debug=True)
mc = memcache.Client(['10.0.0.111:11211'], debug=True)
# mc.set('k1', 'v1')
ret = mc.get('k1')
print(ret)

