# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import pickle
import time
import sys
from lib import modules
from conf import setting
from src import admin

USER_NAME = ''


def student_db_read():
    """
    读取学生数据库
    :return: 返回学生数据库中以学生类为元素创建的列表， 一个由学生名组成的字典
    """
    student_data = pickle.load(open(setting.STUDENT_DB, 'rb'))
    student_dic = {}

    for index, student in enumerate(student_data):
        stu_dic = {student.name: student.pwd}
        student_dic.update(stu_dic)
    return student_data, student_dic


def login():
    """
    学生登陆函数
    :return:
    """
    student_data, student_dic = student_db_read()
    print('---------  学生登陆 ---------')

    while True:
        user_name = input('请输入用户名： ')
        if user_name not in student_dic:
            print('用户名不存在...')
            continue
        user_pwd = input('请输入密码： ')
        if not student_dic.get(user_name) == user_pwd:
            print('密码错误...')
            continue
        else:
            global USER_NAME
            USER_NAME = user_name
            print('欢迎 \033[31;0m%s\033[0m, 登陆成功!' % user_name)
            time.sleep(1)
            break
    return student_data, student_dic


def outer(func):
    """
    登陆装饰器 使用功能前需先登陆
    :param func:
    :return:
    """
    def inner():
        if USER_NAME == '':
            print('您还未登陆,请先登陆...')
            time.sleep(1)
            ret = login()
            if ret:
                func()
        else:
            func()
    return inner


def student_db_save(student_data):
    """
    保存学生数据库
    :param student_data:
    :return:
    """
    pickle.dump(student_data, open(setting.STUDENT_DB, 'wb'))


def register():
    """
    学生注册
    :return: 
    """
    # 读取学生数据库, 得到一个以所有学生姓名组成的列表
    student_data, student_dic = student_db_read()
    # student_data = []
    # student_dic = {}

    while True:
        student_name = input('输入新学生的姓名： ')
        if student_name in student_dic:
            print('学生 \033[31;0m%s\033[0m 已经存在! ' % student_name)
            continue
        student_pwd = input('输入密码： ')
        confirm_pwd = input('确认密码： ')
        if not student_pwd and student_pwd == confirm_pwd:
            print('两次密码不一致...')
            continue
        student_age = input('输入学生的年龄： ')
        if not student_age.isdigit():
            print('输入有误...')
            continue
        student_gender = input('输入学生的性别： ')
        if not student_gender == '男' or student_gender == '女':
            print('输入有误...')
            continue

        # 调用学生类对象创建学生
        student_obj = modules.STUDENT(name=student_name, pwd=student_pwd, age=student_age, gender=student_gender)
        student_data.append(student_obj)
        # 保存学生数据库
        student_db_save(student_data)
        print('学生 \033[31;0m%s\033[0m 注册成功!' % student_name)
        time.sleep(1)
        break


def student_have_class(student_obj):
    """
    读取学生数据库得到其中已选课程列表
    :param student_obj:
    :return:
    """
    student_have_class_list =[]
    for k, v in enumerate(student_obj.class_list):
        student_have_class_list.append(v.name)
    return student_have_class_list


def show_student_classes(student_obj):
    """
    展示学生已选的课程列表
    :return:
    """
    # 展示该学生当前已选的课程
    print('--------  已选课程  ----------')
    if not student_obj.class_list:
        print('<  无  >')
    else:
        print('序号    课程    老师')
        for index, item in enumerate(student_obj.class_list):
            print(index + 1, item.name, item.teacher.name)
        print('--------  end  ----------')
        return index


def catch_student_obj(student_data):
    """
    用登陆用户找出学生数据库中该学生对象
    :return:
    """
    # student_data, student_dic = student_db_read()
    # 找到数据库中登陆用户的 学生类对象
    for index, student in enumerate(student_data):
        if USER_NAME == student.name:
            student_obj = student
    return student_obj, student_data


