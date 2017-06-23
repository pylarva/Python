# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_auto_20170622_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 22, 6, 10, 42, 779442, tzinfo=utc), verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='server',
            name='cpu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Cpu', null=True),
        ),
    ]
