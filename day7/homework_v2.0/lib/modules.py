# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import time
from src import admin
from src import student


class TEACHER:

    def __init__(self, name,  age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.asset = 0

    def gain(self, value):
        self.asset += int(value)
        print('%s 老师加钱成功!' % self.asset)

    def fine(self, value):
        self.asset -= int(value)
        print('扣钱扣钱T T ...只剩 %s 块钱! ' % self.asset)


class COURSE:

    def __init__(self, name, award, time, teacher):
        self.name = name
        self.award = award
        self.time = time
        self.teacher = teacher

    def attend_class(self):
        """
        学生选择上课 老师加钱
        :return:
        """
        print('同学们!!老司机准备开车...')
        print(3 * ('今天我们来学 \033[31;0m%s\033[0m...\n' % self.name))
        time.sleep(1)
        print('OK...下课下课!!!')

        teacher_data, teacher_list = admin.teacher_db_read()
        teacher_name = self.teacher.name
        # 由老师的名字去数据库中找到索引
        for k, v in enumerate(teacher_list):
            if teacher_name == v:
                index = k
        teacher_obj = teacher_data[index]
        # 老师加钱
        teacher_obj.gain(self.award)
        # 上课记录
        student.student_class_record(self.name)
        time.sleep(1)
        # 保存老师数据
        admin.teacher_db_save(teacher_data)

    def teacher_evaluate(self):
        """
        学生评价老师 差评扣钱
        :return:
        """
        print('老师上课 Low 爆了...')
        teacher_data, teacher_list = admin.teacher_db_read()
        teacher_name = self.teacher.name
        # 由老师的名字去数据库中找到索引
        for k, v in enumerate(teacher_list):
            if teacher_name == v:
                index = k
        teacher_obj = teacher_data[index]
        # 老师扣钱
        teacher_obj.fine(1)
        time.sleep(1)
        # 保存老师数据
        admin.teacher_db_save(teacher_data)


class STUDENT:

    def __init__(self, name, pwd, age, gender):
        self.name = name
        self.pwd = pwd
        self.age = age
        self.gender = gender
        self.class_list = []
        self.class_record = []