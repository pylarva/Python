# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-10 05:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0036_auto_20170509_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.OneToOneField(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserGroup'),
        ),
    ]
