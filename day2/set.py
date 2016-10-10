#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 创建一个集合
se1 = {11,22}
print(type(se1))
se2 = set([22,33])
# li = []
# list((11,22)) 创建列表的时候调用 __init__,内部执行for循环里面的元组tuple

# 操作集合

# 增加
se1.add(44)

# A存在B不存在
se3 = se1.difference(se2)

# A有B无 B有A无
se4 = se1.symmetric_difference(se2)

# 更新se1
# se1.difference_update(se2)

# 移除(不存在不报错)
#se1.discard(11)
# remove（不存在报错）
#se1.remove(11)
# 随机移除(返回移除的元素,这里pop里面不能加参数，而list里面pop可以有参数)
ret = se1.pop()

# 交集
se5 = se1.intersection(se2)

# 合并并集
se6 = se1.union(se2)

# update(接受一个可以被迭代的对象)
lii = [11,2,3]
# se8 = se1.update(lii)
se1.update(lii)
se7 = se1

print(se7)