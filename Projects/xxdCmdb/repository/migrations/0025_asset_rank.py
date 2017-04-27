# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0024_auto_20170427_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='rank',
            field=models.IntegerField(default=3, choices=[(1, b'root'), (2, b'admin'), (3, b'rd')]),
        ),
    ]
