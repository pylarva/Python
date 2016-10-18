#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os,sys,re,time
from collections import defaultdict,OrderedDict


# 读取haproxy配置文件，得到backend列表和server字典
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
                    server_dict['ip'] = server_info[2]
                    server_dict['weight'] = server_info[4]
                    server_dict['maxconn'] = server_info[6]
                    backend_name_dict[backend_name].append(server_dict)

                else:
                    server_flag = False

    #print(backend_name_dict)
    return(backend_list,backend_name_dict)

def name_add():
    name_flag = True
    while name_flag:
        name_input = input('请输入名称(以字母数字或者下划线开头)： ')
        if len(name_input) == 0:
            continue
        elif name_input == 'q':
            name_flag = False
        elif re.match('[0-9a-zA-Z\_]+', name_input):
            name = name_input
            name_flag = False
        else:
            print('输入有误...')
    return name


def ip_add():
    ip_flag = True
    while ip_flag:
        ip_input = input('请输入IP地址： ')
        if len(ip_input) == 0:
            continue
        elif ip_input == 'q':
            ip_flag = False
        elif re.match('(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}(\:\d{1,5})?$', ip_input):
            ip = ip_input
            ip_flag = False
        else:
            print('IP格式有误...')
            continue
    return ip

def weight_add():
    weight_flag = True
    while weight_flag:
        weight_input = input('请输入权重值： ')
        if len(weight_input) == 0:
            continue
        elif weight_flag == 'q':
            weight_flag = False
        elif weight_input.isdigit():
            weight = int(weight_input)
            weight_flag = False
        else:
            print('输入有误...')
    return weight

def maxconn_add():
    maxconn_flag = True
    while maxconn_flag:
        maxconn_input = input('请输入最大文件打开数： ')
        if len(maxconn_input) == 0:
            continue
        elif maxconn_flag == 'q':
            maxconn_flag = False
        elif maxconn_input.isdigit():
            maxconn = int(maxconn_input)
            maxconn_flag = False
        else:
            print('输入有误...')
    return maxconn


def backend_server_add(backend_server_dict):
    add_flag = False
    with open(haproxy_file, 'r') as read_file,open('newfile', 'w') as write_file:
        for line in read_file:
            if re.match('backend', line):
                write_file.write(line)
                backend_name = line.split()[1]
                for server_dict in backend_server_dict[backend_name]:
                    server_line = '\tserver {name} {ip} weight {weight} maxconn {maxconn}\n'
                    write_file.write(server_line.format(**server_dict))
                add_flag = True
            elif add_flag and re.match('\s+server', line):
                pass
            else:
                write_file.write(line)
                add_flag = False
    print('添加新server成功！')




# 打印登陆选项菜单
def menu_show():
    print(
        '''
\033[32m=========================================\033[0m
\033[32m||      Haproxy配置文件管理平台       ||\033[0m
\033[32m=========================================\033[0m
当前系统backend列表如下：
        ''')
    # 调用file_read函数
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
def haproxy_add(backend_server_dict):
    backend_name = input('请输入要修改的backend: ')

    if backend_name in backend_server_dict:
        add_server_dict = OrderedDict()
        print('请依次输入想要添加的server信息（按q退出）： ')
        add_server_dict['name'] = name_add()
        add_server_dict['ip'] = ip_add()
        add_server_dict['weight'] = weight_add()
        add_server_dict['maxconn'] = maxconn_add()

        print(add_server_dict['name'],add_server_dict['ip'],add_server_dict['weight'],add_server_dict['maxconn'])
        server_commit = input('是否添加该条server信息[Y/N]： ')
        if server_commit == 'Y' or server_commit == 'y':
            backend_server_dict[backend_name].append(add_server_dict)
            backend_server_add(backend_server_dict)
            add_flag = False
            return add_flag
        else:
            add_flag = False
            return add_flag
    else:
        print('输入不正确...')

# 删除haprxoy server函数
#def haproxy_dell():
# 修改haproxy server函数
#def haproxy_change():


# 开始主程序
def main():
    main_flag = True
    while main_flag:
        menu_show()
        (backend_name_dict, backend_server_dict) = file_read()
        ret = user_select()
        if ret == 1:
            inquiry_flag = True
            while inquiry_flag:
                inquiry_flag = haproxy_show(inquiry_flag,backend_server_dict)
        if ret == 2:
            add_flag = True
            while add_flag:
                add_flag = haproxy_add(backend_server_dict)
        if ret == 3:
            haproxy_dell()
        if ret == 4:
            haproxy_change()
        if ret == 5:
            print("退出系统成功！")
            sys.exit()

haproxy_file = 'haproxy_conf_ori'
main()