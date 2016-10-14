#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys, re
from collections import defaultdict,OrderedDict

# 向用户展示当前backend列表
def backend_show(haproxy_file):
    backend_name_list = []
    backend_name = ''
    server_list = {}
    i = 0
    with open(haproxy_file, 'r') as file:
        for line in file:
            line = line.split()
            if bool(line) is not False and line[0] == 'backend':
                backend_name = line[1]
                backend_name_list.append(backend_name)
            elif bool(line) is not False and line[0] == 'server':
                server_list[backend_name][i] = line
                i += 1
                print(server_list[backend_name][i])
    print(backend_name_list)
    print(server_list)
    for k,v in enumerate(backend_name_list):
        print('%s. %s'% (k,v))

# 打印登陆选项菜单
def menu_show():
    print(
        '''
\033[32m=========================================\033[0m
\033[32m||      Haproxy配置文件管理平台       ||\033[0m
\033[32m=========================================\033[0m
当前系统backend列表如下：
        ''')
    # 调用backend显示函数
    backend_show(haproxy_file)
    print('-'.center(50, '-'))
    print(
        '''
您可以对backend做如下操作：
1.获取HAproxy记录
2.增加HAproxy记录
3.删除HAproxy记录
4.修改HAproxy记录
5.退出系统
=========================================
        '''
    )

# 用户输入编号判断
def user_select():
    """
    用户输入的如果是1-5数字则return对应数字给主函数
    """
    while True:
        user_select = input("请输入编号： ")
        if user_select.isdigit():
            user_select =int(user_select)
            if 0 < user_select < 6:
                return user_select
            else:
                print("编号不存在...")
        else:
            print("输入错误...")

# 显示haproxy server信息
#def haproxy_show(haproxy_file):


# 增加haproxy server函数
#def haproxy_add():
# 删除haprxoy server函数
#def haproxy_dell():
# 修改haproxy server函数
#def haproxy_change():


# 开始主程序
def main():
    menu_show()
    ret = user_select()
    if ret == 1:
        haproxy_show(haproxy_file)
    if ret == 2:
        haproxy_add()
    if ret == 3:
        haproxy_dell()
    if ret == 4:
        haproxy_change()
    if ret == 5:
        print("退出系统成功！")
        sys.exit()

haproxy_file = 'haproxy_conf_ori'
main()