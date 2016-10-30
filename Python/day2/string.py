#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

n_arg = {'name':'lichengbing','age':25}
n = 'My name is {name} and age is {age}'
#print(n.format_map(n_arg))

n1 = 'Hello World'
#print(n1.rjust(40,"-"))

s = "Hello World!"
p = str.maketrans("abcdefg","3!@#$%^")
#print(s.translate(p))

b="ddefdsdff_哈哈"
print(b.isidentifier()) #检测一段字符串可否被当作标志符，即是否符合变量命名规则

