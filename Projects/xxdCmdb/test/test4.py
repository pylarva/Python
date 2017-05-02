#!/usr/bin/env python
# coding: utf-8

from repository import models

obj = models.AuthInfo.objects.filter(id=38).all()
print(obj[0].ip)