# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20170831_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpnaccount',
            name='register_time',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]