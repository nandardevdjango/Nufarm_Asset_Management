﻿import re
from datetime import date, datetime, timedelta
from os import path

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldError, MultipleObjectsReturned
from django.db import models
from django.utils import timezone
from django.utils.encoding import force_text
from NA_DataLayer.fields import JSONField
from NA_DataLayer.MasterData.NA_Employee import NA_BR_Employee
from NA_DataLayer.MasterData.NA_Goods_BR import NA_BR_Goods, CustomManager
from NA_DataLayer.MasterData.NA_Privilege_BR import NA_BR_Privilege
from NA_DataLayer.MasterData.NA_Supplier import NA_BR_Supplier
from NA_DataLayer.MasterData.NA_Sys_Privilege_BR import NA_BR_Sys_Privilege
from NA_DataLayer.OtherPages.NA_Acc_FA import NA_Acc_FA_BR
from NA_DataLayer.OtherPages.NA_Maintenance_BR import NA_BR_Maintenance
from NA_DataLayer.Transactions.NA_Ga_History_BR import NAGaVnHistoryBR
from NA_DataLayer.Transactions.NA_GoodsLost_BR import NA_BR_GoodsLost
from NA_DataLayer.Transactions.NA_Goods_Disposal_BR import NA_BR_Goods_Disposal
from NA_DataLayer.Transactions.NA_Goods_Lending_BR import NA_BR_Goods_Lending
from NA_DataLayer.Transactions.NA_Goods_Maintenance_GA_BR import NA_BR_GA_Maintenance
from NA_DataLayer.Transactions.NA_Goods_Outwards_BR import NA_BR_Goods_Outwards
from NA_DataLayer.Transactions.NA_Goods_Outwards_GA_BR import NABRGoodsOutwardsGA
from NA_DataLayer.Transactions.NA_Goods_Receive_BR import (NA_BR_Goods_Receive,
                                                           CustomSupplierManager,
                                                           custEmpManager)
from NA_DataLayer.Transactions.NA_Goods_Receive_Detail_BR import NA_BR_Goods_Receive_Detail
from NA_DataLayer.Transactions.NA_Goods_Receive_GA_BR import NA_BR_Goods_Receive_GA
from NA_DataLayer.Transactions.NA_Goods_Receive_Other_BR import NA_BR_Goods_Receive_other
from NA_DataLayer.Transactions.NA_Goods_Return_BR import NA_BR_Goods_Return
from NA_DataLayer.Transactions.NA_Goods_Return_GA_BR import NA_BR_Goods_Return_GA
#from NA_DataLayer.Transactions.
from NA_DataLayer.file_storage import NAFileStorage


class NA_BaseModel(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    createddate = models.DateTimeField(
        db_column='CreatedDate', default=timezone.now)
    createdby = models.CharField(db_column='CreatedBy', max_length=100)
    modifieddate = models.DateTimeField(
        db_column='ModifiedDate',
        blank=True,
        null=True
    )
    modifiedby = models.CharField(
        db_column='ModifiedBy',
        max_length=100,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class NA_MasterDataModel(NA_BaseModel):
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    inactive = models.BooleanField(db_column='InActive', default=False)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class NA_TransactionModel(NA_BaseModel):
    fk_goods = models.ForeignKey(
        'goods',
        db_column='FK_Goods',
        max_length=30,
        db_constraint=False,
    )
    fk_employee = models.ForeignKey(
        'Employee',
        db_column='FK_Employee',
        db_constraint=False
    )
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    serialnumber = models.CharField(
        db_column='SerialNumber',
        max_length=100,
        default='N/A'
    )

    class Meta:
        abstract = True


class NA_GoodsReceiveModel(NA_BaseModel):
    datereceived = models.DateTimeField(db_column='DateReceived')
    fk_supplier = models.ForeignKey(
        'NASupplier',
        db_column='FK_Supplier',
        db_constraint=False
    )
    totalpurchase = models.SmallIntegerField(db_column='TotalPurchase')
    totalreceived = models.SmallIntegerField(db_column='TotalReceived')
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )
    descbysystem = models.CharField(
        db_column='DescBySystem',
        max_length=2000,
        blank=True,
        null=True
    )
    refno = models.CharField(db_column='REFNO', max_length=100)

    class Meta:
        abstract = True


class NAGoodsOutwardsModel(NA_TransactionModel):
    isnew = models.BooleanField(db_column='IsNew')
    daterequest = models.DateTimeField(db_column='DateRequest')
    datereleased = models.DateTimeField(db_column='DateReleased')
    fk_usedemployee = models.ForeignKey(
        'Employee',
        db_column='FK_UsedEmployee',
        related_name='rel_used_employee_%(class)s',
        null=True,
        db_constraint=False
    )
    fk_frommaintenance = models.ForeignKey(
        'Employee',
        related_name='rel_maintenance_%(class)s',
        db_column='FK_FromMaintenance',
        blank=True,
        null=True,
        db_constraint=False
    )
    fk_responsibleperson = models.ForeignKey(
        'Employee',
        db_column='FK_ResponsiblePerson',
        max_length=50,
        blank=True,
        null=True,
        related_name='rel_resp_person_%(class)s',
        db_constraint=False
    )
    fk_sender = models.ForeignKey(
        'Employee',
        related_name='rel_sender_%(class)s',
        db_column='FK_Sender',
        max_length=50,
        blank=True,
        null=True,
        db_constraint=False
    )
    fk_stock = models.ForeignKey(
        'NAStock',
        related_name='rel_stock_%(class)s',
        db_column='FK_Stock',
        blank=True,
        null=True,
        db_constraint=False
    )
    fk_lending = models.ForeignKey(
        'NAGoodsLending',
        db_column='FK_Lending',
        related_name='rel_lending_%(class)s',
        null=True,
        blank=True,
        db_constraint=False
    )
    fk_return = models.ForeignKey(
        'NAGoodsReturn',
        db_column='FK_Return',
        related_name='rel_return_%(class)s',
        null=True,
        db_constraint=False
    )
    fk_receive = models.ForeignKey(
        'NA_GoodsReceive_detail',
        db_column='FK_Receive',
        related_name='rel_receive_%(class)s',
        null=True,
        db_constraint=False
    )
    lastinfo = models.CharField(
        db_column='lastinfo', max_length=250, blank=True, null=True)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class NAGoodsReturnModel(NA_TransactionModel):
    datereturn = models.DateTimeField(db_column='DateReturn')
    conditions = models.CharField(db_column='Conditions', max_length=1)
    fk_fromemployee = models.ForeignKey(
        'Employee',
        db_column='FK_FromEmployee',
        max_length=50,
        blank=True,
        null=True,
        related_name='fk_ngr_fromemployee_%(class)s',
        db_constraint=False
    )
    fk_usedemployee = models.ForeignKey(
        'Employee',
        db_column='FK_UsedEmployee',
        max_length=50,
        blank=True,
        null=True,
        related_name='fk_ngr_usedemployee_%(class)s',
        db_constraint=False
    )
    isaccepted = models.PositiveSmallIntegerField(db_column='IsAccepted',default=0)
    iscompleted = models.PositiveSmallIntegerField(db_column='IsCompleted')
    minusDesc = models.CharField(
        db_column='MinusDesc',
        max_length=100,
        blank=True,
        null=True
    )
    fk_goods_outwards = models.ForeignKey(
        'NAGoodsOutwards',
        db_column='FK_Goods_Outwards',
        null=True,
        blank=True,
        related_name='fk_outwards_%(class)s',
        db_constraint=False
    )
    fk_goods_lend = models.ForeignKey(
        'NAGoodsLending',
        db_column='FK_Goods_Lend',
        blank=True,
        null=True,
        related_name='fk_lend_%(class)s',
        db_constraint=False
    )
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class LogEvent(NA_BaseModel):
    modifieddate = None
    modifiedby = None

    nameapp = models.CharField(db_column='NameApp', max_length=30)
    model = models.CharField(db_column='Model', max_length=30)
    descriptions = JSONField()

    def __str__(self):
        return '{}'.format(self.nameapp)

    @staticmethod
    def get_log_data(model, action, values=None, pk=None, **kwargs):
        """
        to get log event data, use it to get date informations if data has deleted,
        existed or updated
        param
        action: e.g (deleted,updated)
        action for getting type of log event

        PK: primary key e.g (IDApp,SupplierCode)
        model: can fill with model class or string
        usage :: LogEvent.get_log_data(pk=1, model=Employee, action='Deleted',
        values='createddate')
        """

        filter_kwargs = {
            'nameapp__istartswith': action,
            'model': model
        }

        if not isinstance(model, type):
            try:
                model = ContentType.objects.get(model=model)
            except ContentType.DoesNotExist:
                raise ValueError('cannot get model %s' % model)
            model = model.model_class()

        if pk is None:
            for field in kwargs.keys():
                filter_kwargs.update({
                    'descriptions__%s' % field: kwargs.get(field)
                })
        else:
            pk_field = model._meta.pk.name
            filter_kwargs.update({
                'descriptions__%s' % pk_field: pk
            })
        filter_kwargs['model'] = force_text(
            model._meta.verbose_name).replace(' ', '')

        try:
            log = LogEvent.objects.get(**filter_kwargs)
        except FieldError:
            raise ValueError('Please ensure lookup fields in models')
        except MultipleObjectsReturned:
            log = LogEvent.objects.filter(**filter_kwargs).first()
        except LogEvent.DoesNotExist as e:
            raise e

        if values:
            if isinstance(values, str):
                log = eval('log.%s' % values)
            elif isinstance(values, list):
                log = [eval('log.%s' % i) for i in values]
            else:
                raise TypeError('values must be list or str')
        return log

    class Meta:
        managed = True
        db_table = 'LogEvent'


class Employee(NA_MasterDataModel):
    FORM_NAME = 'Employee'
    FORM_NAME_ORI = 'employee'

    HUMAN_DISPLAY = {
        'nik': 'Nik',
        'employee_name': 'Employee Name',
        'typeapp': 'Employee Type',
        'jobtype': 'Job Type',
        'gender': 'Gender',
        'status': 'Status',
        'telphp': 'Mobile Phone',
        'territory': 'Territory',
        'descriptions': 'Descriptions',
        'createddate': 'Created Date',
        'createdby': 'Created By',
        'modifieddate': 'Modified Date',
        'modifiedby': 'Modified By'
    }

    nik = models.CharField(
        db_column='NIK', max_length=50, unique=True
    )
    employee_name = models.CharField(
        db_column='Employee_Name', max_length=150, blank=True, null=True)
    typeapp = models.CharField(db_column='TypeApp', max_length=32, choices=(
        ('P', 'Permanent'),
        ('C', 'Casual'),
        ('K', 'Kontrak')
    ))
    jobtype = models.CharField(
        db_column='JobType',
        max_length=150,
        blank=True,
        null=True
    )
    gender = models.CharField(db_column='Gender', max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
        # this is for crazy human, like a programmer their have other gender
        ('O', 'Other')
    ))
    status = models.CharField(db_column='Status', max_length=1, choices=(
        ('S', 'Single'),
        ('M', 'Married')
    ))
    telphp = models.CharField(
        db_column='TelpHP',
        max_length=20,
        blank=True,
        null=True,
        unique=False
    )
    territory = models.CharField(
        db_column='Territory', max_length=50, blank=True, null=True)

    objects = NA_BR_Employee()
    customManager = custEmpManager()

    class Meta:
        managed = True
        db_table = 'employee'

    def __str__(self):
        return self.employee_name


