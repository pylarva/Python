# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys, os, pickle, prettytable, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from conf.setting import *

# 定义登录状态的常量

LOGIN_STATE = False


def check_login(func):
    """

    装饰器,判断管理员权限

    :param func:

    :return:

    """

    def inner(*args, **kwargs):

        if LOGIN_STATE:  # 判断是否已登录

            res = func(*args, **kwargs)

            return res

        else:
            print('程序需要登录后才可执行!')

    return inner


def data_read():
    """

    老师DB读取函数

    :return: 读取结果

    """

    data = pickle.load(open(manage_data_file, 'rb'))

    return data


def data_flush(args):
    """

    写入修改后的新教师类数据

    :param args: 修改后的老师数据

    :return:

    """

    pickle.dump(args, open(manage_data_file, 'wb'))


def subject_data_read():
    """

    读取课程类的数据

    :return: 读取结果

    """

    subject_data = pickle.load(open(subject_data_file, 'rb'))

    return subject_data


def subject_data_flush(args):
    """

    写入修改后的课程类数据

    :param args: 修改后的数据

    :return:

    """

    pickle.dump(args, open(subject_data_file, 'wb'))


def sub_match_teacher(sub_classes):
    """

    匹配课程类中的老师名称与老师类数据中的老师对象

    :param sub_classes:课程名称

    :return:匹配到的老师对象以及对应的索引

    """

    # 读取课程数据

    subject_data = subject_data_read()

    # 遍历课程数据,查找到课堂的名称

    for item in subject_data:

        if sub_classes == item.classes:
            teac_name = item.teacher_name

    # 遍历教师数据,查找到对应老师的对象以及下标值

    teacher_data = data_read()

    for item in teacher_data:

        if item.name == teac_name:
            teacher_ob = item

            index = teacher_data.index(item)

    return teacher_ob, index


def teacher_name():
    """

    生成教师名字列表函数

    :return: 返回名字列表

    """

    manage_data = data_read()

    teacher_list = []

    for teacher in manage_data:
        teacher_list.append(teacher.name)

    # print(teacher_list)

    return teacher_list


def subject_name():
    """

    生成课程名称列表函数

    :return: 课程名称列表

    """

    subject_data = subject_data_read()

    subject_list = []

    for subject in subject_data:
        subject_list.append(subject.classes)

    # print(subject_list)

    return subject_list


@check_login
def creat_teacher():
    """

    创建教师函数

    :return:

    """

    # 读取教书数据

    manage_data = data_read()

    teacher_list = teacher_name()

    name = input('输入教师姓名:')

    if name in teacher_list:  # 判断是否已存在此教师

        print('已有教师:%s的数据' % name)

    else:

        while True:

            age = input('请输入教师年龄:')

            if age.isdigit():

                age = int(age)

                break

            else:
                print('输入有误,请重新输入')

        favor = input('请输入教师爱好和擅长,可多选,使用逗号隔开:')

        # 调用教师类创建教师,并赋予相应属性

        docor_name = Teacher(name, age, favor)

        manage_data.append(docor_name)

        data_flush(manage_data)

        print('教师%s已创建成功!' % name)


@check_login
def creat_subject():
    """

    创建课程函数

    :return:

    """

    # 读取课程数据

    subject_data = subject_data_read()

    subject_list = subject_name()

    classes = input('请输入课程名称:')  # 判断是否有此课程

    if classes in subject_list:

        print('已经有%s课程' % classes)

    else:

        while True:

            value = input('请输入课时费:')

            if value.isdigit():

                value = int(value)

                break

            else:
                print('输入有误,请重新输入.')

        while True:

            print('请选择授课老师'.center(50, '*'))

            manage_data = show_teachers()

            num = input('请选择老师对应的序列号')

            if num.isdigit():

                num = int(num)

                if num < len(manage_data):

                    teacher_name = manage_data[num].name

                    # 调用课程类创建课程,并赋予相应属性

                    subject_obj = Subject(classes, value, teacher_name)

                    subject_data.append(subject_obj)

                    subject_data_flush(subject_data)

                    break

                else:
                    print('输入有误,请重新输入.')

            else:
                print('输入有误,请重新输入.')


# @check_login

def show_teachers():
    """

    显示所有教师信息函数

    :return:

    """

    # 遍历教师数据文件,并打印对应信息

    manage_data = data_read()

    row = prettytable.PrettyTable()

    row.field_names = ['序列号', '教师姓名', '年龄', '爱好', '目前资产']

    for teach in manage_data:
        row.add_row([manage_data.index(teach),

                     teach.name,

                     teach.age,

                     teach.favor,

                     teach.asset])

    print(row)

    return manage_data


def show_subject():
    """

    显示所有课程信息

    :return:

    """

    # 遍历课程数据,并显示相应信息

    subject_data = subject_data_read()

    row = prettytable.PrettyTable()

    row.field_names = ['序列号', '学科名', '课时费', '授课老师', ]

    for subject in subject_data:
        row.add_row([subject_data.index(subject),

                     subject.classes,

                     subject.value,

                     subject.teacher_name])

    print(row)

    return subject_data


def logout():
    """

    退出系统函数

    :return:

    """

    exit('程序退出!')


def menu():
    """

    打印菜单函数

    :return:

    """

    row = prettytable.PrettyTable()

    row.field_names = ['创建老师', '创建课程', '查看所有老师', '查看所有课程', '退出程序']

    row.add_row([0, 1, 2, 3, 'q&quit'])

    print(row)


def login():
    """

    登录函数

    :return:

    """

    user = input('请输入管理员用户名:')

    pwd = input('请输入密码:')

    if (user and pwd) == 'admin':

        # 登录成功后修改全局变量

        global LOGIN_STATE

        LOGIN_STATE = True

        print('登录成功!')

        return LOGIN_STATE

    else:

        print('用户名或者密码错误!')

        return False


@check_login
def main():
    """

    主函数,系统入口

    :return:

    """

    while True:

        menu()

        # 打印菜单后,将函数名形成列表让用户选择,选择后执行对应的函数

        menu_list = [creat_teacher, creat_subject, show_teachers, show_subject, logout]

        inp = input('请选择操作对应的序列号:')

        if inp.isdigit():

            inp = int(inp)

            if inp < len(menu_list):
                menu_list[inp]()

                time.sleep(1)

        elif inp == 'q' or inp == 'quit':

            logout()

        else:
            print('输入错误,请重新输入.')