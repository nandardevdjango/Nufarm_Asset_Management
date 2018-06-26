# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-27 00:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='goods',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='logevent',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='na_goodsreceive_detail',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='naaccfa',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nadisposal',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodshistory',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodslending',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodslost',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodsoutwards',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodsreceive',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodsreceive_other',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nagoodsreturn',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='namaintenance',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nastock',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nasuplier',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nasyspriviledge',
            name='createddate',
            field=models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now),
        ),
    ]
