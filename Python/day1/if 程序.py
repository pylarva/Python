#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

user = 'lichengbing'
passwd = 'li123456'

username = input("username:")
password = input("password:")

if user == username:
    print("username is correct...")
    if password == passwd:
        print("Welcome login...")
    else:
        print("password is invalid...")
else:
    print("用户名都没对...滚粗..")