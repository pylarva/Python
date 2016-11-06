# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import zipfile

# 压缩
z = zipfile.ZipFile('z.zip', 'w')
z.write('xo.xml')
z.write('xxxoo.xml')
z.close()

# 解压
z = zipfile.ZipFile('z.zip', 'r')
for item in z.namelist():
    print(item)
# z.extractall()
z.extract('xo.xml')

import tarfile

# 压缩
tar = tarfile.open('z.tar', 'w')
tar.add('xo.xml', arcname='bbs2.log')
tar.add('xxxoo.xml', arcname='cmdb.log')
tar.close()

# 解压
tar = tarfile.open('z.tar', 'r')
# for item in tar.getmembers():
#     print(item, type(item))
obj = tar.getmember('cmdb.log')  # 和zipfile不同的是 再解压特定文件前要先获取文件特殊对象值
tar.extract(obj)
tar.close()