class NASupplier(NA_MasterDataModel):
    FORM_NAME = 'Supplier'
    FORM_NAME_ORI = 'n_a_supplier'

    HUMAN_DISPLAY = {
        'suppliercode': 'Supplier Code',
        'suppliername': 'Supplier Name',
        'telp': 'Telp',
        'hp': 'Mobile Phone',
        'address': 'Address',
        'contactperson': 'Contact Person',
        'createddate': 'Created Date',
        'createdby': 'Created By',
        'modifieddate': 'Modified Date',
        'modifiedby': 'Modified By'
    }

    idapp = None
    typeapp = None
    descriptions = None

    suppliercode = models.CharField(
        db_column='SupplierCode',
        primary_key=True,
        max_length=30,
        unique=True
    )
    suppliername = models.CharField(
        db_column='SupplierName', max_length=100, blank=True, null=True)
    address = models.CharField(
        db_column='Address', max_length=150, blank=True, null=True)
    telp = models.CharField(
        db_column='Telp',
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    hp = models.CharField(
        db_column='HP',
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    contactperson = models.CharField(
        db_column='ContactPerson', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.suppliername

    objects = NA_BR_Supplier()
    customManager = CustomSupplierManager()

    class Meta:
        managed = True
        db_table = 'n_a_supplier'


class NAAccFa(NA_BaseModel):
    modifieddate = None
    modifiedby = None
    fk_goods = models.ForeignKey(
        'goods',
        db_column='FK_Goods',
        related_name='AccFA_goods',
        db_constraint=False
    )
    serialnumber = models.CharField(db_column='SerialNumber', max_length=50)
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    year = models.DecimalField(
        db_column='Year', max_digits=10, decimal_places=2)
    startdate = models.DateField(db_column='StartDate')
    date_depreciation = models.DateField(
        db_column='DateDepreciation', null=True)
    depr_expense = models.DecimalField(
        db_column='Depr_Expense',
        max_digits=30,
        decimal_places=4,
        blank=True,
        null=True
    )
    depr_accumulation = models.DecimalField(
        db_column='Depr_Accumulation',
        max_digits=30,
        decimal_places=4,
        blank=True,
        null=True
    )
    bookvalue = models.DecimalField(
        db_column='BookValue',
        max_digits=30,
        decimal_places=4,
        blank=True,
        null=True
    )
    is_parent = models.PositiveSmallIntegerField(
        db_column='IsParent', default=0)
    lastupdated = models.DateTimeField(
        db_column='LastUpdated', blank=True, null=True)
    objects = NA_Acc_FA_BR()

    class Meta:
        managed = True
        db_table = 'n_a_acc_fa'

    def __str__(self):
        return self.fk_goods.goodsname


class NAAppparams(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    codeapp = models.CharField(db_column='CodeApp', max_length=64)
    nameapp = models.CharField(
        db_column='NameApp', max_length=100, blank=True, null=True)
    typeapp = models.CharField(
        db_column='TypeApp', max_length=64, blank=True, null=True)
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)
    valuechar = models.CharField(
        db_column='ValueChar', max_length=50, blank=True, null=True)
    fkidapp = models.SmallIntegerField(
        db_column='FKIDApp', blank=True, null=True)
    fkcodeapp = models.CharField(
        db_column='FKCodeApp', max_length=64, blank=True, null=True)
    attstrparams = models.CharField(
        db_column='AttStrParams', max_length=20, blank=True, null=True)
    attdecparams = models.DecimalField(
        db_column='AttDecParams', max_digits=10, decimal_places=3, blank=True, null=True)
    valuestrparams = models.CharField(
        db_column='ValueStrParams', max_length=50, blank=True, null=True)
    valuedecparams = models.DecimalField(
        db_column='ValueDecParams', max_digits=10, decimal_places=3, blank=True, null=True)
    inactive = models.IntegerField(db_column='InActive')
    createddate = models.DateTimeField(
        db_column='CreatedDate', blank=True, null=True)
    createdby = models.CharField(
        db_column='CreatedBy', max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'n_a_appparams'
        unique_together = (('idapp', 'codeapp'),)

class NAGoodsDeletion(NA_BaseModel):
    fk_goods = models.ForeignKey(
        'goods',
        db_column='FK_Goods',
        max_length=30,
        db_constraint=False,
    )
    x_employee = models.ForeignKey(
        'Employee',
        db_column='FK_Employee',
        db_constraint=False
    )
    serialnumber = models.CharField(
        db_column='SerialNumber',
        max_length=100,
        default='N/A'
    )
    bookvalue = models.DecimalField(
    db_column='bookvalue', max_digits=30, decimal_places=4
    )
    submission_date = models.DateField(db_column='submission_date',auto_now_add=True)
    submission_value = models.DecimalField (db_column='submission_value', max_digits=30, decimal_places=4)
    is_value_to_all = models.BooleanField(db_column='is_value_to_all')
    approval_value = models.DecimalField(
        db_column='approval_value', max_digits=30, decimal_places=4)
    #approved_date
    submission_by = models.ForeignKey(
        Employee,
        db_column='fk_submission_by',
        max_length=100,
        related_name='submission_by_employee',
        db_constraint=False)
    approved_by =  models.ForeignKey(
		Employee,
		db_column='fk_approvedby',
		max_length=100,
		related_name='approved_by_employee',
		db_constraint=False)
    acknowledged_by1 =models.ForeignKey(
        Employee,
        db_column='acknowledged_by1',
        max_length=100,
        related_name='acknowledged_by_employee1',
        db_constraint=False)
    acknowledged_by2 =models.ForeignKey(
        Employee,
        db_column='acknowledged_by2',
        max_length=100,
        related_name='acknowledged_by_employee2',
        db_constraint=False)

    class Meta:
        db_table = 'n_a_goods_deletion'
        managed = True

class goods(NA_MasterDataModel):
    itemcode = models.CharField(db_column='ItemCode', max_length=30)
    goodsname = models.CharField(db_column='GoodsName', max_length=150)
    brandname = models.CharField(
        db_column='BrandName', max_length=100, blank=True, null=True)
    priceperunit = models.DecimalField(
        db_column='PricePerUnit', max_digits=30, decimal_places=4)
    depreciationmethod = models.CharField(
        db_column='DepreciationMethod', max_length=3)
    unit = models.CharField(db_column='Unit', max_length=30)
    economiclife = models.DecimalField(
        db_column='EconomicLife', max_digits=10, decimal_places=2)
    placement = models.CharField(
        db_column='Placement', max_length=50, blank=True, null=True)
    typeapp = models.CharField(
        max_length=32,
        db_column='typeapp', null=True, choices=(
            ('IT', 'IT'),
            ('GA', 'GA'),
            ('IT Accessories', 'IT Accessories'),
            ('GA Accesories', 'GA Accesories'),
            ('Others', 'Others')
        )
    )

    class Meta:
        db_table = 'n_a_goods'
        managed = True
    objects = NA_BR_Goods()
    customs = CustomManager()
    #objectT = objects()
    def __str__(self):
        return self.goodsname

class NAGoodsReceive(NA_GoodsReceiveModel):
	idapp_fk_goods = models.ForeignKey(
		goods, db_column='fk_goods', db_constraint=False)
	idapp_fk_receivedby = models.ForeignKey(
		Employee,
		db_column='FK_ReceivedBy',
		max_length=50,
		related_name='fk_receivedBy',
		db_constraint=False
	)
	idapp_fk_p_r_by = models.ForeignKey(
		Employee,
		db_column='FK_P_R_By',
		max_length=50,
		blank=True,
		null=True,
		related_name='fk_p_r_by',
		db_constraint=False
	)
	#equipment_desc = models.CharField(db_column='Equipment_Desc',max_length=400,blank=True,null=True)
	class Meta:
		managed = True
		db_table = 'n_a_goods_receive'
	objects = NA_BR_Goods_Receive()

class NA_GoodsReceive_detail(NA_BaseModel):
	fk_app = models.ForeignKey(
		NAGoodsReceive, db_column='FK_App', db_constraint=False)
	brandname = models.CharField(max_length=100, db_column='BrandName')
	priceperunit = models.DecimalField(
		db_column='PricePerUnit', max_digits=30, decimal_places=4)
	typeapp = models.CharField(db_column='TypeApp', max_length=32)
	warranty = models.DecimalField(
		max_digits=6, decimal_places=2, db_column='Warranty')
	endofwarranty = models.DateTimeField(
		null=True, blank=True, db_column='EndOfWarranty')
	serialnumber = models.CharField(db_column='SerialNumber', max_length=100)

	class Meta:
		db_table = 'n_a_goods_receive_detail'
		managed = True
	objects = NA_BR_Goods_Receive_Detail()

class NAGoodsReturn(NAGoodsReturnModel):
    fk_employee = None
    objects = NA_BR_Goods_Return()

    class Meta:
        managed = True
        db_table = 'n_a_goods_return'

    def __str__(self):
        return self.fk_goods.goodsname


class NAGAMaintenance(NA_TransactionModel):
    fk_employee = None

    requestdate = models.DateField(
        db_column='RequestDate',
        blank=True,
        null=True
    )
    startdate = models.DateField(db_column='StartDate')
    isstillguarantee = models.BooleanField(db_column='IsStillGuarantee')
    expense = models.DecimalField(
        db_column='Expense',
        max_digits=14,
        decimal_places=4
    )
    maintenanceby = models.CharField(
        db_column='MaintenanceBy',
        max_length=100
    )
    personalname = models.CharField(
        db_column='PersonalName',
        max_length=100,
        blank=True,
        null=True
    )
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    issucced = models.IntegerField(
        db_column='IsSucced', blank=True, null=True, default=True)
    isfinished = models.BooleanField(db_column='IsFinished', default=True)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )

    objects = NA_BR_GA_Maintenance()

    class Meta:
        managed = True
        db_table = 'n_a_ga_maintenance'


class NAMaintenance(NA_TransactionModel):
    fk_employee = None

    requestdate = models.DateField(
        db_column='RequestDate',
        blank=True,
        null=True
    )
    startdate = models.DateField(db_column='StartDate')
    isstillguarantee = models.TextField(db_column='IsStillGuarantee')
    expense = models.DecimalField(
        db_column='Expense',
        max_digits=14,
        decimal_places=4
    )
    maintenanceby = models.CharField(
        db_column='MaintenanceBy',
        max_length=100
    )
    personalname = models.CharField(
        db_column='PersonalName',
        max_length=100,
        blank=True,
        null=True
    )
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    issucced = models.IntegerField(db_column='IsSucced', blank=True, null=True)
    isfinished = models.BooleanField(db_column='IsFinished', default=False)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )

    objects = NA_BR_Maintenance()

    class Meta:
        managed = True
        db_table = 'n_a_maintenance'


class NAStock(NA_BaseModel):
    fk_goods = models.ForeignKey(
        goods, db_column='FK_Goods', db_constraint=False)
    t_goods_spare = models.PositiveSmallIntegerField(
        db_column='T_Goods_Spare', null=True)
    totalqty = models.IntegerField(db_column='TotalQty', null=True)
    tisused = models.IntegerField(db_column='TIsUsed', null=True)
    tisnew = models.PositiveSmallIntegerField(db_column='TIsNew', null=True)
    tisrenew = models.PositiveSmallIntegerField(
        db_column='TIsRenew', null=True)
    tisbroken = models.IntegerField(db_column='TIsBroken', null=True)
    tgoods_return = models.SmallIntegerField(
        db_column='TGoods_Return', blank=True, null=True)
    tgoods_received = models.IntegerField(
        db_column='TGoods_Received', blank=True, null=True)
    tmaintenance = models.SmallIntegerField(
        db_column='TMaintenance', blank=True, null=True)
    tdisposal = models.IntegerField(db_column='TDisposal', null=True)
    tislost = models.IntegerField(db_column='TIsLost', null=True)

    class Meta:
        managed = True
        db_table = 'n_a_stock'


class NAGoodsLending(NA_TransactionModel):
    isnew = models.IntegerField(db_column='IsNew')
    datelending = models.DateField(
        db_column='DateLending', blank=True, null=True)
    datereturn = models.DateTimeField(db_column='DateReturn', null=True)
    fk_stock = models.ForeignKey(
        NAStock,
        db_column='FK_Stock',
        related_name='fk_gl_stock',
        db_constraint=False
    )
    fk_responsibleperson = models.ForeignKey(
        Employee,
        db_column='FK_ResponsiblePerson',
        blank=True,
        null=True,
        related_name='fk_gl_employee_resp_person',
        db_constraint=False
    )
    interests = models.CharField(
        db_column='interests', max_length=150, blank=True, null=True)
    fk_sender = models.ForeignKey(
        Employee,
        db_column='FK_Sender',
        blank=True,
        null=True,
        related_name='fk_gl_employee_sender',
        db_constraint=False
    )
    statuslent = models.CharField(
        db_column='Status', max_length=10, default = 'L')
    fk_maintenance = models.ForeignKey(
        NAMaintenance,
        db_column="FK_Maintenance",
        blank=True,
        null=True,
        related_name='fk_gl_maintenance',
        db_constraint=False
    )
    fk_return = models.ForeignKey(
        NAGoodsReturn,
        db_column='FK_RETURN',
        blank=True,
        null=True,
        related_name='fk_gl_goods_return',
        db_constraint=False
    )
    fk_receive = models.ForeignKey(
        NAGoodsReceive,
        db_column='FK_Receive',
        blank=True,
        null=True,
        related_name='fk_gl_goods_receive',
        db_constraint=False
    )
    fk_currentapp = models.ForeignKey(
        'self',
        db_column='FK_CurrentApp',
        blank=True,
        null=True,
        related_name='fk_gl_parent',
        db_constraint=False
    )
    lastinfo = models.CharField(
        db_column='lastinfo', max_length=250, blank=True, null=True)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        managed = True
        db_table = 'n_a_goods_lending'
    objects = NA_BR_Goods_Lending()


class NAGoodsOutwards(NAGoodsOutwardsModel):
	equipment_desc = models.CharField(
		db_column='Equipment_Desc',
		max_length=400,
		blank=True,
		null=True
	)
	class Meta:
		managed = True
		db_table = 'n_a_goods_outwards'
	objects = NA_BR_Goods_Outwards()

class NAGoodsLost(NA_TransactionModel):
    fk_employee = None
    datelost = models.DateTimeField(db_column='DateLost', default=timezone.now)
    fk_goods_outwards = models.ForeignKey(
        NAGoodsOutwards,
        db_column='FK_Goods_Outwards',
        null=True,
        blank=True,
        db_constraint=False
    )
    fk_goods_lending = models.ForeignKey(
        NAGoodsLending,
        db_column='FK_Goods_Lending',
        null=True,
        blank=True,
        db_constraint=False
    )
    fk_maintenance = models.ForeignKey(
        NAMaintenance,
        db_column='FK_Maintenance',
        null=True,
        blank=True,
        db_constraint=False
    )

    fromgoods = models.CharField(db_column='FromGoods', max_length=10)
    fk_lostby = models.ForeignKey(
        Employee,
        db_column='FK_LostBy',
        related_name='lost_by',
        null=True,
        blank=True,
        db_constraint=False
    )
    fk_usedby = models.ForeignKey(
        Employee,
        db_column='FK_UsedBy',
        null=True,
        blank=True,
        related_name='used_by',
        db_constraint=False
    )
    fk_responsibleperson = models.ForeignKey(
        Employee,
        db_column='FK_ResponsiblePerson',
        blank=True,
        null=True,
        related_name='resp_person_goods_lost',
        db_constraint=False
    )
    fk_goods_return = models.ForeignKey(
        NAGoodsReturn,
        db_column='FK_Goods_Return',
        blank=True,
        null=True,
        related_name='return_goods_lost',
        db_constraint=False
    )
    status = models.CharField(db_column='Status', max_length=5)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )
    reason = models.CharField(
        db_column='Reason',
        max_length=250,
        blank=True,
        null=True
    )

    objects = NA_BR_GoodsLost()

    class Meta:
        managed = True
        db_table = 'n_a_goods_lost'


class NADisposal(NA_TransactionModel):
    fk_employee = None

    datedisposal = models.DateField(db_column='DateDisposal')
    islost = models.PositiveSmallIntegerField(db_column='IsLost', default=0)
    fk_lost = models.ForeignKey(
        'NAGoodsLost', db_column='FK_Lost', blank=True, null=True)
    issold = models.PositiveSmallIntegerField(
        db_column='IsSold', blank=True, null=True)
    sellingprice = models.DecimalField(
        db_column='SellingPrice',
        max_digits=30,
        decimal_places=4,
        blank=True,
        null=True
    )
    sold_to = models.CharField(
        db_column='Sold_To', blank=True, null=True, max_length=1)
    fk_sold_to_employee = models.ForeignKey(
        'Employee',
        db_column='FK_Sold_To_Employee',
        related_name='fk_disposal_emp_Sold',
        db_constraint=False, blank=True, null=True,
    )
    sold_to_p_other = models.CharField(
        max_length=120,
        db_column='Sold_To_P_Other',
        blank=True,
        null=True
    )
    bookvalue = models.DecimalField(
        db_column='BookValue', max_digits=10, decimal_places=4)
    descriptions = models.CharField(
        db_column='Descriptions',
        max_length=250,
        blank=True,
        null=True
    )
    fk_proposedby = models.ForeignKey(
        'Employee',
        db_column='FK_ProposedBy',
        related_name='fk_disposal_emp_proposed',
        max_length=50,
        blank=True,
        null=True,
        db_constraint=False
    )

    fk_acknowledge1 = models.ForeignKey(
        'Employee',
        db_column='FK_Acknowledge1',
        related_name='fk_disposal_emp_ack1',
        db_constraint=False, blank=True, null=True,
    )
    fk_acknowledge2 = models.ForeignKey(
        'Employee',
        db_column='FK_Acknowledge2',
        related_name='fk_disposal_emp_ack2',
        db_constraint=False, blank=True, null=True,
    )
    fk_approvedby = models.ForeignKey(
        'Employee',
        db_column='FK_ApprovedBy',
        related_name='fk_disposal_emp_app',
        db_constraint=False, blank=True, null=True,
    )
    fk_acc_fa = models.ForeignKey(
        'NAAccFa',
        related_name='fk_disposal_accfa',
        db_column='FK_Acc_FA',
        blank=True,
        null=True,
        db_constraint=False
    )
    fk_stock = models.ForeignKey(
        'NAStock',
        related_name='fk_disposal_stock',
        db_column='FK_Stock',
        blank=True,
        null=True,
        db_constraint=False
    )
    fk_maintenance = models.ForeignKey(
        'NAMaintenance',
        null=True,
        blank=True,
        db_column='FK_Maintenance',
        db_constraint=False,
        related_name='fk_disposal_maintenance'
    )
    fk_outwards = models.ForeignKey(
        'NAGoodsOutwards',
        db_column='FK_Outwards',
        null=True,
        blank=True,
        db_constraint=False,
        related_name='fk_disposal_outwards'
    )
    fk_lending = models.ForeignKey(
        'NAGoodsLending',
        db_column='FK_Lending',
        null=True,
        blank=True,
        db_constraint=False,
        related_name='fk_disposal_lending'
    )
    fk_return = models.ForeignKey('NAGoodsReturn',
                                  db_column='FK_Return',
                                  null=True,
                                  blank=True,
                                  db_constraint=False,
                                  related_name='fk_disposal_return'
                                  )
    fk_usedemployee = models.ForeignKey(
        'Employee',
        db_column='FK_UsedEmployee',
        null=True,
        blank=True,
        db_constraint=False,
        related_name='fk_disposal_emp_used'
    )

    objects = NA_BR_Goods_Disposal()

    class Meta:
        managed = True
        db_table = 'n_a_disposal'


def upload_to_each_dir(instance, filename):
    return instance.get_dir_image(filename)


class NAPrivilege(AbstractUser, NA_BaseModel):
    FORM_NAME = 'User Privilege'
    FORM_NAME_ORI = 'n_a_privilege'

    HUMAN_DISPLAY = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'username': 'User Name',
        'email': 'Email',
        'divisi': 'Divisi',
        'role': 'Role',
        'picture': 'Picture',
        'date_joined': 'Date Joined',
        'createdby': 'Created By'
    }

    IT = 'IT'
    GA = 'GA'

    DIVISI_CHOICES = (
        (IT, 'IT'),
        (GA, 'GA')
    )

    SUPER_USER = 1
    USER = 2
    GUEST = 3

    ROLE_CHOICES = (
        (GUEST, 'Guest'),
        (USER, 'User'),
        (SUPER_USER, 'Super User')
    )

    createddate = None

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(
        max_length=250, unique=True, blank=False, db_column='UserName')
    email = models.EmailField(unique=True, blank=True, db_column='Email')
    divisi = models.CharField(
        max_length=5, db_column='Divisi', choices=DIVISI_CHOICES)
    password = models.CharField(max_length=128, db_column='Password')
    picture = models.ImageField(
        null=True,
        blank=True,
        default='default.png',
        db_column='Picture',
        upload_to=upload_to_each_dir,
        storage=NAFileStorage()
    )
    last_login = models.DateTimeField(db_column='Last_login', null=True)
    last_form = models.CharField(
        max_length=50,
        db_column='Last_form',
        null=True
    )
    computer_name = models.CharField(max_length=50, db_column='Computer_Name')
    ip_address = models.CharField(max_length=20, db_column='IP_Address')

    role = models.IntegerField(
        choices=ROLE_CHOICES,
        default=GUEST,
        db_column='Role',
        null=True
    )
    is_superuser = models.BooleanField(default=False, db_column='Is_SuperUser')
    is_staff = models.BooleanField(default=False, db_column='Is_Staff')
    is_active = models.BooleanField(default=True, db_column='Is_Active')
    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = ['username']  # required when user is created
    date_joined = models.DateTimeField(
        db_column='Date_Joined', blank=True, null=True)

    objects = NA_BR_Privilege()

    def __str__(self):
        return self.username

    @classmethod
    def get_ga_super_user(cls):
        ga_user = cls.objects.filter(
            divisi=cls.GA,
            is_active=True,
            role=cls.SUPER_USER
        )
        return ga_user

    def get_dir_image(self, filename):
        return path.join(
            'dir_for_{username}'.format(
                username=self.username
            ),
            filename
        )

    def get_picture_name(self):
        pict_name = self.picture.name
        if '\\' in list(pict_name):
            dir_user, filename = pict_name.split('\\')
            pict_name = dir_user + '/' + filename
        return pict_name

    def has_permission(self, action, form_name_ori):
        """
        this function for check if user has permission
        param
        :action: ==> e.g (Allow View,Allow Edit .. etc) use attribute NASysPrivilege.Allow_View .. etc
        :form_name_ori: this is form name ori e.g (n_a_supplier) use attribute NAPrivilege_Form.Supplier_form .. etc

        usage : must be instance of model
        rimba = NAPrivilege.objects.get(username='rimba47prayoga') or from request : request.user.has_permission
        rimba.has_permission(NASysPrivilege.Allow_Add,NAPrivilege_Form.Supplier_form)

        return boolean
        """
        if action not in NASysPrivilege.ALL_PERMISSION:
            raise ValueError('uncategorize, cannot resolve action %s' % action)

        if form_name_ori not in NAPrivilege_Form.ALL_FORM:
            raise ValueError(
                'uncategorize, cannot resolve form %s' % form_name_ori)

        is_has = self.nasysprivilege_set.filter(
            fk_p_form__form_name_ori=form_name_ori,
            permission=action,
            inactive=False
        ).exists()
        return is_has

    def is_have_permission(self, form=None):
        if form:
            return self.nasysprivilege_set.filter(
                fk_p_form__form_name_ori=form
            ).exists()
        return self.nasysprivilege_set.exists()

    def get_all_permission(self, form=None):
        permissions = self.nasysprivilege_set.values(
            'fk_p_form__form_name_ori',
            'permission'
        )
        if form:
            permissions = permissions.filter(
                fk_p_form__form_name_ori=form
            )
        permissions = permissions.iterator()
        data = []
        for permission in permissions:
            data.append({
                'form': permission['fk_p_form__form_name_ori'],
                'permission': permission['permission']
            })
        return data

    def get_permission(self, form):
        if form not in NAPrivilege_Form.ALL_FORM:
            raise ValueError('cannot find %s form' % form)
        return self.get_all_permission(form)

    # ============ Permission for Employee form =============
    @property
    def allow_view_employee(self):
        return self.has_permission(
            NASysPrivilege.Allow_View,
            NAPrivilege_Form.Employee_Form
        )

    @property
    def allow_add_employee(self):
        return self.has_permission(
            NASysPrivilege.Allow_Add,
            NAPrivilege_Form.Employee_Form
        )

    @property
    def allow_edit_employee(self):
        return self.has_permission(
            NASysPrivilege.Allow_Edit,
            NAPrivilege_Form.Employee_Form
        )

    @property
    def allow_delete_employee(self):
        return self.has_permission(
            NASysPrivilege.Allow_Delete,
            NAPrivilege_Form.Employee_Form
        )

    # ============ Permission for Supplier form =============
    @property
    def allow_view_supplier(self):
        return self.has_permission(
            NASysPrivilege.Allow_View,
            NAPrivilege_Form.Supplier_Form
        )

    @property
    def allow_add_supplier(self):
        return self.has_permission(
            NASysPrivilege.Allow_Add,
            NAPrivilege_Form.Supplier_Form
        )

    @property
    def allow_edit_supplier(self):
        return self.has_permission(
            NASysPrivilege.Allow_Edit,
            NAPrivilege_Form.Supplier_Form
        )

    @property
    def allow_delete_supplier(self):
        return self.has_permission(
            NASysPrivilege.Allow_Delete,
            NAPrivilege_Form.Supplier_Form
        )

    # ============ Permission for Goods form =============
    @property
    def allow_view_goods(self):
        return self.has_permission(
            NASysPrivilege.Allow_View,
            NAPrivilege_Form.Goods_Form
        )

    @property
    def allow_add_goods(self):
        return self.has_permission(
            NASysPrivilege.Allow_Add,
            NAPrivilege_Form.Goods_Form
        )

    @property
    def allow_edit_goods(self):
        return self.has_permission(
            NASysPrivilege.Allow_Edit,
            NAPrivilege_Form.Goods_Form
        )

    @property
    def allow_delete_goods(self):
        return self.has_permission(
            NASysPrivilege.Allow_Delete,
            NAPrivilege_Form.Goods_Form
        )

    # ============ Permission for Goods form =============
    @property
    def allow_view_goods_receive(self):
        return self.has_permission(
            NASysPrivilege.Allow_View,
            NAPrivilege_Form.Goods_Receive_Form
        )

    @property
    def allow_add_goods_receive(self):
        return self.has_permission(
            NASysPrivilege.Allow_Add,
            NAPrivilege_Form.Goods_Receive_Form
        )

    @property
    def allow_edit_goods_receive(self):
        return self.has_permission(
            NASysPrivilege.Allow_Edit,
            NAPrivilege_Form.Goods_Receive_Form
        )

    @property
    def allow_delete_goods_receive(self):
        return self.has_permission(
            NASysPrivilege.Allow_Delete,
            NAPrivilege_Form.Goods_Receive_Form
        )

    # ============ Permission for Goods form =============
    @property
    def allow_view_privilege(self):
        return self.has_permission(
            NASysPrivilege.Allow_View,
            NAPrivilege_Form.Privilege_Form
        )

    @property
    def allow_add_privilege(self):
        return self.has_permission(
            NASysPrivilege.Allow_Add,
            NAPrivilege_Form.Privilege_Form
        )

    @property
    def allow_edit_privilege(self):
        return self.has_permission(
            NASysPrivilege.Allow_Edit,
            NAPrivilege_Form.Privilege_Form
        )

    @property
    def allow_delete_privilege(self):
        return self.has_permission(
            NASysPrivilege.Allow_Delete,
            NAPrivilege_Form.Privilege_Form
        )

    class Meta:
        managed = True
        db_table = 'N_A_Privilege'


