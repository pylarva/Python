# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0058_auto_20170519_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(auto_created=True, verbose_name='时间'),
        ),
    ]