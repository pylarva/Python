# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_releaselog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
            ],
            options={
                'verbose_name_plural': 'CPU\u8868',
            },
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu_physical_count',
        ),
        migrations.RemoveField(
            model_name='server',
            name='create_at',
        ),
        migrations.RemoveField(
            model_name='server',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='server',
            name='os_platform',
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_cores',
            field=models.IntegerField(null=True, verbose_name=b'CPU\xe9\x80\xbb\xe8\xbe\x91\xe6\xa0\xb8\xe5\xbf\x83\xe6\x95\xb0', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='over_insured_time',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe8\xbf\x87\xe4\xbf\x9d\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='putaway_time',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe4\xb8\x8a\xe6\x9e\xb6\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=1, blank=True, to='repository.BusinessOne', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf1'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=1, blank=True, to='repository.BusinessTwo', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf2'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_3',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=1, blank=True, to='repository.BusinessThree', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf3'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='host_status',
            field=models.IntegerField(default=2, choices=[(1, b'\xe5\x9c\xa8\xe7\xba\xbf'), (2, b'\xe7\xa6\xbb\xe7\xba\xbf')]),
        ),
        migrations.AlterField(
            model_name='asset',
            name='host_type',
            field=models.IntegerField(default=2, choices=[(1, b'\xe7\x89\xa9\xe7\x90\x86\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8'), (2, b'\xe8\x99\x9a\xe6\x8b\x9f\xe6\x9c\xba'), (3, b'\xe7\xbd\x91\xe7\xbb\x9c\xe8\xae\xbe\xe5\xa4\x87')]),
        ),
        migrations.AlterField(
            model_name='assets',
            name='business_unit',
            field=models.ForeignKey(verbose_name=b'\xe5\xb1\x9e\xe4\xba\x8e\xe7\x9a\x84\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf', blank=True, to='repository.BusinessUnit', null=True),
        ),
        migrations.AlterField(
            model_name='assets',
            name='cabinet_num',
            field=models.CharField(max_length=30, null=True, verbose_name=b'\xe6\x9c\xba\xe6\x9f\x9c\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='assets',
            name='cabinet_order',
            field=models.CharField(max_length=30, null=True, verbose_name=b'\xe6\x9c\xba\xe6\x9f\x9c\xe4\xb8\xad\xe5\xba\x8f\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='assets',
            name='device_status_id',
            field=models.IntegerField(default=1, choices=[(1, b'\xe4\xb8\x8a\xe6\x9e\xb6'), (2, b'\xe5\x9c\xa8\xe7\xba\xbf'), (3, b'\xe7\xa6\xbb\xe7\xba\xbf'), (4, b'\xe4\xb8\x8b\xe6\x9e\xb6')]),
        ),
        migrations.AlterField(
            model_name='assets',
            name='device_type_id',
            field=models.IntegerField(default=1, choices=[(1, b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8'), (2, b'\xe4\xba\xa4\xe6\x8d\xa2\xe6\x9c\xba'), (3, b'\xe9\x98\xb2\xe7\x81\xab\xe5\xa2\x99')]),
        ),
        migrations.AlterField(
            model_name='assets',
            name='idc',
            field=models.ForeignKey(verbose_name=b'IDC\xe6\x9c\xba\xe6\x88\xbf', blank=True, to='repository.IDC', null=True),
        ),
        migrations.AlterField(
            model_name='authinfo',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'[\xe7\x94\xb3\xe8\xaf\xb7\xe4\xb8\xad]'), (2, b'[\xe5\xb7\xb2\xe9\x80\x9a\xe8\xbf\x87]'), (3, b'[\xe5\xb7\xb2\xe6\x8b\x92\xe7\xbb\x9d]')]),
        ),
        migrations.AlterField(
            model_name='businessone',
            name='name',
            field=models.CharField(unique=True, max_length=64, verbose_name=b'\xe4\xb8\x80\xe7\xba\xa7\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf'),
        ),
        migrations.AlterField(
            model_name='businessthree',
            name='name',
            field=models.CharField(unique=True, max_length=64, verbose_name=b'\xe4\xb8\x89\xe7\xba\xa7\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf'),
        ),
        migrations.AlterField(
            model_name='businesstwo',
            name='name',
            field=models.CharField(unique=True, max_length=64, verbose_name=b'\xe4\xba\x8c\xe7\xba\xa7\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='contact',
            field=models.ForeignKey(related_name='c', verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe8\x81\x94\xe7\xb3\xbb\xe4\xba\xba', to='repository.UserGroup'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='manager',
            field=models.ForeignKey(related_name='m', verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\xae\xa1\xe7\x90\x86\xe5\x91\x98', to='repository.UserGroup'),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='name',
            field=models.CharField(max_length=64, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='capacity',
            field=models.FloatField(verbose_name=b'\xe7\xa3\x81\xe7\x9b\x98\xe5\xae\xb9\xe9\x87\x8fGB'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='model',
            field=models.CharField(max_length=32, verbose_name=b'\xe7\xa3\x81\xe7\x9b\x98\xe5\x9e\x8b\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='pd_type',
            field=models.CharField(max_length=32, verbose_name=b'\xe7\xa3\x81\xe7\x9b\x98\xe7\xb1\xbb\xe5\x9e\x8b'),
        ),
        migrations.AlterField(
            model_name='disk',
            name='slot',
            field=models.CharField(max_length=8, verbose_name=b'\xe6\x8f\x92\xe6\xa7\xbd\xe4\xbd\x8d'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='floor',
            field=models.IntegerField(default=1, verbose_name=b'\xe6\xa5\xbc\xe5\xb1\x82'),
        ),
        migrations.AlterField(
            model_name='idc',
            name='name',
            field=models.CharField(max_length=32, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='capacity',
            field=models.FloatField(null=True, verbose_name=b'\xe5\xae\xb9\xe9\x87\x8f', blank=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='manufacturer',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x88\xb6\xe9\x80\xa0\xe5\x95\x86', blank=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='model',
            field=models.CharField(max_length=64, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='slot',
            field=models.CharField(max_length=32, verbose_name=b'\xe6\x8f\x92\xe6\xa7\xbd\xe4\xbd\x8d'),
        ),
        migrations.AlterField(
            model_name='memory',
            name='sn',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98SN\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='memory',
            name='speed',
            field=models.CharField(max_length=16, null=True, verbose_name=b'\xe9\x80\x9f\xe5\xba\xa6', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='device_detail',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xe8\xae\xbe\xe7\xbd\xae\xe8\xaf\xa6\xe7\xbb\x86\xe9\x85\x8d\xe7\xbd\xae', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='intranet_ip',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x86\x85\xe7\xbd\x91IP', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='management_ip',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe7\xae\xa1\xe7\x90\x86IP', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='model',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='port_num',
            field=models.SmallIntegerField(null=True, verbose_name=b'\xe7\xab\xaf\xe5\x8f\xa3\xe4\xb8\xaa\xe6\x95\xb0', blank=True),
        ),
        migrations.AlterField(
            model_name='networkdevice',
            name='sn',
            field=models.CharField(unique=True, max_length=64, verbose_name=b'SN\xe5\x8f\xb7'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='hwaddr',
            field=models.CharField(max_length=64, verbose_name=b'\xe7\xbd\x91\xe5\x8d\xa1mac\xe5\x9c\xb0\xe5\x9d\x80'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='ipaddrs',
            field=models.CharField(max_length=256, verbose_name=b'ip\xe5\x9c\xb0\xe5\x9d\x80'),
        ),
        migrations.AlterField(
            model_name='nic',
            name='name',
            field=models.CharField(max_length=128, verbose_name=b'\xe7\xbd\x91\xe5\x8d\xa1\xe5\x90\x8d\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'\xe6\x96\xb0\xe6\x8f\x90\xe4\xba\xa4'), (2, b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x88\x90\xe5\x8a\x9f'), (3, b'\xe5\x8f\x91\xe5\xb8\x83\xe5\xa4\xb1\xe8\xb4\xa5')]),
        ),
        migrations.AlterField(
            model_name='releaselog',
            name='release_msg',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'\xe6\x97\xa5\xe5\xbf\x97', blank=True),
        ),
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 21, 10, 33, 1, 590037, tzinfo=utc), verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='releasetask',
            name='release_status',
            field=models.IntegerField(default=1, null=True, blank=True, choices=[(1, b'\xe5\x8f\x91\xe5\xb8\x83\xe4\xb8\xad'), (2, b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x88\x90\xe5\x8a\x9f'), (3, b'\xe5\x8f\x91\xe5\xb8\x83\xe5\xa4\xb1\xe8\xb4\xa5')]),
        ),
        migrations.AlterField(
            model_name='server',
            name='cpu_count',
            field=models.IntegerField(null=True, verbose_name=b'CPU\xe4\xb8\xaa\xe6\x95\xb0', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='cpu_model',
            field=models.CharField(max_length=128, null=True, verbose_name=b'CPU\xe5\x9e\x8b\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='manage_ip',
            field=models.GenericIPAddressField(null=True, verbose_name=b'\xe7\xae\xa1\xe7\x90\x86IP', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='model',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x9e\x8b\xe5\x8f\xb7', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='os_version',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xe7\xb3\xbb\xe7\xbb\x9f\xe7\x89\x88\xe6\x9c\xac', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='sn',
            field=models.CharField(max_length=64, verbose_name=b'SN\xe5\x8f\xb7', db_index=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=32, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe'),
        ),
    ]