class NAPrivilege_Form(models.Model):

    Employee_Form = 'employee'
    Supplier_Form = 'n_a_supplier'
    Goods_Form = 'goods'

    Privilege_Form = 'n_a_privilege'

    Goods_Lending_Form = 'n_a_goods_lending'
    Goods_Return_Form = 'n_a_goods_return'
    Goods_Receive_Form = 'n_a_goods_receive'
    Goods_Outwards_Form = 'n_a_goods_outwards'
    Maintenance_Form = 'n_a_maintenance'
    Goods_History_Form = 'n_a_goods_history'

    Disposal_Form = 'n_a_disposal'
    Goods_Lost_Form = 'n_a_goods_lost'
    Fix_asset_Form = 'n_a_acc_fa'

    GA_Maintenance_Form = 'n_a_ga_maintenance'
    GA_Receive_form = 'n_a_ga_receive'
    GA_Outwards_form = 'n_a_ga_outwards'
    GA_Return_Form = 'n_a_ga_return',
    Report_By_Recipient = 'ByRecipient',
    Report_By_RefNumber = 'ByRefNumber',
    Report_by_SerialNumber = 'BySerialNumber'
    MASTER_DATA_FORM = [
        Employee_Form,
        Supplier_Form,
        Goods_Form,
        Privilege_Form
    ]

    TRANSACTION_FORM = [
        Goods_Receive_Form,
        Goods_Outwards_Form,
        Goods_Lending_Form,
        Maintenance_Form,
        Goods_Return_Form,
        Disposal_Form,
        Goods_Lost_Form,
        GA_Maintenance_Form,
        GA_Receive_form,
        GA_Outwards_form
    ]

    OTHER_FORM = [
        Fix_asset_Form,
        Goods_History_Form,

    ]
    REPORT_FORM = [
        Report_By_Recipient,
        Report_By_RefNumber,
        Report_by_SerialNumber
    ]
    ALL_FORM = MASTER_DATA_FORM + TRANSACTION_FORM + OTHER_FORM+REPORT_FORM

    IT_FORM = [
        Goods_Receive_Form,
        Goods_Outwards_Form,
        Fix_asset_Form,
        Goods_History_Form,
        Goods_Lending_Form,
        Maintenance_Form,
        Goods_Return_Form,
        Disposal_Form,
        Goods_Lost_Form,
    ] + MASTER_DATA_FORM

    GA_FORM = [
        GA_Receive_form,
        GA_Outwards_form,
        Fix_asset_Form,
        #satu lagi GA_History
        GA_Maintenance_Form,
        Disposal_Form,
        Goods_Lost_Form,
    ] + MASTER_DATA_FORM

    FORM_NAME_ORI_CHOICES = (
        (Employee_Form, 'employee'),
        (Supplier_Form, 'n_a_supplier'),
        (Goods_Form, 'goods'),

        (Goods_Receive_Form, 'n_a_goods_receive'),
        (Goods_Outwards_Form, 'n_a_goods_outwards'),
        (Goods_Lending_Form, 'n_a_goods_lending'),
        (Goods_Return_Form, 'n_a_goods_return'),
        (Maintenance_Form, 'n_a_maintenance'),
        (Disposal_Form, 'n_a_disposal'),
        (Goods_Lost_Form, 'n_a_goods_lost'),
        #satu lagi asset deletion
        (GA_Receive_form, 'n_a_ga_receive_form'),
        (GA_Outwards_form, 'n_a_ga_outwards'),
        (GA_Maintenance_Form, 'n_a_ga_maintenance'),

        (Goods_History_Form, 'n_a_goods_history'),
        (Fix_asset_Form, 'n_a_acc_fa'),
        (Privilege_Form, 'n_a_privilege'),
        (Report_By_Recipient, 'ByRecipient'),
        (Report_By_RefNumber, 'ByRefNumber'),
        (Report_by_SerialNumber, 'BySerialNumber'),
    )

    idapp = models.AutoField(primary_key=True, db_column='IDApp')
    form_id = models.CharField(max_length=20, db_column='Form_id')
    form_name = models.CharField(max_length=30, db_column='Form_name')
    form_name_ori = models.CharField(
        max_length=50,
        db_column='Form_name_ori',
        choices=FORM_NAME_ORI_CHOICES
    )

    class Meta:
        db_table = 'N_A_Privilege_Form'

    def __str__(self):
        return self.form_name

    @classmethod
    def get_form_it(cls, must_iterate=False):
        fk_form = cls.objects.filter(form_name_ori__in=cls.IT_FORM)
        if must_iterate:
            fk_form = fk_form.iterator()  # technic for loop queryset, improve performance
        return fk_form

    @classmethod
    def get_form_ga(cls, must_iterate):
        fk_form = cls.objects.filter(form_name_ori__in=cls.GA_FORM)
        if must_iterate:
            fk_form = fk_form.iterator()
        return fk_form

    @classmethod
    def get_form_guest(cls, must_iterate=False):
        fk_form = cls.objects.filter(
            form_name_ori__in=['goods', 'n_a_supplier', 'employee'])
        if must_iterate:
            fk_form = fk_form.iterator()  # technic for loop queryset, improve performance
        return fk_form

    @classmethod
    def get_user_form(cls, role, divisi, must_iterate=False):
        """
        return queryset
        """
        if int(role) == NAPrivilege.GUEST:
            return cls.get_form_guest(must_iterate)

        if divisi == NAPrivilege.IT:
            return cls.get_form_it(must_iterate)
        elif divisi == NAPrivilege.GA:
            return cls.get_form_ga(must_iterate)


