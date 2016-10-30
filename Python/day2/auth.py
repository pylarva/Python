#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
#name = "lichengbing"
#print("My name is %s !" % name)
import copy
name = [22,"linux01","linux02",[88,87,86],"Unix",22]
name2 = [1,2,3]
name2.pop() #按索引指定删除，默认为最后一个
name3 = name.copy() #拷贝列表
name4 = copy.copy(name) #浅copy（软链接）
name5 = copy.deepcopy(name) #深copy（完全拷贝）

name[0] = 100
name[3][2] = 100
'''
for i in range(name.count(22)):
    ele_index = name.index(22)
    name[ele_index] = 999
name.extend(name2)
'''
#name.reverse() #倒序输出
#name.sort() #排序

print(name)
print(name3)
print(name4)
print(name5)
