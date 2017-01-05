# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Table, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import ChoiceType

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/s13?charset=utf8", max_overflow=5)

Base = declarative_base()

HostUser2Group = Table('hostuser_2_group', Base.metadata,
                       Column('hostuser_id', ForeignKey('host_user.id'), primary_key=True),
                       Column('group_id', ForeignKey('group.id'), primary_key=True),)

UserProfile2Group = Table('userprofile_2_group', Base.metadata,
                       Column('userprofile_id', ForeignKey('userprofile.id'), primary_key=True),
                       Column('group_id', ForeignKey('group.id'), primary_key=True),)

UserProfile2HostUser = Table('userprofile_2_hostuser', Base.metadata,
                       Column('userprofile_id', ForeignKey('userprofile.id'), primary_key=True),
                       Column('hostuser_id', ForeignKey('host_user.id'), primary_key=True),)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    ip_addr = Column(String(128), unique=True, nullable=False)
    port = Column(Integer, default=22)

    def __repr__(self):
        return "<id=%s, hostname=%s, ip_addr=%s>" % (self.nid, self.hostname, self.ip)


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return "<id=%s, name=%s" % (self.id, self.name)


class UserProfile(Base):
    __tablename__ = 'user_profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    host_list = relationship('HostUser', secondary=UserProfile2HostUser, backref='userprofiles')

    groups = relationship('Group', secondary=UserProfile2Group, backref='userprofiles')

    def __repr__(self):
        return "<id=%s, name=%s" % (self.id, self.username)


class HostUser(Base):
    __tablename__ = 'host_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(Integer, ForeignKey('host.id'))
    AuthTypes = [
        (u'ssh-passwd', u'SSH/Password'),
        (u'ssh-key', u'SSH/KEY'),
    ]
    auth_type = Column(ChoiceType(AuthTypes))
    username = Column(String(64), unique=True, nullable=False)
    password = Column(String(255))

    # relationship
    groups = relationship('Group', secondary=HostUser2Group, backref='host_list')

    # 联合唯一
    __table_args__ = (UniqueConstraint('host_id', 'username', name='host_id_username'))

    def __repr__(self):
        return "<id=%s, name=%s" % (self.id, self.username)


class AuditLog(Base):
    __tablename__ = 'audit_log'
    id = Column(Integer, primary_key=True)
    userprofile_id = Column(Integer, ForeignKey('user_profile.id'))
    hostuser_id = Column(Integer, ForeignKey('bind_host.id'))
    action_choices = [
        (0, 'CMD'),
        (1, 'Login'),
        (2, 'Logout'),
        (3, 'GetFile'),
        (4, 'SendFile'),
        (5, 'Exception'),
    ]
    action_choices2 = [
        (u'cmd', u'CMD'),
        (u'login', u'Login'),
        (u'logout', u'Logout'),
        #(3,'GetFile'),
        #(4,'SendFile'),
        #(5,'Exception'),
    ]
    action_type = Column(ChoiceType(action_choices2))
    #action_type = Column(String(64))
    cmd = Column(String(255))
    date = Column(DateTime)

    user_profile = relationship("UserProfile")
    # bind_host = relationship("BindHost")


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


