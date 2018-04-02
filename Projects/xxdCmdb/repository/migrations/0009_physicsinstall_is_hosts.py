# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-04-02 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_dellserver_asset_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='physicsinstall',
            name='is_hosts',
            field=models.IntegerField(choices=[(1, '是'), (0, '否')], default=0, verbose_name='是否为宿主机'),
        ),
    ]
