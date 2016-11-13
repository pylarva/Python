# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import sys, os, pickle, prettytable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from conf.setting import *

from core import manage_sys


# USER=None



def student_data_read():
    """

    读取学生数据

    :return: 读取到的学生数据

    """

    student_data = pickle.load(open(student_data_file, 'rb'))

    return student_data


def student_data_flush(args):
    """

    刷新学生数据

    :param args: 新的学生数据

    :return:

    """

    pickle.dump(args, open(student_data_file, 'wb'))


def student_name():
    """

    生成学生登录用户名列表

    :return:

    """

    student_data = student_data_read()

    student_name_list = []

    for item in student_data:
        student_name_list.append(item.name)

    return student_name_list


def regist():
    """

    注册函数

    :return:

    """

    student_data = student_data_read()

    student_name_list = student_name()

    name = input('请输入您的用户名:')

    if name in student_name_list:  # 判断是否存在用户名

        print('已有用户:%s' % name)

    else:

        pwd = input('请输入您的密码:')

        for i in range(3):

            pwd_again = input('确认注册密码:')

            if pwd_again == pwd:

                print('%s注册成功!' % name)

                # 调用学生类生成学生对象,并写入学生类数据库中

                student_obj = Student(name, pwd)

                student_data.append(student_obj)

                student_data_flush(student_data)

                break

            else:

                print('密码不正确,请重新输入,还剩尝试次数%s' % (2 - i))


def s_login():
    """

    学生登录函数

    :return:

    """

    # 读取学生类数据库和学生姓名列表,两个列表的下标相匹配

    student_data = student_data_read()

    student_name_list = student_name()

    name = input('请输入您的用户名:')

    if name not in student_name_list:

        print('无%s用户名.' % name)

    else:

        for i in range(3):

            pwd = input('请输入用户%s的密码:' % name)

            # 如果输入的密码与学生类中的密码匹配

            if pwd == student_data[student_name_list.index(name)].pwd:

                global USER

                USER = name

                print('登录成功!!!')

                return True

            else:
                print('密码校验失败,剩余尝试次数:%s' % (2 - i))


def choice_subject():
    """

    选择课程函数

    :return:

    """

    # 读取学生类数据库和学生姓名列表,两个列表的下标相匹配

    student_data = student_data_read()

    student_name_list = student_name()

    # 读取课程类数据库

    subject_data = manage_sys.show_subject()

    inp = input('请选择学科名对应的序列号')

    if inp.isdigit():

        inp = int(inp)

        if inp < len(subject_data):

            # 如果输入序列符合条件,课程数据库中取到相应课程对象

            subject = subject_data[inp]

            # 学生类对象中取到课程列表,如果已有课程提示,如果无相同课程,添加入课程列表,并写入数据

            student_subject_list = student_data[student_name_list.index(USER)].subject_classes

            if subject.classes in student_subject_list:

                print('您的课表中已有%s学科!' % subject.classes)

            else:

                student_subject_list.append(subject.classes)

                student_data_flush(student_data)

                print('课程关联成功')

        else:
            print('选择有误,请重新输入')

    else:
        print('选择有误,请重新输入')


def has_subject():
    """

    显示已选课程函数

    :return:

    """

    # 读取学生类数据库和学生姓名列表,两个列表的下标相匹配

    student_data = student_data_read()

    student_name_list = student_name()

    # 读取学生对象中的对应课程列表信息,打印所有课程信息

    student_subject_list = student_data[student_name_list.index(USER)].subject_classes

    row = prettytable.PrettyTable()

    row.field_names = ['序列号', '课程名']

    for item in student_subject_list:
        row.add_row([student_subject_list.index(item), item])

    print(row)

    return student_subject_list


def s_logout():
    sys.exit('程序退出!')


def show_menu():
    """

    登录后的菜单信息函数

    :return:

    """

    row = prettytable.PrettyTable()

    row.field_names = ['选择课程', '查看已选课程', '上课', '教学事故', '退出程序']

    row.add_row([0, 1, 2, 3, '3&q&quit'])

    print(row)


def attend():
    """

    上课函数

    :return:

    """

    # 读取学生类数据库和学生姓名列表,两个列表的下标相匹配

    student_data = student_data_read()

    student_name_list = student_name()

    student_subject_list = student_data[student_name_list.index(USER)].subject_classes

    for index, item in enumerate(student_subject_list):
        print(index, item)

    inp = input('请选择课程对应的序列号:')  # 选择上课的目标课程

    if inp.isdigit():

        inp = int(inp)

        if inp < len(student_subject_list):  # 如果符合序列号标准

            # 确认课程名称

            subject_classes = student_subject_list[inp]

            # 读取课程对象数据

            subject_data = manage_sys.subject_data_read()

            # 确认相应的课程对象

            for item in subject_data:

                if item.classes == subject_classes:
                    subject_obj = item

            # 调用课程对象的上课方法

            subject_obj.attend_class()

        else:
            print('选择有误')

    else:
        print('选择有误!')


def s_accidents():
    """

    教学事故函数,与上课函数相同

    :return:

    """

    student_data = student_data_read()

    student_name_list = student_name()

    student_subject_list = student_data[student_name_list.index(USER)].subject_classes

    for index, item in enumerate(student_subject_list):
        print(index, item)

    inp = input('请选择课程对应的序列号:')

    if inp.isdigit():

        inp = int(inp)

        if inp < len(student_subject_list):

            subject_classes = student_subject_list[inp]

            subject_data = manage_sys.subject_data_read()

            for item in subject_data:

                if item.classes == subject_classes:
                    subject_obj = item

            # 调用课程对象的教学事故方法

            subject_obj.accidents()

        else:
            print('选择有误')

    else:
        print('选择有误!')


def main2():
    """

    登录后的菜单选择界面

    :return:

    """

    # 将函数名形成列表,选择后执行函数

    menu = [choice_subject, has_subject, attend, s_accidents, s_logout]

    while True:

        show_menu()

        inp = input('请选择操作对应的序列号:')

        if inp == 'q' or inp == 'quit':

            s_logout()

        elif inp.isdigit():

            inp = int(inp)

            if inp < len(menu):

                menu[inp]()

            else:
                print('输入有误,请重新输入')

        else:
            print('输入有误,请重新输入~')


def main():
    """

    主函数入口

    :return:

    """

    print('''1.登录

2.注册''')

    inp = input('请选择相应操作序列号:')

    if inp == '1':

        res = s_login()

        if res:
            main2()

    elif inp == '2':

        regist()

    else:
        print('选择有误!系统退出')





    # if __name__ == '__main__':

    #     main()