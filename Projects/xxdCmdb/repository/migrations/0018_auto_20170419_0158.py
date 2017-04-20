# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0017_auto_20170419_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='host_item',
            field=models.IntegerField(default=1, choices=[(1, b'c1'), (1, b'c2')]),
        ),
        migrations.AlterField(
            model_name='asset',
            name='host_status',
            field=models.IntegerField(default=2, choices=[(1, b'\xe5\x9c\xa8\xe7\xba\xbf'), (2, b'\xe7\xa6\xbb\xe7\xba\xbf')]),
        ),
    ]
