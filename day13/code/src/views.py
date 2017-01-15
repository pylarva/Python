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


def create_host():
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
    hosts_file = os.path.join(base_dir, 'db', 'new_group.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = db_conn.Group(group_name=key)
            db_conn.session.add(obj)
        db_conn.session.commit()


def create_host_user():
    hosts_file = os.path.join(base_dir, 'db', 'new_host_user.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            print(key, val)

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
    hosts_file = os.path.join(base_dir, 'db', 'new_fort_user.yml')
    f = open(hosts_file)
    source = yaml.load(f)
    if source:
        for key, val in source.items():
            print(key, val)

            host_list = val.get('host')
            print(host_list)

            # 如果主机列表不为空 循环添加堡垒机用户权限 如 user01 → web01 + db01
            if host_list:
                for item in host_list:
                    print(item)
                    host_ret = db_conn.session.query(db_conn.Host).filter_by(hostname=item).all()
                    host_obj = host_ret[0]
                    obj = db_conn.FortUser(user_name=key, pwd=val.get('pwd'), host_user_id=host_obj.id)
                    db_conn.session.add(obj)

            # 如果主机列表为空 则说明该用户属于某个 用户组
            else:
                group = val.get('group')
                if not group:
                    print('主机或者主机组不能同时为空...')
                    sys.exit()
                else:
                    group_ret = db_conn.session.query(db_conn.Group).filter_by(group_name=group).all()
                    group_obj = group_ret[0]
                    obj = db_conn.FortUser(user_name=key, pwd=val.get('pwd'),
                                           group_id=group_obj.id)
                    db_conn.session.add(obj)

        db_conn.session.commit()


if __name__ == '__main__':
    # create_host()
    # create_group()
    # create_host_user()
    create_fort_user()