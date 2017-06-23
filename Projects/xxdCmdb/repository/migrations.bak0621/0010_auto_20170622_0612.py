# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20170622_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releaselog',
            name='release_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 6, 22, 6, 12, 55, 83982, tzinfo=utc), verbose_name=b'\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
