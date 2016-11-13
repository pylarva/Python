# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing


class TEACHER:
    def __init__(self, name,  age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.asset = 0


class COURSE:

    def __init__(self, name, award, time, teacher):
        self.name = name
        self.award = award
        self.time = time
        self.teacher = teacher