# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-10 05:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0038_auto_20170510_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, to='repository.UserGroup'),
        ),
    ]
