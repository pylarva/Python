# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-13 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_ippool'),
    ]

    operations = [
        migrations.AddField(
            model_name='ippool',
            name='status',
            field=models.IntegerField(choices=[(1, '在线'), (2, '空闲'), (3, '禁用')], default=2),
        ),
    ]
