# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-07 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nagavnhistory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
