# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-09-11 12:19
from __future__ import unicode_literals

import NA_DataLayer.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0002_nagavnhistory_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logevent',
            name='descriptions',
            field=NA_DataLayer.fields.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='naprivilege_form',
            name='form_name_ori',
            field=models.CharField(choices=[('employee', 'employee'), ('n_a_supplier', 'n_a_supplier'), ('goods', 'goods'), ('n_a_privilege', 'n_a_privilege'), ('n_a_acc_fa', 'n_a_acc_fa'), ('n_a_goods_receive', 'n_a_goods_receive'), ('n_a_goods_outwards', 'n_a_goods_outwards'), ('n_a_ga_receive', 'n_a_ga_receive_form'), ('n_a_ga_outwards', 'n_a_ga_outwards')], db_column='Form_name_ori', max_length=50),
        ),
    ]
