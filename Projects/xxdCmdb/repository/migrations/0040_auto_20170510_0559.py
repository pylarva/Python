# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-10 05:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0039_auto_20170510_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserGroup'),
        ),
    ]
