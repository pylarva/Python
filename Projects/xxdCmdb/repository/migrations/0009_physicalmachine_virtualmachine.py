# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_auto_20170404_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalMachine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u7269\u7406\u673a')),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u865a\u62df\u673a')),
                ('num', models.IntegerField()),
            ],
        ),
    ]
