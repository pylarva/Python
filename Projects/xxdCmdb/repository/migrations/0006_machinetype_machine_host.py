# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_machinetype_machine_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='machinetype',
            name='machine_host',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
