# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_hostdatabase'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='hostdatabase',
            name='business',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cmdb.BusinessLine'),
        ),
    ]
