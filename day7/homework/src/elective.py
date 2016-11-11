# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


class Teacher:

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.asset = 0

    def absence(self):
        self.asset -= 1

    def gain(self, value):
        self.asset += value


class Course:

    def __init__(self, name, award, time, teacher_obj):
        self.name = name
        self.award = award
        self.time = time
        self.teacher = teacher_obj.name


class Student:

    def __init__(self, name, pwd, age, gender):
        self.name = name
        self.pwd = pwd
        self.age = age
        self.gender = gender
        self.list = []
        self.record = []

    # def select_course(self):




