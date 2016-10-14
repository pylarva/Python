#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
import sys, re
from collections import defaultdict,OrderedDict

# 向用户展示当前backend列表
def backend_show(haproxy_file):
    backend_list = []
    backend_list_show = {}
    backend_list_server = defaultdict(list)

    with open(haproxy_file, 'r') as file:
        for line in file:
            if re.match('backend', line):
                backend_name = line.split()[1]
                backend_list.append(backend_name)
            elif re.match('\s+server', line):
                line = line.split()
                server_dict = {}
                server_dict['name'] = line[1]
                server_dict['server'] = line[2]
                server_dict['weight'] = line[4]
                server_dict['maxconn'] = line[6]
                backend_list_server[backend_name].append(server_dict)
    #             check_dic = backend_list_server.get(backend_name)
    #             if check_dic is None:
    #                 backend_list_server.setdefault(backend_name, line)
    #             else:
    #                 backend_list_server[backend_name].append(line)
    # print(backend_list_server)
    # for k,v in enumerate(backend_list,1):
    #     backend_list_show[k] = v
    #     print('\033[31m%s\033[0m. \033[31m%s\033[0m'% (k,v))
    return(backend_list,backend_list_show, backend_list_server)


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
    (backend_list, backend_list_show, backend_list_server) = backend_show(haproxy_file)
    for k,v in enumerate(backend_list,1):
        backend_list_show[k] = v
        print('\033[31m%s\033[0m. \033[31m%s\033[0m'% (k,v))
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
def haproxy_show(backend_list_server):
    while True:
        backend = input("请输入backend: ")
        value = backend_list_server[backend]
        print(value)
        if backend in backend_list_server:
            print('''
-------------------------------------------
序号    名称     地址      权重     最大连接数
                  ''')
            for k,v in enumerate(value,1):
                print('%-5s'% k,end='')
                print(value[k]['name'],value[k]['server'])
        else:
            print('输入错误，请重新输入...')


# 增加haproxy server函数
#def haproxy_add():
# 删除haprxoy server函数
#def haproxy_dell():
# 修改haproxy server函数
#def haproxy_change():


# 开始主程序
def main():
    menu_show()
    (backend_list, backend_list_show, backend_list_server) = backend_show(haproxy_file)
    ret = user_select()
    if ret == 1:
        haproxy_show(backend_list_server)
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