# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

from sqlalchemy import create_engine,and_,or_,func,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,UniqueConstraint,DateTime
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/s13", max_overflow=5)

Base = declarative_base()


# 程序登陆用户和服务器账户，一个人可以有多个服务器账号，一个服务器账号可以给多个人用
UserProfile2HostUser= Table('userprofile_2_hostuser',Base.metadata,
    Column('userprofile_id',ForeignKey('user_profile.id'),primary_key=True),
    Column('hostuser_id',ForeignKey('host_user.id'),primary_key=True),
)


class Host(Base):
    __tablename__='host'
    id = Column(Integer,primary_key=True,autoincrement=True)
    hostname = Column(String(64),unique=True,nullable=False)
    ip_addr = Column(String(128),unique=True,nullable=False)
    port = Column(Integer,default=22)
    def __repr__(self):
        return "<id=%s,hostname=%s, ip_addr=%s>" %(self.id,
                                                    self.hostname,
                                                    self.ip_addr)


class HostUser(Base):
    __tablename__ = 'host_user'
    id = Column(Integer, primary_key=True)
    AuthTypes = [
        (u'ssh-passwd', u'SSH/Password'),
        (u'ssh-key', u'SSH/KEY'),
    ]
    # auth_type = Column(ChoiceType(AuthTypes))
    auth_type = Column(String(64))
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255))

    host_id = Column(Integer, ForeignKey('host.id'))
    __table_args__ = (UniqueConstraint('host_id', 'username', name='_host_username_uc'),)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique=True,nullable=False)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer,primary_key=True)
    username = Column(String(64),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    # 一个人只能在一个组
    group_id = Column(Integer, ForeignKey('group.id'))

    host_list =relationship('HostUser', secondary=UserProfile2HostUser, backref='userprofiles')


Session = sessionmaker(bind=engine)
session = Session()

obj = session.query(UserProfile).filter(usename='输入的用户名', password='输入的密码').first()
if not obj:
    # 输入这个人的所有机器
    for item in obj.host_list:
        # item 是一个HostUser对象
        item.password, item.username,
        # item.host 对象 host对象
        item.host.hostname,item.host.port


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer,primary_key=True)
    userprofile_id = Column(Integer,ForeignKey('user_profile.id'))
    hostuser_id = Column(Integer,ForeignKey('host_user.id'))

    cmd = Column(String(255))
    date = Column(DateTime)
