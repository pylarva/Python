# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0018_auto_20170419_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='host_cpu',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='host_machine',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='host_memory',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='host_type',
            field=models.IntegerField(default=2, choices=[(1, b'\xe7\x89\xa9\xe7\x90\x86\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8'), (2, b'\xe8\x99\x9a\xe6\x8b\x9f\xe6\x9c\xba'), (3, b'\xe7\xbd\x91\xe7\xbb\x9c\xe8\xae\xbe\xe5\xa4\x87')]),
        ),
    ]
