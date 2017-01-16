# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

import os
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from conf import setting

Base = declarative_base()

engine = create_engine(setting.DB_CONN, echo=False)


class Host(Base):
    __tablename__ = 'host'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)
    port = Column(Integer, default=22)
    ip = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        temp = '%s  %s %s' % (self.id, self.hostname, self.ip)
        return temp


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        temp = '%s %s' % (self.id, self.group_name)
        return temp


class HostUser(Base):
    __tablename__ = 'host_user'
    id = Column(Integer, primary_key=True, autoincrement=False)
    host_id = Column(Integer, ForeignKey(Host.id))
    user_name = Column(String(64), nullable=False)
    pwd = Column(String(128))
    group_id = Column(Integer, ForeignKey(Group.id))

    host = relationship(Host, backref='h')
    group = relationship(Group, backref='g')

    def __repr__(self):
        temp = '%s %s %s %s %s' % (self.id, self.host_id, self.user_name, self.pwd, self.group_id)
        return temp


class FortUser(Base):
    __tablename__ = 'fort_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(64), nullable=False)
    pwd = Column(String(128))
    host_user_id = Column(Integer, ForeignKey(HostUser.id))
    group_id = Column(Integer, ForeignKey(Group.id))

    host_user = relationship(HostUser, backref='u')

    def __repr__(self):
        temp = '%s %s %s %s %s' % (self.id, self.user_name, self.pwd, self.host_user_id, self.group_id)
        return temp


class HistoryLog(Base):
    __tablename__ = 'history_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String(128))
    user_name = Column(String(64))
    host = Column(String(64))
    cmd = Column(String(128))

    def __repr__(self):
        temp = '%s %s %s %s %s' % (self.id, self.time, self.user_name, self.host, self.cmd)
        return temp


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)

# init_db()
# drop_db()

Session = sessionmaker(bind=engine)
session = Session()