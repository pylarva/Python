# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 08:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0070_auto_20170531_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 31, 8, 46, 58, 811030, tzinfo=utc), verbose_name='时间'),
        ),
    ]
