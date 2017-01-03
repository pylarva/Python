# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

# 关系不再AB表中

from sqlalchemy import create_engine,and_,or_,func,Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey,UniqueConstraint,DateTime
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/s13", max_overflow=5)

Base = declarative_base()


# HostToHostUser = Table('host_to_host_user', Base.metadata,
#                        Column('host_id', ForeignKey('host.nid'), primary_key=True),
#                        Column('host_user_id', ForeignKey('host_user.nid'), primary_key=True),)

class HostToHostUser(Base):
    __tablename__ = 'host_to_host_user'
    nid = Column(Integer, primary_key=True, autoincrement=True)

    host_id = Column(Integer, ForeignKey('host.nid'))
    host_user_id = Column(Integer, ForeignKey('host_user.nid'))


class Host(Base):
    __tablename__ = 'host'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(32))
    port = Column(String(32))
    ip = Column(String(32))

    host_user = relationship('HostUser', secondary=HostToHostUser.__table__, backref='h')


class HostUser(Base):
    __tablename__ = 'host_user'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))

Session = sessionmaker(bind=engine)
session = Session()

host_obj = session.query(Host).filter(Host.hostname == 'c1').first()
print(host_obj.host_user)