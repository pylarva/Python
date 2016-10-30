#！/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os,sys,re,time
from collections import defaultdict,OrderedDict


# 读取haproxy配置文件，得到backend列表和server字典
def file_read():
    """
    读原始配置文件，得到backend列表和保存有server信息的字典
    :return: backend列表，server字典
    """
    backend_list = []
    server_flag = False
    backend_server_dict = defaultdict(list)

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
                    backend_server_dict[backend_name].append(server_dict)

                else:
                    server_flag = False

    return(backend_list,backend_server_dict)


def name_add():
    """
    添加server信息时对name有效性检查
    :return: name 名称
    """
    name_flag = True
    while name_flag:
        name_input = input('请输入名称(以字母数字或者下划线开头)： ')
        if len(name_input) == 0:
            continue
        elif name_input == 'q':
            name_flag = False
        elif re.match('[0-9a-zA-Z\_]+', name_input):
            name = name_input
            return name
        else:
            print('输入有误...')


def ip_add():
    """
    添加server信息时对ip有效性检查
    :return: ip
    """
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
    """
    添加server信息时对weight有效性检查
    :return: 权重
    """
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
    """
    添加server信息时对maxconn有效性检查
    :return: 最大连接数
    """
    maxconn_flag = True
    while maxconn_flag:
        maxconn_input = input('请输入最大文件打开数： ')
        if len(maxconn_input) == 0:
            continue
        elif maxconn_flag == 'q':
            maxconn_flag = False
        elif maxconn_input.isdigit():
            maxconn = int(maxconn_input)
            return maxconn
        else:
            print('输入有误...')


def backend_server_add(backend_server_dict):
    """
    根据server字典写文件操作，一个文件读，一个文件写
    :param backend_server_dict: server字典
    :return:
    """
    add_flag = False
    newfile = '%s.new' % haproxy_file
    with open(haproxy_file, 'r') as read_file,open(newfile, 'w') as write_file:
        for line in read_file:
            if re.match('backend', line):
                if backend_server_dict[line.split()[1]]:
                    write_file.write(line)
                    backend_name = line.split()[1]
                    for server_dict in backend_server_dict[backend_name]:
                        if server_dict:
                            server_line = '\tserver {name} {ip} weight {weight} maxconn {maxconn}\n'
                            write_file.write(server_line.format(**server_dict))
                        else:
                            write_file.write('\n')
                    add_flag = True
                else:
                    pass
                add_flag = True
            elif add_flag and re.match('\s+server', line):
                pass
            else:
                write_file.write(line)
                add_flag = False
        print('更新server成功！')
        os.system('mv %s %s.bak' % (haproxy_file, haproxy_file))
        os.system('mv %s %s' % (newfile, haproxy_file))
        time.sleep(2)


def check_repeat(backend_name, backend_server_dict, add_server_dict):
    """
    检查同backend里面是否有相同ip，做更新操作
    :param backend_name: 名称
    :param backend_server_dict: server字典
    :param add_server_dict: 要添加的server信息
    :return: 更新后的server字典
    """
    de = backend_server_dict[backend_name]
    for k, v in enumerate(de):
        if de[k]['ip'] == add_server_dict['ip']:
            del de[k]
    de.append(add_server_dict)
    return backend_server_dict


# 打印登陆选项菜单
def menu_show():
    """
    打印登陆互动菜单
    :return:
    """
    print(
        '''
\033[32m=========================================\033[0m
\033[32m||      Haproxy配置文件管理平台       ||\033[0m
\033[32m=========================================\033[0m
当前系统backend列表如下：
        ''')
    # 调用file_read函数显示backend列表
    show_dict = {}
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


