# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 02:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0054_auto_20170518_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_id', models.IntegerField(blank=True, null=True)),
                ('release_time', models.CharField(blank=True, max_length=32, null=True, verbose_name='时间')),
                ('release_msg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='日志')),
            ],
            options={
                'verbose_name_plural': '发布任务日志',
            },
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='release_id',
        ),
        migrations.AddField(
            model_name='projecttask',
            name='release_last_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
