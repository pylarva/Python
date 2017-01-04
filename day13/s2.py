# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 多对多

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/s13", max_overflow=5)

Base = declarative_base()


class Host(Base):
    __tablename__ = 'host'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(32))
    port = Column(String(32))
    ip = Column(String(32))


class HostUser(Base):
    __tablename__ = 'host_user'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))


class HostToHostUser(Base):
    __tablename__ = 'host_to_host_user'
    nid = Column(Integer, primary_key=True, autoincrement=True)

    host_id = Column(Integer, ForeignKey('host.nid'))
    host_user_id = Column(Integer, ForeignKey('host_user.nid'))

    # 建立关系
    host = relationship('Host', backref='h')
    host_user = relationship('HostUser', backref='u')


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)

# 创建表
# init_db()

# 插入数据
Session = sessionmaker(bind=engine)
session = Session()
#
# session.add_all([
#     Host(hostname='c1', port='22', ip='1.1.1.1'),
#     Host(hostname='c2', port='22', ip='1.1.1.2'),
# ])
# session.commit()
#
# session.add_all([
#     HostUser(username='root'),
#     HostUser(username='sa'),
#     HostUser(username='db'),
# ])
# session.commit()
#
# session.add_all([
#     HostToHostUser(host_id=1, host_user_id=1),
#     HostToHostUser(host_id=1, host_user_id=2),
#     HostToHostUser(host_id=2, host_user_id=1),
#     HostToHostUser(host_id=2, host_user_id=3),
# ])
# session.commit()

# 1、找到 hostname 为c1的nid
# host_obj = session.query(Host).filter(Host.hostname == 'c1').first()
# print(host_obj.nid)

# 2、指定映射关系查找 对应主机用户ID
# host_to_host_user = session.query(HostToHostUser.host_user_id).filter(HostToHostUser.host_id == host_obj.nid).all()
# print(host_to_host_user)

# [(1,), (2,), (3,)]
# [1, 2, 3]

# r = zip(*host_to_host_user)

# 3、查找到用户
# users = session.query(HostUser.username).filter(HostUser.nid.in_(list(r)[0])).all()
# print(users)

# relationship 多对多查询
host_obj = session.query(Host).filter(Host.hostname == 'c1').first()
for item in host_obj.h:
    print(item.host_user.username)