# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0019_auto_20170419_0206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admininfo',
            name='user_info',
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_1',
            field=models.ForeignKey(default=1, blank=True, to='repository.BusinessOne', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf1'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_2',
            field=models.ForeignKey(default=1, blank=True, to='repository.BusinessTwo', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf2'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_3',
            field=models.ForeignKey(default=1, blank=True, to='repository.BusinessThree', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf3'),
        ),
    ]
