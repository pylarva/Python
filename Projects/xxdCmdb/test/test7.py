#!/usr/bin/env python
# coding: utf-8

from string import Template

# 用$符号进行格式化 替换单词内部要用大括号{} 输出$符号要转义
s1 = Template("$who likes $what..")
s2 = Template("${who}likes $what..")
s3 = Template("$$$who likes $what..")
print(s1.substitute(who='Snow', what='Ygritte'))
print(s2.substitute(who='Snow', what='Ygritte'))
print(s3.substitute(who='Snow', what='Ygritte'))


d = dict(who='Snow')
# substitute比较严格 要求每一个占位符都要找到变量 否则报错; 而safe_substitute如果没找到变脸 直接将$100原样输出
print(Template("$who need $100.").safe_substitute(who="Snow"))
print(Template("$who need $100.").substitute(who="Snow"))


