# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing

import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMIN_DB = os.path.join(BASE_DIR, 'db', 'adm_db')

STUDENT_DB = os.path.join(BASE_DIR, 'db', 'student_db')

TEACHER_DB = os.path.join(BASE_DIR, 'db', 'teacher_db')

COURSE_DB = os.path.join(BASE_DIR, 'db', 'course_db')