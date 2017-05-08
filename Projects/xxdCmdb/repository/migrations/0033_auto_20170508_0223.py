# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-08 02:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0032_auto_20170508_0200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup',
            name='business_one',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='business_one',
            field=models.ManyToManyField(to='repository.BusinessOne'),
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='business_three',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='business_three',
            field=models.ManyToManyField(to='repository.BusinessThree'),
        ),
        migrations.RemoveField(
            model_name='usergroup',
            name='business_two',
        ),
        migrations.AddField(
            model_name='usergroup',
            name='business_two',
            field=models.ManyToManyField(to='repository.BusinessTwo'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.UserGroup'),
        ),
    ]
