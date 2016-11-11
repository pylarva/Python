# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import configparser
from src import elective
import pickle
from config import setting
from lib.decryption import decryption_pwd


def login(num):
    if num == 1:
        config = configparser.ConfigParser()
        config.read(setting.ADMIN_DB, encoding='utf-8')

        while True:
            user_name = input('请输入用户名： ')
            user_password = input('请输入密码： ')
            if config.has_option(user_name, 'password'):
                user_password = decryption_pwd(user_password)
                if config.get(user_name, 'password') == user_password:
                    return True
                else:
                    print('密码错误...')
            else:
                print('用户名不存在...')
                continue

    elif num == 2:

        while True:
            stu_name = input('输入用户名： ')
            stu_pwd = input('输入密码： ')
            stu_list = pickle.load(open(setting.STUDENT_DB, 'rb'))

            for item in stu_list:
                if item.name == stu_name and item.pwd == stu_pwd:
                    return True
            print('用户名或密码错误!')


def create_teacher():
    teacher_list = pickle.load(open(setting.TEACHER_DB, 'rb'))
    # teacher_list = []
    teacher_name = input('请输入老师姓名： ')
    teacher_gender = input('性别： ')
    teacher_age = input('请输入老师年龄： ')
    teacher_obj = elective.Teacher(name=teacher_name, age=teacher_age, gender=teacher_gender)
    teacher_list.append(teacher_obj)
    pickle.dump(teacher_list, open(setting.TEACHER_DB, 'wb'))
    print('创建成功！')
    # r = pickle.load(open(setting.TEACHER_DB, 'rb'))
    # print(r[0].name)


def create_course():
    course_list = pickle.load(open(setting.COURSE_DB, 'rb'))
    # course_list = []
    course_name = input('输入课程名称：')
    course_award = input('课时费： ')
    course_time = input('上课时间： ')
    teacher_list = pickle.load(open(setting.TEACHER_DB, 'rb'))
    for k, v in enumerate(teacher_list):
        print(k+1, v.name)
    select_teacher = input('关联老师，输入编号： ')
    course_teacher = teacher_list[int(select_teacher) - 1]
    print('关联老师: \033[31;0m%s\033[0m 成功！' % teacher_list[int(select_teacher) - 1].name)
    course_obj = elective.Course(name=course_name, award=course_award, time=course_time,
                                 teacher_obj=teacher_list[int(select_teacher) - 1])
    course_list.append(course_obj)
    pickle.dump(course_list, open(setting.COURSE_DB, 'wb'))
    print('创建课程成功！')


def admin():
    ret = login(1)
    if ret:
        show_menu = '''
            \033[35;0m-------------- 管理后台 ---------------\033[0m
            \033[32;0m1、创建老师
            2、创建课程
            3、退出
            \033[0m'''
        print(show_menu)
        while True:
            innp = input('请输入编号： ')
            if innp == '1':
                create_teacher()
                pass
            elif innp == '2':
                create_course()
            elif innp == 'q':
                pass


def student():
    ret = login(2)
    if ret:
        print('-----------  课程列表  -----------')
        course_list = pickle.load(open(setting.COURSE_DB, 'rb'))
        for k, v in enumerate(course_list):
            print(k, v.name, v.time, v.teacher)


def register():
    print('-----------  学生注册  -----------')

    while True:
        student_list = pickle.load(open(setting.STUDENT_DB, 'rb'))
        # student_list = []
        student_name = input('输入新用户名： ')
        student_pwd = input('输入密码： ')
        student_age = input('年龄： ')
        student_gender = input('性别： ')
        if student_name and student_pwd and student_age and student_gender:
            student_obj = elective.Student(student_name, student_pwd, student_age, student_gender)
            student_list.append(student_obj)
            pickle.dump(student_list, open(setting.STUDENT_DB, 'wb'))
            print('注册成功!')
            break
        else:
            print('输入有误...')
            continue

'''
def register():
    config = configparser.ConfigParser()
    config.read(setting.STUDENT_DB, encoding='utf-8')
    print('-----------  学生注册  -----------')

    while True:
        user_name = input('请输入新用户名： ')
        user_pwd = input('请输入用户密码： ')

        if user_name and user_pwd:
             if not config.has_section(user_name):
                 config.add_section(user_name)
                 user_pwd = decryption_pwd(user_pwd)
                 config.set(user_name, 'password', user_pwd)
                 config.write(open(setting.STUDENT_DB, 'w'))
                 print('注册成功！')
                 return
             else:
                 print('用户已经存在...')
                 continue
        else:
            print('用户名或密码不能为空...')
            continue
'''

def out():
    pass


def main():
    show_menu = '''
    \033[35;0m-------------- 选课中心 ---------------\033[0m
    \033[32;0m1、管理登陆
    2、学生登陆
    3、学生注册
    4、退出
    \033[0m'''
    show_dic = {
        '1': admin,
        '2': student,
        '3': register,
        '4': out
    }
    while True:
        print(show_menu)
        user_select = input('输入编号 >> ')
        if user_select in show_dic:
            show_dic[user_select]()
        else:
            continue