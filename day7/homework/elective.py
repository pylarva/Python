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



