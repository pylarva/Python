# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-19 02:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20170919_1031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projecttask',
            old_name='port',
            new_name='git_url',
        ),
    ]