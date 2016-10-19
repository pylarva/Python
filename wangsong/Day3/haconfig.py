#!/usr/bin/env python

"""
__author:super
blog adress: http://blog.csdn.net/songfreeman
haconfig.py  is class for  manage haproxy configuration  
operate configuration contend as:
        backend test.oldboy.org
                server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000
class haproxy:
ip: the ip address in backend configuration. such as : 100.1.7.9
weight: weight value in backend configuration . default 20
max_conn: maxconn value in backend configuration.default 100
backend_contant:  backend configuration full value. ex: server 191.125.2.34 191.125.2.34 weight 20 maxconn 200
backend_name: all backend name in configuration file: ex: ['test.oldboy.org','buy.oldboy.org']
run in python3.x
"""

import os
import shutil
import re


class haproxy(object):

    __default_path = os.path.dirname(os.path.basename("__file__"))
    __default_file = os.path.join(__default_path, "haproxy.cfg")
    _tmp_file = os.path.join(__default_path, "tmp.cfg")

    def __init__(self, ip='', weight=20, max_conn=100, file=__default_file):
        self.config_file = file
        self.ip_address = ip
        self.weight = weight
        self.max_conn = max_conn
        self.backend_contant = ''
        self.backend_name = list()

    # 检查ip是否合法
    @property
    def check_ip_available(self):
        rule = "((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$"
        r = re.compile(rule)
        if r.match(self.ip_address):
            return True
        else:
            return False

    # 拼接字符串
    def union_str(self):
        """
        添加或修改backend的内容时,调用此类方法，将输入的参数值拼接成一行完成配置信息
        :return: 更新到self.backend_value属性中,
        """
        _default_str = 'server {ip} {ip} weight {weight} maxconn {maxconn}'
        self.backend_contant = _default_str.format(ip=self.ip_address,
                                                   weight=self.weight,
                                                   maxconn=self.max_conn)

    def get_backend_name(self):
        """
        获取配置文件中的所有 backend 节点信息
        :return: 无返回值,保存在 self.backend_name 中
        """
        with open(self.config_file, 'r') as fr:
            for line in fr:
                if line.startswith("backend"):
                    self.backend_name.append(line.split()[1])

    # 查找指定 backend 节点下的配置信息
    def show_backend(self, backend):
        """
        根据用户输入的 backend 节点值获取对应的配置文件
        :param backend: 查找的键值,如: test.oldboy.org
        :return: 返回一个列表  list
        """
        result = list()
        # 定位到查找的行标识
        line_locked_flag = False

        with open(self.config_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 如果找到 backend 配置节
                if line.startswith('backend'):
                    # 获取backend的内容,test.oldboy.com
                    url_addr = line.split()[1]
                    # 如果内容和搜索的内容一样,则将定位标识置为True
                    if url_addr == backend:
                        line_locked_flag = True
                        continue
                    else:
                        line_locked_flag = False

                # 如果定位到内容则将配置写入到结果列表中
                if line_locked_flag:
                    result.append(line)
        return result

    # 增加backend内容
    def add_backend(self, backend):
        """
        根据输入的backend查找文件:
        如果存在 backend,则在配置末尾增加一条记录
        如果不存在 backend，则在最后新增加一个
        :param backend: 要增加的backend，如:test.oldboy.com
        :return:
        """
        # 是否存在指定的backend标识,如果存在就在指定下面添加配置，没有就新建一个backend,再添加配置
        backend_is_exists_flag = False
        # 定位到查找的行标识
        line_locked_flag = False

        try:
            with open(self.config_file, 'r') as fr,open(self._tmp_file, 'a+') as fw:
                for line in fr:
                    if line.startswith('backend'):
                        url_addr = line.split()[1]
                        if url_addr == backend:
                            backend_is_exists_flag = True
                            line_locked_flag = True
                        else:
                            # 找到"backend"字符标识,且定位标识为True,说明到了定位的下一个backend,这时需要先追加一条配置
                            if line_locked_flag:
                                fw.write("        {content}\n".format(content=self.backend_contant))
                                line_locked_flag = False
                    fw.write(line)

                # 文件中没有要添加的 backend 节点,那在最后新增加一个节点
                if not backend_is_exists_flag:
                    fw.write("backend {url}\n".format(url=backend))
                    fw.write("        {content}\n".format(content=self.backend_contant))

            # 将临时文件重命名,替换原来的配置文件
            shutil.move(self._tmp_file, self.config_file)

            return True
        except Exception as e:
            return e

    # 删除指定 backend 的配置
    def del_backend(self, backend):
        is_locked_flag = False
        # 是否找到指定的 IP 配置信息
        is_delete_flag = False
        try:
            with open(self.config_file, 'r') as fr, open(self._tmp_file, 'a+') as fw:
                for line in fr:
                    # 找到backend行
                    if line.startswith("backend"):
                        url_addr = line.split()[1]
                        # 找到指定的backend节点
                        if url_addr == backend:
                            is_locked_flag = True
                        else:
                            # 找到指定 backend 节点的下一个backend, 定位标识别改为False
                            if is_locked_flag:
                                is_locked_flag = False
                    else:
                        if is_locked_flag:
                            # 在定位的 backend 节点下找到符合的 IP ,则把这一行跳过,不写到tmp文件中
                            if line.count(self.ip_address) > 0:
                                is_delete_flag = True
                                continue

                    fw.write(line)
            shutil.move(self._tmp_file, self.config_file)
            if not is_delete_flag:
                return False
            else:
                return True
        except Exception as e:
            return e





