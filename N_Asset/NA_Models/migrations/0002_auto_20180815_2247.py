# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-08-15 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('NA_Models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NAGAMaintenance',
            fields=[
                ('idapp', models.AutoField(db_column='IDApp', primary_key=True, serialize=False)),
                ('createddate', models.DateTimeField(db_column='CreatedDate', default=django.utils.timezone.now)),
                ('createdby', models.CharField(db_column='CreatedBy', max_length=100)),
                ('modifieddate', models.DateTimeField(blank=True, db_column='ModifiedDate', null=True)),
                ('modifiedby', models.CharField(blank=True, db_column='ModifiedBy', max_length=100, null=True)),
                ('serialnumber', models.CharField(db_column='SerialNumber', default='N/A', max_length=100)),
                ('requestdate', models.DateField(blank=True, db_column='RequestDate', null=True)),
                ('startdate', models.DateField(db_column='StartDate')),
                ('isstillguarantee', models.BooleanField(db_column='IsStillGuarantee')),
                ('expense', models.DecimalField(db_column='Expense', decimal_places=4, max_digits=10)),
                ('maintenanceby', models.CharField(db_column='MaintenanceBy', max_length=100)),
                ('personalname', models.CharField(blank=True, db_column='PersonalName', max_length=100, null=True)),
                ('enddate', models.DateField(blank=True, db_column='EndDate', null=True)),
                ('typeapp', models.CharField(db_column='TypeApp', max_length=32)),
                ('issucced', models.IntegerField(blank=True, db_column='IsSucced', default=True, null=True)),
                ('isfinished', models.BooleanField(db_column='IsFinished', default=True)),
                ('descriptions', models.CharField(blank=True, db_column='Descriptions', max_length=250, null=True)),
                ('fk_goods', models.ForeignKey(db_column='FK_Goods', db_constraint=False, max_length=30, on_delete=django.db.models.deletion.DO_NOTHING, to='NA_Models.goods')),
            ],
            options={
                'db_table': 'n_a_ga_maintenance',
                'managed': True,
            },
        ),
        #migrations.RemoveField(
        #    model_name='nastock',
        #    name='isbroken',
        #),
        #migrations.AddField(
        #    model_name='nadisposal',
        #    name='fk_lost',
        #    field=models.ForeignKey(blank=True, db_column='FK_Lost', null=True, on_delete=django.db.models.deletion.CASCADE, to='NA_Models.NAGoodsLost'),
        #),
        migrations.AddField(
            model_name='nadisposal',
            name='fk_sold_to_employee',
            field=models.ForeignKey(blank=True, db_column='FK_Sold_To_Employee', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_disposal_emp_Sold', to='NA_Models.Employee'),
        ),
        migrations.AddField(
            model_name='nadisposal',
            name='sold_to',
            field=models.CharField(blank=True, db_column='Sold_To', max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='nadisposal',
            name='sold_to_p_other',
            field=models.CharField(blank=True, db_column='Sold_To_P_Other', max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='nastock',
            name='tdisposal',
            field=models.IntegerField(db_column='TDisposal', null=True),
        ),
        migrations.AddField(
            model_name='nastock',
            name='tisbroken',
            field=models.IntegerField(db_column='TIsBroken', null=True),
        ),
        migrations.AddField(
            model_name='nastock',
            name='tislost',
            field=models.IntegerField(db_column='TIsLost', null=True),
        ),
        migrations.AlterField(
            model_name='nadisposal',
            name='sellingprice',
            field=models.DecimalField(blank=True, db_column='SellingPrice', decimal_places=4, max_digits=30, null=True),
        ),
        migrations.AlterField(
            model_name='nastock',
            name='tisnew',
            field=models.PositiveSmallIntegerField(db_column='TIsNew', null=True),
        ),
        migrations.AlterField(
            model_name='nastock',
            name='tisrenew',
            field=models.PositiveSmallIntegerField(db_column='TIsRenew', null=True),
        ),
        migrations.RemoveField(
            model_name='nastock',
            name='isbroken',
        ),
        migrations.AlterField(
            model_name='nagamaintenance',
            name='fk_goods',
            field=models.ForeignKey(db_column='FK_Goods', db_constraint=False, max_length=30, on_delete=django.db.models.deletion.DO_NOTHING, to='NA_Models.goods'),
        ),
    ]
