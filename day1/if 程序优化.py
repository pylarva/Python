#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

user = 'lichengbing'
passwd = 'li123456'

username = input("username:")
password = input("password:")

if user == username and password ==passwd:
   print("Welcome Login...")
else:
    print("Invalid username or password..")