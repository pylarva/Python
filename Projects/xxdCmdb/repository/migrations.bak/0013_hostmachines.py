# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_virtualmachines_mudroom_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostMachines',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_machines_ip', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name_plural': '\u5bbf\u4e3b\u673a\u8868',
            },
        ),
    ]
