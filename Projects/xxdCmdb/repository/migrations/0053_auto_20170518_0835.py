# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-18 08:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0052_auto_20170518_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='git_branch',
            field=models.CharField(blank=True, default='输入发布分支', max_length=32, null=True),
        ),
    ]
