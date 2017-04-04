# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_physicalmachine_virtualmachine'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='physicalmachine',
            options={'verbose_name_plural': '\u7269\u7406\u673a\u8868'},
        ),
        migrations.AlterModelOptions(
            name='virtualmachine',
            options={'verbose_name_plural': '\u865a\u62df\u673a\u8868'},
        ),
    ]