class NASysPrivilege(NA_BaseModel):

    Allow_View = 'Allow View'
    Allow_Add = 'Allow Add'
    Allow_Edit = 'Allow Edit'
    Allow_Delete = 'Allow Delete'

    ALL_PERMISSION = [
        Allow_View,
        Allow_Add,
        Allow_Edit,
        Allow_Delete
    ]

    PERMISSION_CHOICES = (
        (Allow_View, 'Allow View'),
        (Allow_Add, 'Allow Add'),
        (Allow_Edit, 'Allow Edit'),
        (Allow_Delete, 'Allow Delete')
    )

    fk_p_form = models.ForeignKey(
        NAPrivilege_Form,
        db_column='FK_PForm',
        db_constraint=False
    )
    permission = models.CharField(
        max_length=50,
        db_column='Permission',
        choices=PERMISSION_CHOICES
    )
    user_id = models.ForeignKey(
        NAPrivilege,
        db_column='User_id',
        on_delete=models.CASCADE,
        db_constraint=False
    )
    inactive = models.IntegerField(
        db_column='InActive', null=True, blank=True, default=0)

    objects = NA_BR_Sys_Privilege()

    class Meta:
        db_table = 'N_A_Sys_Privilege'
        unique_together = (('fk_p_form', 'permission', 'user_id'))

    def __str__(self):
        return '{username} : {form_name} - {permission}'.format(
            username=self.user_id.username,
            form_name=self.fk_p_form.form_name,
            permission=self.permission
        )

    @staticmethod
    def default_permission_it(form_name_ori):
        """
        return list of permissions [Allow View, Allow Add, etc.]
        """

        permissions = []
        if form_name_ori in NAPrivilege_Form.IT_FORM:
            permissions.append(NASysPrivilege.Allow_View)
            permissions.append(NASysPrivilege.Allow_Add)
            permissions.append(NASysPrivilege.Allow_Edit)
            permissions.append(NASysPrivilege.Allow_Delete)
            return permissions
        else:
            raise ValueError()

    @staticmethod
    def default_permission_ga(form_name_ori):
        permissions = []
        if form_name_ori in NAPrivilege_Form.GA_FORM:
            permissions.append(NASysPrivilege.Allow_View)
            permissions.append(NASysPrivilege.Allow_Add)
            permissions.append(NASysPrivilege.Allow_Edit)
            permissions.append(NASysPrivilege.Allow_Delete)
            return permissions
        else:
            raise ValueError()

    @staticmethod
    def default_permission_guest(form_name_ori):
        return [NASysPrivilege.Allow_View]

    @classmethod
    def set_data_permission(cls, user, data):
        """
        not return anything, but append dict to paratemer list
        to save memory
        """
        permissions = None
        if int(user.role) == NAPrivilege.GUEST:
            permissions = cls.default_permission_guest
        else:
            if user.divisi == NAPrivilege.IT:
                permissions = cls.default_permission_it
            elif user.divisi == NAPrivilege.GA:
                permissions = cls.default_permission_ga

        fk_forms = NAPrivilege_Form.get_user_form(
            user.role,
            user.divisi,
            must_iterate=True
        )
        if permissions is not None:
            is_have_permission = user.is_have_permission()
            user_permissions = user.get_all_permission()
            for fk_form in fk_forms:  # loop queryset
                form_name_ori = fk_form.form_name_ori
                for permission in permissions(form_name_ori):
                    if int(user.role) != NAPrivilege.SUPER_USER:
                        if form_name_ori == NAPrivilege_Form.Privilege_Form:
                            if permission != NASysPrivilege.Allow_View:
                                continue
                    if is_have_permission:
                        must_continue = False

                        for i in user_permissions:
                            if (i['form'] == form_name_ori and
                                    permission == i['permission']):
                                must_continue = True
                                break
                            else:
                                must_continue = False
                        if must_continue:
                            continue
                    data.append({
                        'fk_p_form': fk_form,  # foreign key in models must be instance
                        'permission': permission,
                        'user_id': user,
                        'createddate': datetime.now(),
                        'createdby': user.createdby
                    })
        else:
            raise ValueError('')

    @classmethod
    def set_permission(cls, user):
        data = []
        cls.set_data_permission(user, data)
        cls.objects.bulk_create([
            cls(**field) for field in data
        ])
        return 'successfully added permission'

    @classmethod
    def set_custom_permission(cls, **kwargs):
        user_id = kwargs['user_id']
        fk_form = kwargs['fk_form']
        permissions = kwargs['permissions']
        createdby = kwargs['createdby']
        user = NAPrivilege.objects.get(idapp=user_id)
        fk_p_form = NAPrivilege_Form.objects.get(idapp=fk_form)
        len_permissions = len(permissions)
        if len_permissions > 1:
            data = []
            for permission in permissions:
                data.append({
                    'fk_p_form': fk_p_form,
                    'permission': permission,
                    'user_id': user,
                    'createddate': datetime.now(),
                    'createdby': createdby
                })
            cls.objects.bulk_create([
                cls(**field) for field in data
            ])
        elif len_permissions == 1:
            sys_privilege = cls()
            sys_privilege.fk_p_form = fk_p_form
            sys_privilege.permission = permissions[0]
            sys_privilege.user_id = user
            sys_privilege.createddate = datetime.now()
            sys_privilege.createdby = createdby
            sys_privilege.save()
        elif len_permissions < 1:
            raise ValueError('permission cannot be null')
        return 'successfully added custom permission'


