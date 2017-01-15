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

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

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


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)

# init_db()
# drop_db()

Session = sessionmaker(bind=engine)
session = Session()