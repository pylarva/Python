#!/usr/bin/env python

"""
__author: super
blog    : http://blog.csdn.net/songfreeman
this is the main program for haproxy operation,there has 3 functions for operate haproxy.cfg file
1.search backend
2.add backend
3.del backend
this program was writed by python3.4
"""

from Day3.haconfig import haproxy

welcome_title_str = "%s\n#%s#\n#%s#\n#%s#\n%s" % ("".ljust(50, '#'),
                                                  ''.ljust(48, ' '),
                                                  'HAProxy 配置管理程序'.center(43, ' '),
                                                  ''.ljust(48, ' '),
                                                  ''.ljust(50, '#')
                                                  )
menu_str = "\n1.查找配置\n2.添加配置\n3.删除配置\n4.退出程序\n"


# 返回一个非空的输入
def input_string(show_message, is_int=False):
    """
    对input函数进行重新改造,增加判断不能为空,
    :param show_message: input()中的提示信息
    :param is_int: 是否要求输入必须为数字,默认为False,如果为True就要检查是否为数字
    :return: 返回用户输入的值
    """
    not_null_flag = False
    while not not_null_flag:
        # 获得用户的输入信息
        input_value = input("{message}".format(message=show_message)).strip().lower()
        if not input_value:
            continue
        else:
            # 如果要求输入必须为数字,则做以下验证
            if is_int:
                if not input_value.isdigit():
                    print("\n\033[1;30m非法输入,请输入一个数字!\033[0m")
                    continue
            not_null_flag = True
    return input_value


if __name__ == "__main__":
    print(welcome_title_str)

    # 退出系统标识
    exit_flag = False
    while not exit_flag:
        print(menu_str)
        choose = input("请选择功能模块:").strip().lower()

        # 退出系统
        if choose == '4':
            exit_flag = True
            continue

        if choose not in ('1', '2', '3'):
            print("\n\033[1;31m输入错误!请输入正确的功能编号.\033[0m")
            continue
        else:
            # 实例化配置文件对象
            proxyobj = haproxy()

            # 1. 查找节点配置信息
            if choose == "1":
                # 获取所有 backend 的节点名称
                proxyobj.get_backend_name()
                print("\n当前配置文件所有 backend 节点名称：")
                for name in proxyobj.backend_name:
                    print(name)

                search_backend = input_string("\n请输入要查找的 backend 域名:")
                # 调用类方法获取配置信息列表
                search_result = proxyobj.show_backend(search_backend)
                if not search_result:
                    print("\n\033[1;30m没有找到要查找的记录!\033[1m\n ")
                else:
                    for record in search_result:
                        print(record.strip())

            # 2. 添加配置
            if choose == "2":
                search_backend = input_string("请输入要添加的 backend 域名:")
                # 对配置文件对象进行赋值
                proxyobj.ip_address = input_string("请输入添加的 IP 地址:")
                # 判断IP是否合法
                while not proxyobj.check_ip_available:
                    proxyobj.ip_address = input_string("\nIP地址不合法！ 请重新输入 IP 地址:")
                proxyobj.weight = input_string("请输入添加的 weight 值:", is_int=True)
                proxyobj.max_conn = input_string("请输入添加的 max conn 值:", is_int=True)

                # 根据用户输入的信息,调用类的格式化字符串方法生成配置文件串
                proxyobj.union_str()

                # 调用添加方法进行添加配置操作
                if proxyobj.add_backend(search_backend):
                    print("\n添加成功! 节点当前配置更新为：")

                # 将添加成功的信息打印出来,直接调用类的查看方法
                search_result = proxyobj.show_backend(search_backend)
                for line in search_result:
                    print(line.strip())

            # 3. 删除配置
            if choose == "3":
                # 重新获取一下当前配置文件中的节点名称列表
                proxyobj.get_backend_name()

                # 要删除的 backend 节点是否存在标识
                is_exist_flag = False
                while not is_exist_flag:
                    search_backend = input_string("请指定要删除配置的 backend 节点名称: ")
                    if search_backend not in proxyobj.backend_name:
                        print("\n当前配置文件中未找到 %s 的 backend 节点!" % search_backend)
                        continue
                    else:
                        is_exist_flag = True

                proxyobj.ip_address = input_string("请输入要删除的 IP 地址：")
                # 判断IP是否合法
                while not proxyobj.check_ip_available:
                    proxyobj.ip_address = input_string("\nIP地址不合法！ 请重新输入 IP 地址:")

                # 调用类的删除方法进行删除操作
                if proxyobj.del_backend(search_backend):
                    print("\n删除成功!当前节点配置更新为： ")
                else:
                    print("\n删除失败!请检查 IP 地址是否存在!\n")

                # 将修改后的信息打印出来,直接调用类的查看方法
                search_result = proxyobj.show_backend(search_backend)
                for line in search_result:
                    print(line.strip())