class NAGoodsReceive_other(NA_GoodsReceiveModel):
    fk_goods = models.ForeignKey(
        goods,
        db_column='fk_goods',
        db_constraint=False
    )
    fk_receivedby = models.ForeignKey(
        Employee,
        db_column='FK_ReceivedBy',
        max_length=50,
        related_name='fk_receivedBy_other',
        db_constraint=False
    )
    fk_p_r_by = models.ForeignKey(
        Employee,
        db_column='FK_P_R_By',
        max_length=50,
        blank=True,
        null=True,
        related_name='fk_p_r_by_other',
        db_constraint=False
    )

    objects = NA_BR_Goods_Receive_other()

    class Meta:
        db_table = 'n_a_goods_receive_other'


class NAGoodsHistory(NA_TransactionModel):
    modifieddate = None
    modifiedby = None
    fk_employee = None

    fk_lending = models.ForeignKey(
        NAGoodsLending,
        null=True,
        blank=True,
        db_column='FK_Lending',
        db_constraint=False
    )

    fk_outwards = models.ForeignKey(
        NAGoodsOutwards,
        null=True,
        blank=True,
        db_column='FK_Outwards',
        db_constraint=False
    )

    fk_return = models.ForeignKey(
        NAGoodsReturn,
        null=True,
        blank=True,
        db_column='FK_Return',
        db_constraint=False
    )

    fk_maintenance = models.ForeignKey(
        NAMaintenance,
        null=True,
        blank=True,
        db_column='FK_Maintenance',
        db_constraint=False
    )

    fk_disposal = models.ForeignKey(
        NADisposal,
        null=True,
        blank=True,
        db_column='FK_Disposal',
        db_constraint=False
    )

    fk_lost = models.ForeignKey(
        NAGoodsLost,
        null=True,
        blank=True,
        db_column='FK_Lost',
        db_constraint=False
    )

    class Meta:
        db_table = 'n_a_goods_history'
        managed = True


