# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0027_auto_20170428_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authinfo',
            name='ctime',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
