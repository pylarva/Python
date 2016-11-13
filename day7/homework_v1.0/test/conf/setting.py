# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os, sys, time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

"""

配置文件

"""

# 存储老师信息的数据文件

manage_data_file = '%s/data/manage.pickle' % BASE_DIR

# 存储课程信息的数据文件

subject_data_file = '%s/data/subject.pickle' % BASE_DIR

# 存储学生信息的数据文件

student_data_file = '%s/data/student.pickle' % BASE_DIR


# 定义教师类

class Teacher:
    def __init__(self, name, age, favor):
        self.favor = favor

        self.name = name

        self.age = age

        self.asset = 0

    def gain(self, value):
        """

        上课时老师资产增加

        :param value: 课程的课时费

        :return:

        """

        self.asset = int(self.asset) + int(value)

    def teach_accidents(self):
        """

        课程事故时老师资产减少

        :return:

        """

        self.asset -= 1


from core import manage_sys


# 定义课程类

class Subject:
    def __init__(self, classes, value, teacher_name):  # 构造方法

        self.classes = classes

        self.value = int(value)

        self.teacher_name = teacher_name

    def attend_class(self):
        """

        课程上课,并对相应老师的资产做相应调整

        :return:

        """

        print('来上课,今天我们学%s' % self.classes)

        print(5 * ('%s...' % self.classes))

        time.sleep(1)

        print('齐活!下课下课!!!')

        teacher_obj, index = manage_sys.sub_match_teacher(self.classes)

        # 执行老师对象的资产增加方法

        teacher_obj.gain(self.value)

        teacher_data = manage_sys.data_read()

        teacher_data[index] = teacher_obj

        manage_sys.data_flush(teacher_data)

    def accidents(self):
        """

        课堂事故,并对相应老师的资产做相应调整,

        :return:

        """

        print('卧槽,今天上不了课了,%s老师去做大保健了' % self.teacher_name)

        print(5 * '大保健...')

        time.sleep(1)

        print('退钱退钱退钱!!!')

        teacher_obj, index = manage_sys.sub_match_teacher(self.classes)

        # 执行老师对象的资产减少方法

        teacher_obj.teach_accidents()

        teacher_data = manage_sys.data_read()

        teacher_data[index] = teacher_obj

        manage_sys.data_flush(teacher_data)


# 定义学生的类

class Student:
    def __init__(self, name, pwd):
        self.name = name

        self.pwd = pwd

        self.subject_classes = []