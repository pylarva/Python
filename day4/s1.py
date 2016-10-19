#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


# 1、定义的函数是否可以被调用执行
#callable()

# 2、ACSII码转换数字
#print(chr(65))
#print(ord('A'))

# 3、生成随机验证码
# import random
# li = []
# for i in range(6):
#     r = random.randrange(0, 5)
#     if r == 2 or r == 4:
#         num = random.randrange(0, 9)
#         li.append(str(num))
#     else:
#         temp = random.randrange(65, 91)
#         c = chr(temp)
#         li.append(c)
# result = "".join(li)  # 使用join时元素必须是字符串
# print(result)

# 4、Python先编译后执行
# 编译， 单行single, 表达式eval, 和Python一样的格式exec
# 将字符串编译成Python代码
# compile()
# 执行
# eval()
# exec()
# s = "print(123)"
# r = compile(s, "<string>", "exec")  # 将字符串编译成Python代码
# exec(r)

# exec 和 eval 都可以执行，通常exec功能更强大（可以接受代码或者字符串）
# 但是 eval 有返回值，exec没有
# s = "8*8"
# ret = eval(s)
# print(ret)

# 5、查看对象提供的功能
# print(dir(dict))
# help(list) # 读模块源码

# 6、共97，每页显示10条，需要都少页
# r = divmod(97, 10)
# n1, n2 = divmod(97, 10)
# print(n1, n2)

# 7、判断某一对象是否是某类的实例
# s = [1,2,3]
# print(isinstance(s, list))

# 8、筛选函数
# filter(函数， 可迭代对象)
def f2(a):
    if a>22:
        return True
li = [11, 22, 33]
ret = filter(f2, li)
print(list(ret))