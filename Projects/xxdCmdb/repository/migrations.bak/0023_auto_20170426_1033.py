# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0022_auto_20170426_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='host_ip',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]