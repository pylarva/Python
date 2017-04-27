# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0025_asset_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='rank',
        ),
    ]
