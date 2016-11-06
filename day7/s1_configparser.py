# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

# configparser 模块
# 用于处理特定格式的文件 实质上是通过open来操作文件

import configparser

# 1、读取文件 读取节点
config = configparser.ConfigParser()
config.read('conf_file', encoding='utf-8')
ret = config.sections()  # 获取所有节点 返回一个列表
ret1 = config.items('section1')  # 读取节点下的键值对
ret2 = config.options('section1')  # 读取某个节点下的键

print(ret)
print(ret1)
print(ret2)

# 2、读取节点键值
v = config.get('section1', 'k1')  # 获取指定key下的值 默认 str 类型
# v = config.getint('section1', 'k1')
# v = config.getfloat('section1', 'k1')
# v = config.getboolean('section1', 'k1')
print(v, type(v))

# 3、检查 添加 删除节点
has_sec = config.has_section('section1')
print(has_sec)

# config.add_section('section5')
# config.write(open('conf_file', 'w'))

# config.remove_section('section3')
# config.write(open('conf_file', 'w'))

# 4、检查 删除 设置 指定组内的键值对
has_opt = config.has_option('section1', 'k1')
print(has_opt)

# config.remove_option('section2', 'k3')
# config.write(open('conf_file', 'w'))

config.set('section5', 'k1', '123')
config.write(open('conf_file', 'w'))






