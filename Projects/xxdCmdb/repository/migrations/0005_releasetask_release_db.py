# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-16 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20170816_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='releasetask',
            name='release_db',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]