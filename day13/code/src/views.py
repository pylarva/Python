# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys
import yaml

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from src import db_conn

"""
根据yml模板 插入数据库数据
"""


def create_host():
    """
    创建主机
    :return:
    """
    hosts_file = os.path.join(base_dir, 'db', 'new_host.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            # print(key, val)
            obj = db_conn.Host(hostname=key, ip=val.get('ip'), port=val.get('port') or 22)
            db_conn.session.add(obj)
        db_conn.session.commit()


def create_group():
    """
    创建用户组
    :return:
    """
    hosts_file = os.path.join(base_dir, 'db', 'new_group.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            obj = db_conn.Group(group_name=key)
            db_conn.session.add(obj)
        db_conn.session.commit()


def create_host_user():
    """
    创建主机用户 一台主机可以有不同权限的用户
    :return:
    """
    hosts_file = os.path.join(base_dir, 'db', 'new_host_user.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            # print(key, val)

            # 查询主机表中的主机编号
            host = val.get('host')
            host_ret = db_conn.session.query(db_conn.Host).filter_by(hostname=host).all()
            host_obj = host_ret[0]

            # 查询主机组编号
            group = val.get('group')
            group_ret = db_conn.session.query(db_conn.Group).filter_by(group_name=group).all()
            group_obj = group_ret[0]

            obj = db_conn.HostUser(id=key, host_id=host_obj.id, user_name=val.get('user_name'),
                                   pwd=val.get('pwd'), group_id=group_obj.id)
            db_conn.session.add(obj)
        db_conn.session.commit()


def create_fort_user():
    """
    创建堡垒机用户
    :return:
    """
    hosts_file = os.path.join(base_dir, 'db', 'new_fort_user.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            # print(key, val)

            host_list = val.get('host')
            # print(host_list)

            # 如果主机列表不为空 循环添加堡垒机用户权限 如 user01 → web01 + db01
            if host_list:
                for item in host_list:

                    # 获取 yaml 文件中的权限 主机 + 用户列表
                    host = list(item.keys())[0]
                    user = item.get(host)

                    # 查主机编号
                    host_ret = db_conn.session.query(db_conn.Host).filter_by(hostname=host).all()
                    host_obj = host_ret[0]

                    # 在HostUser中查 主机编号+用户名 对应的HostUeser对应的编号
                    host_user_ret = db_conn.session.query(db_conn.HostUser).filter_by(host_id=host_obj.id, user_name=user).all()
                    host_user_obj = host_user_ret[0]

                    # 在堡垒机用户表中添加主机用户对应ID
                    obj = db_conn.FortUser(user_name=key, pwd=val.get('pwd'), host_user_id=host_user_obj.id)
                    db_conn.session.add(obj)

            # 如果主机列表为空 则说明该用户属于某个 用户组
            group = val.get('group')
            if group:
                group_ret = db_conn.session.query(db_conn.Group).filter_by(group_name=group).all()
                group_obj = group_ret[0]
                obj = db_conn.FortUser(user_name=key, pwd=val.get('pwd'),
                                       group_id=group_obj.id)
                db_conn.session.add(obj)

        db_conn.session.commit()


def run():
    create_host()
    create_group()
    create_host_user()
    create_fort_user()

# run()