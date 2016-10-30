# ！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# import json
#
# li = [11, 22, 33]
# # dump先写文件
# json.dump(li, open('db', 'w'))
# # load从文件读再loads
# li1 = json.load(open('db', 'r'))
# print(type(li1), li1)


import pickle
# pickle 只能Python识别 不适用于别的语言
# li = [11, 22, 33]
# r = pickle.dumps(li)
# print(r)
#
# result = pickle.loads(r)
# print(result)

li = [11, 22, 33]
pickle.dump(li, open('db1', 'wb'))
result = pickle.load(open('db1', 'rb'))
print(result, type(result))

# json/pickle 区别1

# json更加适合跨语言 字符串 基本数据类
# pickle 处理Python复杂类型的序列化 缺点是仅适用于Python
