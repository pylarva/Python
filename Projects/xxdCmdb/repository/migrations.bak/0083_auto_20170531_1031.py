# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 10:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0082_auto_20170531_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttask',
            name='business_1',
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='business_2',
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='project_type',
        ),
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 31, 10, 31, 39, 706035, tzinfo=utc), verbose_name='时间'),
        ),
        migrations.DeleteModel(
            name='ProjectTask',
        ),
    ]