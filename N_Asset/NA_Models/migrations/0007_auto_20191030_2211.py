# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-10-30 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0006_auto_20191014_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='nagareturn',
            name='isaccepted',
            field=models.PositiveSmallIntegerField(db_column='IsAccepted', default=0),
        ),
        migrations.AddField(
            model_name='nagoodslost',
            name='fk_goods_return',
            field=models.ForeignKey(blank=True, db_column='FK_Return', db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_goods_lost', to='NA_Models.NAGoodsReturn'),
        ),
        migrations.AddField(
            model_name='nagoodsreturn',
            name='isaccepted',
            field=models.PositiveSmallIntegerField(db_column='IsAccepted', default=0),
        ),
        migrations.AlterField(
            model_name='naprivilege_form',
            name='form_name_ori',
            field=models.CharField(choices=[('employee', 'employee'), ('n_a_supplier', 'n_a_supplier'), ('goods', 'goods'), ('n_a_goods_receive', 'n_a_goods_receive'), ('n_a_goods_outwards', 'n_a_goods_outwards'), ('n_a_goods_lending', 'n_a_goods_lending'), ('n_a_goods_return', 'n_a_goods_return'), ('n_a_maintenance', 'n_a_maintenance'), ('n_a_disposal', 'n_a_disposal'), ('n_a_goods_lost', 'n_a_disposal'), ('n_a_ga_receive', 'n_a_ga_receive_form'), ('n_a_ga_outwards', 'n_a_ga_outwards'), ('n_a_ga_maintenance', 'n_a_ga_maintenance'), ('n_a_goods_history', 'n_a_goods_history'), ('n_a_acc_fa', 'n_a_acc_fa'), ('n_a_privilege', 'n_a_privilege')], db_column='Form_name_ori', max_length=50),
        ),
        migrations.AlterModelTable(
            name='naprivilege_form',
            table='N_A_Privilege_Form',
        ),
    ]
