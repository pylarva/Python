#!/usr/bin/env python
# -*- coding:utf-8 -*-

name = input("input you name:")
age = int(input("input you age:"))
job = input("input you job:")

msg = '''
Infomation of user name:%s:
--------------
Name:  %s
Age:   %d
Job:   %s
------END-----
''' % (name,name,age,job)
print(msg)

'''
name = "lichengbing" # This is a variable
age = 21
print(name,age)
'''