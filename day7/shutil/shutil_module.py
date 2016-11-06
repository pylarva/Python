# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import shutil

# 拷贝文件内容
shutil.copyfileobj(open('old.xml', 'r'), open('new.xml', 'w'))

# 拷贝文件
shutil.copyfile('f1.log', 'f2.log')

# 拷贝权限
shutil.copymode('f1.log', 'f2.log')

# 拷贝文件状态信息
shutil.copystat('f1.log', 'f2.log')

# 拷贝文件和权限
shutil.copy('f1.log', 'f2.log')

# 递归地拷贝文件夹
# shutil.copytree('folder1', 'folder2', ignore=shutil.ignore_patterns('*.pyc', '*.txt'))

# 递归地删除文件
# shutil.rmtree('folder2')

# 递归地移动重命名文件
# shutil.move('folder2', 'folder3')

# 打包文件
ret = shutil.make_archive(r'C:\GitHub\Python\day7\shutil\www', 'gztar', root_dir=r'C:\GitHub\Python\day7\shutil\folder1')


