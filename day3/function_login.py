#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


def login(user,pwd):
    '''
    用户用户登陆验证
    :param: user 用户名
    :param: pwd  密码
    :return: Ture 登陆成功 False 登陆失败
    '''
    f = open('db','r')
    for line in f:
        if line.split('|')[0] == user and line.split('|')[1] == pwd:
            return True
    return False


def register(user, pwd):
    '''
    用户用户注册
    :param user: 用户名
    :param pwd: 密码
    :return: 默认None
    '''
    f = open('db', 'a')
    temp = "\n" + user + "|" + pwd
    f.write(temp)
    f.close()


def main():
    select = input("请选择：【1】登陆 【2】注册 ：")
    if select == "1":
        print("正在登陆...")
        user = input("请输入用户名： ")
        pwd = input("请输入密码： ")
        ret = login(user, pwd)
        if ret is True:
            print("登陆成功！")
        else:
            print("登陆失败！")
    if select == "2":
        print("正在注册...")
        user = input("请输入用户名： ")
        pwd = input("请输入密码 ")
        ret = register(user, pwd)
        print("注册成功！")

main()