# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
import pickle
import sys
from conf import setting
from lib import modules


def login():
    """
    管理员登陆
    :return:
    """
    print('\033[35;0m-----------  选课后台登陆  -------------\033[35;0m')

    while True:
        user_name = input('请输入管理员用户名： ')
        user_pwd = input('请输入密码: ')

        if (user_name and user_pwd) == 'admin':
            print('欢迎 \033[31;0m%s\033[0m 登陆成功！' % user_name)
            time.sleep(1)
            break
        else:
            print('用户名或者密码错误...')


def teacher_db_read():
    """
    读取老师数据库
    :return: 所有包含老师对象的列表， 老师姓名组成的列表
    """
    teacher_data = pickle.load(open(setting.TEACHER_DB, 'rb'))
    teacher_list = []
    for index, teacher in enumerate(teacher_data):
        teacher_list.append(teacher.name)
    return teacher_data, teacher_list


def teacher_db_save(teacher_data):
    pickle.dump(teacher_data, open(setting.TEACHER_DB, 'wb'))


def create_teacher():
    """
    创建老师
    :return:
    """
    # 读取老师数据库, 得到一个以所有老师姓名组成的列表
    teacher_data, teacher_list = teacher_db_read()
    # teacher_data = []
    # teacher_list = []

    while True:
        teacher_name = input('输入老师的姓名： ')
        if teacher_name in teacher_list:
            print('老师 \033[31;0m%s\033[0m 已经存在! ' % teacher_name)
            continue
        else:
            teacher_age = input('输入老师的年龄： ')
            if not teacher_age.isdigit():
                print('输入有误...')
                continue
            teacher_gender = input('输入老师的性别： ')
            if not teacher_gender == '男' or teacher_gender == '女':
                print('输入有误...')
                continue

            # 调用教师类对象创建老师
            teacher_obj = modules.TEACHER(name=teacher_name, age=teacher_age, gender=teacher_gender)
            teacher_data.append(teacher_obj)
            # 保存老师数据库
            teacher_db_save(teacher_data)
            print('创建老师 \033[31;0m%s\033[0m 成功!' % teacher_name)
            time.sleep(1)
            break


def course_db_read():
    """
    读取课程数据库
    :return:返回包括所有课程对象的列表
    """
    course_data = pickle.load(open(setting.COURSE_DB, 'rb'))
    course_list = []
    for index, course in enumerate(course_data):
        course_list.append(course.name)
    return course_data, course_list


def course_db_save(course_data):
    """
    保存课程数据库
    :return:
    """
    pickle.dump(course_data, open(setting.COURSE_DB, 'wb'))


def create_crouse():
    """
    创建课程
    :return:
    """
    # 读取课程数据库, 得到一个以所有课程名组成的列表
    course_data, course_list = course_db_read()
    # course_data = []
    # course_list = []

    # 输入课程基本信息
    while True:
        course_name = input('输入课程名： ')
        if course_name in course_list:
            print('课程 \033[31;0m%s\033[0m 已经存在! ' % course_name)
            continue
        else:
            course_award = input('输入课时费： ')
            if not course_award.isdigit():
                print('输入有误...')
                continue
            course_time = input('上课时间： ')
            if not course_time:
                print('输入有误...')
                continue

            # 展示所有老师信息供选择并关联
            index = show_all_teacher()
            teacher_index = input('输入老师编号并关联[q退出]: ')
            if teacher_index == 'q':
                break
            if teacher_index.isdigit():
                if int(teacher_index) - 1 <= index:
                    # 读取老师数据库第 index 的老师对象
                    teacher_data, teacher_list = teacher_db_read()
                    course_teacher = teacher_data[int(teacher_index) - 1]
                else:
                    print('输入有误...')
                    continue

            # 调用课程类对象创建课程
            course_obj = modules.COURSE(name=course_name, award=course_award, time=course_time, teacher=course_teacher)
            course_data.append(course_obj)
            # 保存老师数据库
            course_db_save(course_data)
            print('创建课程 \033[31;0m%s\033[0m 成功!' % course_name)
            time.sleep(1)
            break


def show_all_teacher():
    print('序号  姓名     年龄  性别  资产')
    # 读取老师数据库
    all_teacher, teacher_list = teacher_db_read()
    for index, teacher in enumerate(all_teacher):
        print('%-5d %-5s %-5s %-5s %s' % (index+1, teacher.name, teacher.age, teacher.gender, teacher.asset))
    out = input('[Enter]继续...')
    return index


def show_all_course():
    print('序号  名称     学时费  上课时间  上课老师')
    # 读取课程数据库
    all_course, course_list = course_db_read()
    for index, course in enumerate(all_course):
        print('%-5d %-5s %-5s %-5s %s' % (index + 1, course.name, course.award, course.time, course.teacher.name))
    out = input('[Enter]继续...')
    return index


def logout():
    print('退出系统...')
    time.sleep(1)
    sys.exit()


def main():
    """
    选课后台管理主程序
    :return:
    """
    show_menu = '''\033[35;0m----------  选课后台管理  ----------\033[35;0m
    \033[32;0m1、创建老师
    2、创建课程
    3、查看所有老师
    4、查看所有课程
    5、退出
    \033[0m'''
    show_dic = {
        '1': create_teacher,
        '2': create_crouse,
        '3': show_all_teacher,
        '4': show_all_course,
        '5': logout
    }

    while True:
        print(show_menu)
        innp = input('选择编号>> ')

        if innp.isdigit():
            if int(innp) < 6:
                show_dic[innp]()
        else:
            print('输入错误...')