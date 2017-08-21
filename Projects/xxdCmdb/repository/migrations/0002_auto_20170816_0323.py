# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-16 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='releasetask',
            name='apply_time',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='releasetask',
            name='apply_user',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='releasetask',
            name='check_time',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='releasetask',
            name='check_user',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='releasetask',
            name='release_status',
            field=models.IntegerField(blank=True, choices=[(1, '发布中'), (2, '发布成功'), (3, '发布失败'), (4, '待审核')], default=1, null=True),
        ),
    ]