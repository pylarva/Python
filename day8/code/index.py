# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:lichengbing
from setting import ClassName
from setting import Path


def execute():
    model = __import__(Path, fromlist=True)
    cls = getattr(model, ClassName)
    obj = cls()
    obj.f1()

if __name__ == '__main__':
    execute()