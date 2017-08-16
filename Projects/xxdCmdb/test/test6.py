#!/usr/bin/env python
# coding: utf-8

import time
from django.utils import timezone

t = time.strftime('%Y-%m-%d %H:%M')
print(t)
# print(timezone.localtime(t))