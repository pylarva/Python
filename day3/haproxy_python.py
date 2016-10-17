#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os,sys,re,time
from collections import defaultdict,OrderedDict


# 向用户展示当前backend列表
def file_read():
    backend_list = []
    server_flag = False
    backend_name_dict = defaultdict(list)

    with open(haproxy_file, 'r') as file:
        for line in file:
            if line.split():
                server_dict = OrderedDict()
                line = line.split()

                if line[0] == 'backend':
                    backend_name = line[1]
                    backend_list.append(backend_name)

                    server_flag = True
                elif line[0] == 'server' and server_flag:
                    server_info = line
                    server_dict['name'] = server_info[1]
                    server_dict['server'] = server_info[2]
                    server_dict['weight'] = server_info[4]
                    server_dict['maxconn'] = server_info[6]
                    backend_name_dict[backend_name].append(server_dict)

                else:
                    server_flag = False

    #print(backend_name_dict)
    return(backend_list,backend_name_dict)


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
    show_dict = {}
    backend_list = ''
    (backend_list, backend_name_dict) = file_read()
    for k,v in enumerate(backend_list, 1):
        show_dict[k] = v
        print('\033[31m%s\033[0m. \033[31m%s\033[0m' % (k, v))
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
            if 0 < user_select < 6:
                return user_select
            else:
                print("编号不存在...")
        else:
            print("输入错误...")

# 显示haproxy server信息
def haproxy_show(inquiry_flag,backend_server_dict):
    backend_name = input('请输入所查询的backend名称（ \'b\' 返回）： ')
    if backend_name in backend_server_dict:
        print('\n================================================================')
        print('%-5s %-10s %-15s %-15s %-15s' % ('序号', '名称', 'IP', '权重', '最大连接数'))
        server_list = backend_server_dict[backend_name]
        for k, v in enumerate(server_list, 1):
            print('%-5s ' % k,end='')
            for m,n in v.items():
                print('%-15s ' % n,end='')
            print()
        print('\n================================================================')
        return inquiry_flag
    if backend_name == 'b':
        inquiry_flag = False
    else:
        print('输入错误，请重新输入...')
    return inquiry_flag



# 增加haproxy server函数
#def haproxy_add():
# 删除haprxoy server函数
#def haproxy_dell():
# 修改haproxy server函数
#def haproxy_change():


# 开始主程序
def main():
    backend_flag = True
    while backend_flag:
        menu_show()
        (backend_name_dict, backend_server_dict) = file_read()
        ret = user_select()
        if ret == 1:
            inquiry_flag = True
            while inquiry_flag:
                inquiry_flag = haproxy_show(inquiry_flag,backend_server_dict)
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