class NAGaReceive(NA_BaseModel):
    fk_goods = models.ForeignKey(
        goods,
        db_column='FK_Goods',
        db_constraint=False
    )
    fk_receivedby = models.ForeignKey(
        Employee,
        db_column='FK_ReceivedBy',
        max_length=50,
        related_name='fk_receivedBy_ga',
        db_constraint=False
    )
    fk_p_r_by = models.ForeignKey(
        Employee,
        db_column='FK_P_R_By',
        max_length=50,
        blank=True,
        null=True,
        related_name='fk_p_r_by_ga',
        db_constraint=False
    )
    fk_supplier = models.ForeignKey(
        'NASupplier',
        db_column='FK_Supplier',
        db_constraint=False
    )
    datereceived = models.DateTimeField(
        db_column='DateReceived', default=timezone.now)
    brand = models.CharField(db_column='Brand', max_length=100)
    invoice_no = models.CharField(
        db_column='Invoice_No', max_length=100, blank=True, null=True)

    typeapp = models.CharField(
        db_column='TypeApp', max_length=64, blank=True, null=True)
    machine_no = models.CharField(
        db_column='Machine_No', unique=True, max_length=50)
    chassis_no = models.CharField(db_column='Chassis_No', max_length=50)
    year_made = models.DateField(db_column='Year_Made')
    colour = models.CharField(max_length=20)
    model = models.CharField(
        db_column='Model', max_length=100, blank=True, null=True)
    kind = models.CharField(
        db_column='Kind', max_length=30, blank=True, null=True)
    cylinder = models.CharField(
        db_column='Cylinder', max_length=20, blank=True, null=True)
    fuel = models.CharField(
        db_column='Fuel', max_length=20, blank=True, null=True)
    price = models.DecimalField(
        db_column='Price', max_digits=30, decimal_places=4
    )

    descriptions = models.CharField(
        db_column='Descriptions', max_length=200, blank=True, null=True)

    objects = NA_BR_Goods_Receive_GA()

    class Meta:
        managed = True
        db_table = 'n_a_ga_receive'

    def get_history(self):
        return self.nagavnhistory_set.values(
            'idapp',
            'reg_no',
            'expired_reg',
            'bpkb_expired',
            'createddate',
            'createdby'
        )

    def get_active_reg_number(self):
        today = date.today()
        try:
            reg = self.nagavnhistory_set.get(
                expired_reg__gt=today,
                bpkb_expired__gt=today
            )
        except MultipleObjectsReturned:
            reg = self.nagavnhistory_set.active().last()
        return reg


