# !/usr/bin/env python
# -*- coding:utf-8 -*-

class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1

    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst

    def get_no_of_instance1(c):
        return c.no_inst

k1 = Kls()
# k2 = Kls()

print(k1.get_no_of_instance())
# print(k1.get_no_of_instance1())
