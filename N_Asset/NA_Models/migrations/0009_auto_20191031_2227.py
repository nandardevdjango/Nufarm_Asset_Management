# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-31 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0008_auto_20191030_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nagoodslost',
            name='fk_goods_return',
            field=models.ForeignKey(blank=True, db_column='FK_Goods_Return', db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_goods_lost', to='NA_Models.NAGoodsReturn'),
        ),
    ]
