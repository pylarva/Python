# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-13 10:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_releaselog'),
    ]

    operations = [
        migrations.AddField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 13, 10, 45, 16, 253122, tzinfo=utc), verbose_name='时间'),
        ),
    ]