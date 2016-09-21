#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys,time

def shopping_home(user_name,salary):
    product_dict = {
        '家电类':['iphone',5888],
    while True:


user_file = open('C:/software/github/Python/day2/shopping_cart/user.txt','r+')
user_list = user_file.readlines()
user_name = input('请输入您的用户名： ')
for user_line in user_list:
    (user,password,salary) = user_line.split()
    salary = int(salary)
    if user == user_name:
        i = 0
        while i < 3:
            passwd = input('请输入密码： ')
            if passwd == password:
                print('\033[32;1m%s\033[0m，欢迎您！您当前余额为 \033[31;1m%d\033[0m...'% (user_name,salary))
                print('正在进入购物页面...')
                time.sleep(2)
                shopping_home(user_name,salary)
            else:
                print('密码错误，还剩%d次机会...'% (2-i))
                i += 1
                continue
    else:
        print('用户未找到...')
        sys.exit()





