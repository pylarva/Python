#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# 打开文件
# f = open('db', 'r')  # 只读
# f = open('db', 'w')  # 只写，先清空
# f = open('db', 'x')  # python 3.0 新加（如果文件存在报错，不存在则创建并写内容）
# f = open('db', 'a')  # 追加
# f = open('db', 'r', encoding="utf-8")  # 指定字符编码，防止乱码
# f = open('db', 'rb')  # 以二进制打开

# r+ 能调整写文件指针位置,其他的总是写到末尾
# a+ 能读，但是写文件只能在末尾添加
# w+ 会先清空文件再写
f = open('db', 'r+', encoding="utf-8")  # 如果模式没有加 b 默认按照一个字符读取数据
data = f.read(1)
f.seek(3)   # 调整文件指针到执行位置（以字节方式查找）
print(f.tell())
f.write("777")  # 会覆盖已经存在的元素

# 操作文件
f.read()  # 无参数默认读全部;有参数（b按字节;无b按字符）
f.tell()  # 查看指针位置
f.seek()  # 按字节调整指针位置
f.write()  # 写文件
f.close()  # 关闭
f.fileno()  # 文件的描述符
f.flush()  # 强刷文件到硬盘
f.readable()  # 是否可读
f.readline()  # 仅读取一行
f.truncate()  # 截断指针后面的所有数据

# for循环文件对象
for line in f:
    print(line)

# 关闭文件
f.close()
with open('db') as f:
    pass
# 同时打开两个文件
with open('db01') as f1, open('db02') as f2:
    pass