class NAGaVnHistory(NA_BaseModel):

    EXTENDS = 'extends'
    LOST = 'lost'
    OTHER = 'other'
    PURPOSE_CHOICES = (
        (EXTENDS, 'extends'),
        (LOST, 'lost'),
        (OTHER, 'other')
    )

    reg_no = models.CharField(db_column='Reg_No', max_length=50, unique=True)
    fk_app = models.ForeignKey(
        NAGaReceive,
        db_column='FK_App',
        db_constraint=False
    )
    fk_parent = models.ForeignKey(
        'self',
        db_column='FK_Parent',
        db_constraint=False,
        null=True,
        blank=True
    )
    expired_reg = models.DateField(db_column='Expired_Reg')

    date_reg = models.DateField(db_column='Date_Reg', blank=True, null=True)
    bpkb_expired = models.DateField(
        db_column='BPKB_Expired', null=True, blank=True)
    purpose = models.CharField(
        max_length=30,
        choices=PURPOSE_CHOICES,
        db_column='Purpose',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(
        db_column='Descriptions', max_length=200, blank=True, null=True)

    objects = NAGaVnHistoryBR()

    def __str__(self):
        return self.reg_no

    @property
    def is_expired_reg(self):
        return date.today() > self.expired_reg

    @property
    def is_bpkb_expired(self):
        return date.today() > self.bpkb_expired

    @classmethod
    def get_expired_regs(cls, reg_id=None):
        result = []
        now = datetime.now()
        filter_kwargs = {
            'fk_app__is_active': True,
            'fk_app__expired_reg__range': [
                (now - timedelta(days=10)),
                now
            ]
        }
        only_fields = [  # improve performance
            'idapp',
            'fk_app__reg_no',
            'fk_app__expired_reg',
            'fk_employee__employee_name',
            'fk_employee__telphp',
            'fk_employee__inactive'
        ]
        regs = (NAGaOutwards.objects.filter(**filter_kwargs)
                                    .select_related('fk_app', 'fk_employee')
                                    .only(*only_fields))

        if reg_id:
            regs = regs.filter(fk_app=reg_id)
        regs = list(regs)

        if regs:
            for reg in regs:
                result.append({
                    'idapp': int(reg.fk_app_id),
                    'reg_number': reg.fk_app.reg_no,
                    'date_expire': reg.fk_app.expired_reg.strftime('%d/%m/%Y'),
                    'is_expire': reg.fk_app.is_expired_reg,
                    'is_dismissed': False,
                    'idapp_outwards': reg.idapp,
                    'employee_name': reg.fk_employee.employee_name,
                    'employee_phone': reg.fk_employee.telphp,
                    'employee_inactive': reg.fk_employee.inactive
                })
        return result

    class Meta:
        managed = True
        db_table = 'n_a_ga_vn_history'


class NAGoodsEquipment(NA_BaseModel):
    modifiedby = None
    modifieddate = None

    IT, GA = range(2)
    name_app = models.CharField(db_column='NameApp', max_length=50)
    type_app = models.IntegerField(
        choices=((GA, 'GA'), (IT, 'IT')),
        db_column='TypeApp',
    )

    def __str__(self):
        return '{type_app}: {name_app}'.format(
            type_app=self.get_type_app_display(),
            name_app=self.name_app
        )

    @classmethod
    def get_type_app(cls, request):
        url_name = request.resolver_match.url_name
        if re.match(r'ga', url_name):
            return cls.GA
        elif re.match(r'it', url_name):
            return cls.IT
        else:
            raise ValueError('url is not desired')

    @classmethod
    def get_equipment(cls, request):
        return cls.objects.filter(type_app=cls.get_type_app(request))

    class Meta:
        managed = True
        db_table = 'n_a_equipment'


class NAGaOutwards(NAGoodsOutwardsModel):
    # TODO: delete typeapp
    fk_lending = None
    serialnumber = None
    fk_app = models.ForeignKey(
        NAGaVnHistory,
        db_column='fk_app',
        db_constraint=False
    )
    fk_receive = models.ForeignKey(
        NAGaReceive,
        db_column='FK_Receive',
        db_constraint=False
    )
    equipment = models.ManyToManyField(
        NAGoodsEquipment,
        related_name='ga_equipment',
        db_constraint=False,
        db_column='Equipment'
    )
    add_equipment = models.ManyToManyField(
        NAGoodsEquipment,
        related_name='ga_add_equipment',
        db_constraint=False,
        db_column='AddEquipment'
    )
    objects = NABRGoodsOutwardsGA()

    class Meta:
        managed = True
        db_table = 'n_a_ga_outwards'


class NAGAReturn(NAGoodsReturnModel):
    fk_employee = None
    fk_goods_outwards = None
    fk_goods_lend = None

    fk_ga_outwards = models.ForeignKey(
        'NAGaOutwards',
        db_column='fk_ga_outwards',
        db_constraint=False,
        blank=True, null=True
    )

    objects = NA_BR_Goods_Return_GA()

    class Meta:
        managed = True
        db_table = 'n_a_ga_return'

    def __str__(self):
        return self.fk_goods.goodsname
