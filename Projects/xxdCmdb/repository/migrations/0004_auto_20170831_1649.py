# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-31 08:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20170831_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpnaccount',
            name='active',
            field=models.IntegerField(blank=True, choices=[(1, '正常'), (2, '注销')], null=True),
        ),
    ]
