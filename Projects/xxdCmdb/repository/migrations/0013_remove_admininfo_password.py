# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-31 09:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_auto_20170725_0809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admininfo',
            name='password',
        ),
    ]
