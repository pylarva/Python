# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_auto_20170407_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachines',
            name='mudroom_host',
            field=models.CharField(default=b'192.168.1.1', max_length=32),
        ),
    ]
