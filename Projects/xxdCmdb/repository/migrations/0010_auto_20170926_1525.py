# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-26 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20170919_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesstwo',
            name='business_remark',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='备注'),
        ),
        migrations.AddField(
            model_name='businesstwo',
            name='business_url',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='业务线接口地址'),
        ),
    ]