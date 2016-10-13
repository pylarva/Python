#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys, re

# 向用户展示当前backend列表
def backend_show(haproxy_file):
    backend_list = []
    backend_list_show = {}
    with open(haproxy_file, 'r') as file:
        for line in file:
            if re.match('backend', line):
                backend_name = line.split()[1]
                backend_list.append(backend_name)
    for k,v in enumerate(backend_list,1):
        backend_list_show[k] = v
        print('\033[31m%s\033[0m. \033[31m%s\033[0m'% (k,v))


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
    print('--------------------------------------------')
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
            if user_select > 0 and user_select < 6:
                return user_select
            else:
                print("编号不存在...")
        else:
            print("输入错误...")

# 显示haproxy server信息
def haproxy_show():
    backend = input("请输入backend: ")


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
        haproxy_show()
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