@outer
def choose_class():
    """
    学生选课
    :return:
    """
    # 读取学生数据库
    student_data, student_dic = student_db_read()
    # 读取课程数据库
    course_date, course_list = admin.course_db_read()
    # 找到数据库中登陆用户的 学生类对象
    student_obj, student_data = catch_student_obj(student_data)
    print(student_obj.name)
    # 得到学生已选课程列表
    student_have_class_list = student_have_class(student_obj)

    # 展示该学生当前已选的课程
    show_student_classes(student_obj)

    # 展示所有课程列表
    print('-------------  总课程列表  ---------------')
    index = admin.show_all_course()

    while True:
        # 选择的课程编号 == 课程数据库列表顺序
        innp = input('选择课程编号[q退出]>> ')
        if innp == 'q':
            break
        if innp.isdigit() and int(innp) <= index + 1:
            # 检查课程是否重复
            if course_date[int(innp) - 1].name in student_have_class_list:
                print('已有该学习课程,不能重复选择...')
                continue
            course_obj = course_date[int(innp) - 1]
            # 将被选择的课程对象添加进学生数据库
            student_obj.class_list.append(course_obj)
            # 写入数据库
            student_db_save(student_data)
            print('添加课程 \033[31;0m%s\033[0m 成功! ' % course_obj.name)
            break
        else:
            print('输入错误...')


@outer
def attend_class():
    student_data, student_dic = student_db_read()
    # 找到数据库中登陆用户的 学生类对象
    student_obj, student_data = catch_student_obj(student_data)
    # 展示该学生当前已选的课程
    index = show_student_classes(student_obj)

    while True:
        innp = input('输入上课课程编号[q退出]>> ')
        if innp == 'q':
            break
        if innp.isdigit() and int(innp) <= index + 1:
            # 课程名
            course_name = student_obj.class_list[int(innp) - 1].name
            # 由课程名找到课程对象在数据库中的存储索引 再由索引找到课程对象
            course_data, course_list = admin.course_db_read()
            course_index = course_list.index(course_name)
            course_obj = course_data[course_index]
            # 执行上课方法
            course_obj.attend_class()
            break


@outer
def teacher_evaluate():
    """
    评价老师 如果给差评 老师会被扣钱
    :return:
    """
    student_data, student_dic = student_db_read()
    # 找到数据库中登陆用户的 学生类对象
    student_obj, student_data = catch_student_obj(student_data)
    # 展示该学生当前已选的课程
    index = show_student_classes(student_obj)

    while True:
        innp = input('输入上课课程编号[q退出]>> ')
        if innp == 'q':
            break
        if innp.isdigit() and int(innp) <= index + 1:
            # 课程名
            course_name = student_obj.class_list[int(innp) - 1].name
            # 由课程名找到课程对象在数据库中的存储索引 再由索引找到课程对象
            course_data, course_list = admin.course_db_read()
            course_index = course_list.index(course_name)
            course_obj = course_data[course_index]

            while True:
                student_evaluate = input('[1]点赞 [2]差评...')
                if student_evaluate == '1':
                    print('给老师5 \033[31;0m%s\033[0m 点攒成功! ' % course_obj.teacher.name)
                    time.sleep(1)
                    break
                elif student_evaluate == '2':
                    # 执行扣钱方法
                    course_obj.teacher_evaluate()
                    break
        break


def student_class_record(course_name):
    """
    上课记录
    :param course_name:
    :return:
    """
    student_data, student_dic = student_db_read()
    student_obj, student_data = catch_student_obj(student_data)

    record = '{0} 上了一节 {1} 课...'.format(time.strftime('%Y-%m-%d %H:%m'), course_name)
    student_obj.class_record.append(record)
    student_db_save(student_data)


@outer
def class_record():
    """
    读取上课记录
    :return:
    """
    student_data, student_dic = student_db_read()
    student_obj, student_data = catch_student_obj(student_data)

    for item in student_obj.class_record:
        print(item)


def logout():
    """
    注销
    :return:
    """
    global USER_NAME
    if not USER_NAME:
        print('还未登陆...')
        time.sleep(1)
    else:
        USER_NAME = ''
        print('注销成功...')
        time.sleep(1)


def quit_sys():
    """
    退出系统
    :return:
    """
    sys.exit()


def main():
    """
    学生选课主程序
    :return:
    """
    show_menu = '''\033[35;0m----------  学生选课系统  ----------\033[35;0m
        \033[32;0m1、学生登陆
        2、学生注册
        3、学生选课
        4、学生上课
        5、评价老师
        6、上课记录
        7、注销
        8、退出
        \033[0m'''
    show_dic = {
        '1': login,
        '2': register,
        '3': choose_class,
        '4': attend_class,
        '5': teacher_evaluate,
        '6': class_record,
        '7': logout,
        '8': quit_sys
    }

    while True:
        print(show_menu)
        innp = input('选择编号>> ')

        if innp.isdigit():
            if innp in show_dic:
                show_dic[innp]()
        else:
            continue