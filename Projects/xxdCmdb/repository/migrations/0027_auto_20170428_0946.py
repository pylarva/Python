# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0026_remove_asset_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='authinfo',
            name='ctime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='authinfo',
            name='status',
            field=models.IntegerField(default=1, choices=[(1, b'[\xe7\x94\xb3\xe8\xaf\xb7\xe4\xb8\xad]'), (2, b'[\xe9\x80\x9a\xe8\xbf\x87]'), (3, b'[\xe6\x8b\x92\xe7\xbb\x9d]')]),
        ),
    ]
