# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0020_auto_20170420_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessthree',
            name='superior_business',
        ),
        migrations.RemoveField(
            model_name='businesstwo',
            name='superior_business',
        ),
        migrations.AlterField(
            model_name='asset',
            name='business_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=1, blank=True, to='repository.BusinessOne', null=True, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf1'),
        ),
    ]
