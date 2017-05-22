# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 07:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0061_auto_20170519_0316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='release_last_id',
            field=models.IntegerField(blank=True, default='-', null=True),
        ),
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 19, 7, 27, 4, 431351, tzinfo=utc), verbose_name='时间'),
        ),
    ]
