#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# abs取绝对值
n = abs(-1)
print(n)

# all() 所有元素为真则为真
n = all([1, 2, 3, 4])
print(n)
# any() 只要有真则为真
n = any([1, 0, None])
print(n)

# ascii() 自动执行对象的__repr__方法

# bin() 10进制转换成2进制
# oct() 10进制转换成8进制
# hex() 10进制转换成16进制

# bool值
# 0,None,"",[],{},() 都为False
print(bool(0))

# bytes()字符串转换字节类型
# bytearray()字符串转换字节生成列表
# utf-8 一个汉字占用3个字节
# gbk 一个汉字占用2个字节
s = "李杰"
n = bytes(s, encoding="utf-8")
print(n)

# 将字节转换成字符串
n = str(bytes(s, encoding="utf-8"), encoding="utf-8")
print(n)