# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 09:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0072_auto_20170531_0848'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReleaseLog',
        ),
        migrations.RemoveField(
            model_name='releasetask',
            name='release_env',
        ),
        migrations.RemoveField(
            model_name='releasetask',
            name='release_name',
        ),
        migrations.RemoveField(
            model_name='releasetask',
            name='release_type',
        ),
        migrations.DeleteModel(
            name='ReleaseTask',
        ),
    ]