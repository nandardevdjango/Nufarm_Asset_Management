# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-12-08 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0011_auto_20201126_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nagoodslending',
            name='lastinfo',
            field=models.CharField(blank=True, db_column='lastinfo', max_length=150, null=True),
        ),
    ]