# 显示相应的backend server信息
def haproxy_show(backend_name, backend_server_dict):
    """
    根据backend，遍历backend_server_dict字典展现给用户
    """
    inquiry_flag = True
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
    """
    对server字典进行增加操作，将字典信息再写入到文件
    :param backend_server_dict: 保存有server信息的字典
    :return: 返回更新后的server字典
    """
    backend_name = input('请输入要修改的backend: ')

    if backend_name in backend_server_dict:
        add_server_dict = OrderedDict()
        print('请依次输入想要添加的server信息： ')
        add_server_dict['name'] = name_add()
        add_server_dict['ip'] = ip_add()
        add_server_dict['weight'] = weight_add()
        add_server_dict['maxconn'] = maxconn_add()

        print(add_server_dict['name'],add_server_dict['ip'],add_server_dict['weight'],add_server_dict['maxconn'])
        server_commit = input('是否添加该条server信息[Y/N]： ')
        if server_commit == 'Y' or server_commit == 'y':
            # 检查是否有重复ip
            backend_server_dict = check_repeat(backend_name, backend_server_dict, add_server_dict)
            # 进行server的添加
            backend_server_add(backend_server_dict)
            add_flag = False
            return (add_flag, backend_server_dict)
        else:
            add_flag = False
            return (add_flag, backend_server_dict)
    else:
        add_backend_name = input('Backend不存在，是否添加？[Y/N] ')
        if add_backend_name == 'Y' or add_backend_name == 'y':
            with open(haproxy_file, 'a+') as file:
                file.write('\n'*2 + 'backend ' + '%s' % backend_name)
                server_dict = OrderedDict()
                # server_dict['name'] = ''
                # server_dict['ip'] = ''
                # server_dict['weight'] = ''
                # server_dict['maxconn'] = ''
                backend_server_dict[backend_name].append(server_dict)
                print('添加成功！')
                add_flag = True
                return (add_flag, backend_server_dict)
        else:
            add_flag = False
            return (add_flag, backend_server_dict)


# 删除haprxoy server函数
def haproxy_del(backend_server_dict):
    """
    删除server信息还是基于对总的server字典操作，然后根据字典写文件
    :param backend_server_dict: 总的server字典
    :return: 更新后的字典
    """
    user_choose = input('删除整个backend【按1】，删除单个server【按2】： ')
    if user_choose == '1':
        user_choose_backend = input('请输入bankend名称： ')
        if user_choose_backend in backend_server_dict:
            haproxy_show(user_choose_backend, backend_server_dict)
            affir_del = input('确认全部删除吗？[Y/N]: ')
            if affir_del == 'Y' or affir_del == 'y':
                del backend_server_dict[user_choose_backend]
                # 写入文件
                backend_server_add(backend_server_dict)
            else:
                del_flag = False
                return(del_flag, backend_server_dict)
        else:
            del_flag = False
            return (del_flag, backend_server_dict)

    elif user_choose == '2':
        user_choose_backend = input('请输入backend名称： ')
        if user_choose_backend in backend_server_dict:
            haproxy_show(user_choose_backend, backend_server_dict)
            user_choose_ip = input('请输入要删除的IP地址： ')
            if re.match('(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}(\:\d{1,5})?$', user_choose_ip):
                de = backend_server_dict[user_choose_backend]
                for k, v in enumerate(de):
                    if de[k]['ip'] == user_choose_ip:
                        del de[k]
                backend_server_add(backend_server_dict)
                time.sleep(1)
                del_flag = False
                return (del_flag, backend_server_dict)
            else:
                print('输入错误...')
                time.sleep(1)
                del_flag = False
                return (del_flag, backend_server_dict)
    else:
        print('输入错误')
        time.sleep(1)
        del_flag = False
        return (del_flag, backend_server_dict)


# 开始主程序
def main():
    main_flag = True
    while main_flag:
        menu_show()
        # 调用file_read读取文件，得到一个backend列表和一个保存有server信息的字典
        (backend_name_dict, backend_server_dict) = file_read()

        ret = user_select()

        if ret == 1:
            inquiry_flag = True
            while inquiry_flag:
                backend_name = input('请输入所查询的backend名称（ \'b\' 返回）： ')
                inquiry_flag = haproxy_show(backend_name, backend_server_dict)

        if ret == 2:
            add_flag = True
            while add_flag:
                (add_flag, backend_server_dict) = haproxy_add(backend_server_dict)

        if ret == 3:
            del_flag = True
            while del_flag:
                (del_flag, backend_server_dict) = haproxy_del(backend_server_dict)

        if ret == 4:
            change_flag = True
            while change_flag:
                (change_flag, backend_server_dict) = haproxy_add(backend_server_dict)

        if ret == 5:
            print("退出系统成功！")
            sys.exit()

haproxy_file = 'haproxy_conf_ori'
main()