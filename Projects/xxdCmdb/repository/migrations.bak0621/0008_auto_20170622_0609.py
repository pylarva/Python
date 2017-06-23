# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20170621_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disk',
            name='model',
        ),
        migrations.RemoveField(
            model_name='nic',
            name='netmask',
        ),
        migrations.RemoveField(
            model_name='nic',
            name='up',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_cores',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_count',
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_model',
        ),
        migrations.RemoveField(
            model_name='server',
            name='os_version',
        ),
        migrations.RemoveField(
            model_name='server',
            name='over_insured_time',
        ),
        migrations.RemoveField(
            model_name='server',
            name='putaway_time',
        ),
        migrations.AddField(
            model_name='nic',
            name='switch_ip',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe4\xb8\x8a\xe8\x81\x94\xe4\xba\xa4\xe6\x8d\xa2\xe6\x9c\xbaIP', blank=True),
        ),
        migrations.AddField(
            model_name='nic',
            name='switch_port',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe4\xb8\x8a\xe8\x81\x94\xe4\xba\xa4\xe6\x8d\xa2\xe6\x9c\xba\xe7\xab\xaf\xe5\x8f\xa3', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='cabinet',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe6\x9c\xba\xe6\x9f\x9c', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='cpu',
            field=models.ForeignKey(default=django.db.models.deletion.SET_NULL, blank=True, to='repository.Cpu', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='idc',
            field=models.CharField(max_length=32, null=True, verbose_name=b'IDC', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='putaway',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe4\xb8\x8a\xe6\x9e\xb6\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='raid',
            field=models.CharField(max_length=8, null=True, verbose_name=b'Raid', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='service',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe4\xbf\x9d\xe4\xbf\xae\xe6\x9c\x9f', blank=True),
        ),
        migrations.AlterField(
            model_name='nic',
            name='hwaddr',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe7\xbd\x91\xe5\x8d\xa1mac\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
        ),
        migrations.AlterField(
            model_name='nic',
            name='ipaddrs',
            field=models.CharField(max_length=256, null=True, verbose_name=b'ip\xe5\x9c\xb0\xe5\x9d\x80', blank=True),
        ),
        migrations.AlterField(
            model_name='nic',
            name='name',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe7\xbd\x91\xe5\x8d\xa1\xe5\x90\x8d\xe7\xa7\xb0', blank=True),
        ),
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 22, 6, 9, 2, 392506, tzinfo=utc), verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='server',
            name='hostname',
            field=models.CharField(unique=True, max_length=128, verbose_name=b'\xe4\xb8\xbb\xe6\x9c\xba\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='server',
            name='manage_ip',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xae\xa1\xe7\x90\x86IP', blank=True),
        ),
    ]
