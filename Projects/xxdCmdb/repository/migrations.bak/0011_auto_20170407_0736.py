# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0010_auto_20170404_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicalMachines',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=108)),
                ('host_ip', models.CharField(max_length=32)),
                ('item', models.CharField(max_length=32)),
                ('bussiness', models.CharField(max_length=32)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '\u7269\u7406\u673a\u8868',
            },
        ),
        migrations.CreateModel(
            name='VirtualMachines',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=108)),
                ('host_ip', models.CharField(max_length=32)),
                ('item', models.CharField(max_length=32)),
                ('bussiness', models.CharField(max_length=32)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '\u865a\u62df\u673a\u8868',
            },
        ),
        migrations.DeleteModel(
            name='PhysicalMachine',
        ),
        migrations.DeleteModel(
            name='VirtualMachine',
        ),
    ]
