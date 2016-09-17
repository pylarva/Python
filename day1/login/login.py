#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os,sys,getpass

os.system('cls')

file_user = open('user.txt','r+')
file_lock = open('user_lock.txt','r+')
user_list = file_user.readlines()
lock_list = file_lock.readlines()

i = 0
while i < 3:
    name = input("Input you name: ")

    for lock_line in lock_list:
        lock_line = lock_line.strip('\n')
        if name == lock_line:
            print("用户 \033[31;1m%s\033[0m 已被锁定，请稍候再试..."% name)
            sys.exit(1)

    for user_line in user_list:
        (user,password) = user_line.strip('\n').split()
        if user == name:
            j = 0
            while j < 3:
                passwd = getpass.getpass("请输入密码:")
                if passwd == password:
                    print("欢迎回来， \033[32;1m%s\033[0m !"% name)
                    sys.exit(0)
                else:
                    print("密码错误，还剩 %s 次机会..."% (2 - j))
                    j += 1
            else:
                if j == 3:
                    file_lock.write(name + '\n')
                    print("密码错误超过最大次数，账号 %s 被锁定！"% name)
                    sys.exit(2)
    else:
        print("账号不存在，还剩 %s 次机会..."% (2 - i))
        i += 1
else:
    if i == 3:
        print("退出...")
        sys.exit(3)

file_lock.close()
file_user.close()