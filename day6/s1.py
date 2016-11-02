# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
"""
一行注释
"""
#  模块

import s2
import sys
import time

# print(vars(s2))
# print(s2.__dict__)

# __doc__  #  注释用
# __file__  # 当前py文件所在路径
# __cached  # 自解码pyc缓存文件
# __name__  # 只有执行当前文件时候 当前文件的特殊变量__name__ == "__main__"
# __package__  # 属于哪个包文件

# from bin import admin
# print(admin.__package__)


# sys 模块
# print(sys.platform)

# 进度条
# def view_bar(num, total):
#     rate = num / total
#     rate_num = int(rate * 100)
#     r1 = '\r%s>%d%%' % ("="*num, rate_num,)  # 加 r 的话让每次输出回到初始最前面位置
#     sys.stdout.write(r1)  # 和print的区别就是不加换行符
#     sys.stdout.flush()  # 清空屏幕输出
#
# for i in range(0, 101):
#     time.sleep(0.1)
#     view_bar(i, 100)

# os 模块
# 自己看

# 加密模块

# hashlib

# import hashlib
#
# obj = hashlib.md5(bytes('sdfsdfsadf', encoding='utf-8'))  # 加bytes任意字符防止被撞库破译
# obj.update(bytes('123', encoding='utf-8'))
# r = obj.hexdigest()
# print(r)


# 正则表达式

import re

# print(re.findall('ko.{1,3}e', 'sdfsfwerekobbbesdkobef'))  # 返回一个列表
# 反斜杠
# print(re.search("\\\\com", "\comcn").group())
# print(re.findall('ko[\d]e', 'sdfsfwereko2esdkobef'))
# 元字符 . ^ $ * + ? {}
# 单词
# print(re.findall(r'I\b', 'I&am Ikobe'))

# 分组
# 去已经匹配到的数据中再提取数据
# origin = 'has sdfsdfsdfwer432'
# r = re.match("h\w+", origin)
# r = re.match("h(\w+)", origin)
# r = re.match("h(?P<name>\w+)", origin)
# print(r.group())
# print(r.groups())
# print(r.groupdict())

# findall 分组
# origin = "hasaabc halaaabc"
# r = re.findall("h(\w+)a(ab)c", origin)  # 首先整体匹配 再将分组放入结果
# print(r)

# spilt 分组
# origin = "hello alex abc alex age"
# r = re.split("a(le)x", origin, 1)  # 忽略了alex 直接匹配le
# print(r)


# match
# print(re.match('com', 'comwww.runcombb').group())  # match 匹配起始位置
# print(re.search('com', 'www.runcombb').group())  # search 匹配第一次位置

# sub subn 匹配 替换
# print(re.sub("g.t", "have", 'I get A, get B', 1))  # 1表示只替换1次
# print(re.subn("g.t", "have", 'I get A, get B'))  # 提示替换了几次

# split
# print(re.split('\d+', 'one1two2three3four4'))  # 有空格

# compile 封装一个固定匹配规则供多次调用
# s = "JGood is a boy,so cool..."
# r = re.compile(r'\w*oo\w*')   # 查找所有包含oo的单词
# print(r.findall(s))






