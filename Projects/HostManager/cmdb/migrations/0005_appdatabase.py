# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0004_auto_20170307_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('r', models.ManyToManyField(to='cmdb.HostDatabase')),
            ],
        ),
    ]
