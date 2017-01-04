# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:pylarva
# bolg:www.lichengbing.com

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123@10.0.0.111:3306/s13?charset=utf8", max_overflow=5)

Base = declarative_base()


# 单表
class Test(Base):
    __tablename__ = 'test'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))


# 一对多
class Group(Base):
    __tablename__ = 'group'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(32))

    def __repr__(self):
        temp = '%s  %s' %(self.nid, self.caption)
        return temp


class User(Base):
    __tablename__ = 'user'
    nid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    # 外键
    group_id = Column(Integer, ForeignKey('group.nid'))
    # 创建虚拟关系 relationship 一般与外键配合使用
    group = relationship("Group", backref='uuu')

    def __repr__(self):
        temp = '%s  %s %s' %(self.nid, self.name, self.group_id)
        return temp


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)

# init_db()
Session = sessionmaker(bind=engine)
session = Session()

# 组
# session.add(Group(caption='运维'))
# session.add(Group(caption='开发'))
# session.commit()

# 人
# session.add_all([
#     User(name='user_01', group_id=1),
#     User(name='user_02', group_id=1),
#     User(name='user_03', group_id=2),
# ])
# session.commit()

# 只获取用户
# ret = session.query(Group).all()
# print(ret)

# 获得的只是个对象 自动执行 __repr__ 方法
# ret = session.query(User).filter(User.name == 'user_01').all()
# print(ret)
# obj = ret[0]
# print(obj.nid, obj.name, obj.group_id)

# ret = session.query(User.name).all()
# print(ret)


# 联表查询
# sql = session.query(User).join(Group)
# print(sql)
# ret = session.query(User).join(Group).all()
# print(ret)

# left join
# ret = session.query(User).join(Group, isouter=True).all()
# print(ret)

# 指定映射关系
# ret = session.query(User.name, Group.caption).join(Group).all()
# print(ret)

# relationship 简化联合查询 正向查找
# ret = session.query(User).all()
# for obj in ret:
    # obj 代表 User
    # group 代表新 Group
    # print(obj.nid, obj.name, obj.group_id, obj.group.nid, obj.group.caption)

# 查所有是 运维 的人
ret = session.query(User.name, Group.caption).join(Group, isouter=True).filter(Group.caption == '运维').all()
print(ret)

# 利用relationship 新方式反向查询
obj = session.query(Group).filter(Group.caption == '运维').first()
print(obj.nid, obj.caption)
# uuu 代表在这个组下面的所有人 是一个列表
print(obj.uuu)