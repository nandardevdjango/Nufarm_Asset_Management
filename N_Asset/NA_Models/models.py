﻿from django.db import models, connections
from datetime import datetime
from NA_DataLayer.NA_Goods_BR import NA_BR_Goods
from django_mysql.models import JSONField
from NA_DataLayer.NA_Goods_BR import NA_BR_Goods,CustomManager
from NA_DataLayer.NA_Goods_Receive_BR import NA_BR_Goods_Receive,CustomSuplierManager,custEmpManager
from NA_DataLayer.NA_Maintenance_BR import NA_BR_Maintenance
from NA_DataLayer.NA_GoodsLost_BR import NA_BR_GoodsLost
from NA_DataLayer.NA_Goods_Lending_BR import NA_BR_Goods_Lending
from NA_DataLayer.NA_Goods_Outwards_BR import NA_BR_Goods_Outwards
from NA_DataLayer.NA_Priviledge_BR import NA_BR_Priviledge
from django.core import checks
from django_mysql.utils import connection_is_mariadb
from django.contrib.auth.models import AbstractUser

def forced_mariadb_connection(self):
    errors = []

    any_conn_works = False
    conn_names = ['default'] + list(set(connections) - {'default'})
    for db in conn_names:
        conn = connections[db]
        if (
            hasattr(conn, 'mysql_version') and
            connection_is_mariadb(conn) and
            conn.mysql_version >= (5, 7)
        ):
            any_conn_works = True
            #any_conn_works = False

    if not any_conn_works:
        errors.append(
            checks.Error(
                'MySQL 5.7+ is required to use JSONField',
                hint='At least one of your DB connections should be to '
                        'MySQL 5.7+',
                obj=self,
                id='django_mysql.E016'
            )
        )
    return errors

JSONField._check_mysql_version = forced_mariadb_connection
class LogEvent(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    nameapp = models.CharField(db_column='NameApp', max_length=30)
    descriptions = JSONField()
    createddate = models.DateTimeField(db_column='CreatedDate', auto_now_add=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=30)

    def __str__(self):
        return '{}'.format(self.nameapp)
    def __get_descriptions__(self):
        return self.descriptionsapp
    class Meta:
        db_table = 'LogEvent'

class Employee(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    nik = models.CharField(db_column='NIK', max_length=50)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=32, blank=True, null=True)  # Field name made lowercase.
    jobtype = models.CharField(db_column='JobType', max_length=150, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1)  # Field name made lowercase.
    telphp = models.CharField(db_column='TelpHP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=50, blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=50, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    from NA_DataLayer.NA_Employee import NA_BR_Employee

    objects = NA_BR_Employee()
    customManager = custEmpManager()
    ##objects = models.Manager() #default manager
    class Meta:
        managed = True
        db_table = 'employee'

    def __str__(self):
        return self.employee_name

class NASuplier(models.Model):
    supliercode = models.CharField(db_column='SuplierCode', primary_key=True, max_length=30)  # Field name made lowercase.
    supliername = models.CharField(db_column='SuplierName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telp = models.CharField(db_column='Telp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hp = models.CharField(db_column='HP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contactperson = models.CharField(db_column='ContactPerson', max_length=100, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.supliername

    from NA_DataLayer.NA_Suplier import NA_BR_Suplier

    #NA = NA_BR_Suplier()
    objects = NA_BR_Suplier() #default manager
    customManager = CustomSuplierManager()
    class Meta:
        managed = True
        db_table = 'n_a_suplier'

class NAAccFa(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.ForeignKey('goods',db_column='FK_Goods', related_name='AccFA_goods',to_field='idapp')  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    year = models.DecimalField(db_column='Year', max_digits=10, decimal_places=2)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    depr_expense = models.DecimalField(db_column='Depr_Expense', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    depr_accumulation = models.DecimalField(db_column='Depr_Accumulation', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.

    from NA_DataLayer.NA_Acc_FA import NA_Acc_FA_BR
    objects = NA_Acc_FA_BR()
    class Meta:
        managed = True
        db_table = 'n_a_acc_fa'
    def __str__(self):
        return str(self.fk_goods)

class NAAppparams(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    codeapp = models.CharField(db_column='CodeApp', max_length=64)  # Field name made lowercase.
    nameapp = models.CharField(db_column='NameApp', max_length=100, blank=True, null=True)  # Field name made lowercase.
    typeapp = models.CharField(db_column='TypeApp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    valuechar = models.CharField(db_column='ValueChar', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fkidapp = models.SmallIntegerField(db_column='FKIDApp', blank=True, null=True)  # Field name made lowercase.
    fkcodeapp = models.CharField(db_column='FKCodeApp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    attstrparams = models.CharField(db_column='AttStrParams', max_length=20, blank=True, null=True)  # Field name made lowercase.
    attdecparams = models.DecimalField(db_column='AttDecParams', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    valuestrparams = models.CharField(db_column='ValueStrParams', max_length=50, blank=True, null=True)  # Field name made lowercase.
    valuedecparams = models.DecimalField(db_column='ValueDecParams', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    inactive = models.IntegerField(db_column='InActive')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_appparams'
        unique_together = (('idapp', 'codeapp'),)


class NADisposal(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datedisposal = models.DateField(db_column='DateDisposal')  # Field name made lowercase.
    ishasvalue = models.IntegerField(db_column='IsHasValue', blank=True, null=True)  # Field name made lowercase.
    issold = models.IntegerField(db_column='IsSold', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    FK_ResponsiblePerson = models.CharField(db_column='FK_ResponsiblePerson', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_acc_fa = models.CharField(db_column='FK_Acc_FA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.IntegerField(db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=10, decimal_places=4)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_disposal'


class goods(models.Model):
	idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
	itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
	goodsname = models.CharField(db_column='GoodsName', max_length=150)  # Field name made lowercase.
	brandname = models.CharField(db_column='BrandName', max_length=100, blank=True, null=True)  # Field name made lowercase.
	typeapp = models.CharField(db_column='TypeApp', max_length=32)  # Field name made lowercase.
	priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=30, decimal_places=4)  # Field name made lowercase.
	depreciationmethod = models.CharField(db_column='DepreciationMethod', max_length=3)  # Field name made lowercase.
	unit = models.CharField(db_column='Unit', max_length=30)  # Field name made lowercase.
	economiclife = models.DecimalField(db_column='EconomicLife', max_digits=10, decimal_places=2)  # Field name made lowercase.
	placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.
	descriptions = models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	inactive = models.IntegerField(db_column='InActive', blank=True, null=True)  # Field name made lowercase.
	createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
	createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		db_table = 'n_a_goods'
		managed = True
	objects =  NA_BR_Goods()
	customs = CustomManager()
	def __str__(self):
		return self.goodsname




class NAGoodsReceive(models.Model):
	idapp = models.AutoField(db_column='IDApp', primary_key=True)
	idapp_fk_goods =models.ForeignKey(goods,db_column='fk_goods')
	datereceived = models.DateTimeField(db_column='DateReceived')
	fk_suplier = models.ForeignKey(NASuplier,db_column='FK_Suplier')
	totalpurchase = models.SmallIntegerField(db_column='TotalPurchase')
	totalreceived = models.SmallIntegerField(db_column='TotalReceived')
	idapp_fk_receivedby = models.ForeignKey(Employee, db_column='FK_ReceivedBy', max_length=50, related_name='fk_receivedBy')  # Field name made lowercase.
	idapp_fk_p_r_by = models.ForeignKey(Employee,db_column='FK_P_R_By', max_length=50, blank=True, null=True, related_name='fk_p_r_by')
	createddate = models.DateTimeField(db_column='CreatedDate')
	createdby = models.CharField(db_column='Createdby', max_length=50)
	modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
	modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)
	descriptions =  models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)# Field name made lowercase.
	descbysystem =  models.CharField(db_column='DescBySystem', max_length=250, blank=True, null=True)# Field name made lowercase.
	refno =  models.CharField(db_column='REFNO', max_length=50)# Field name made lowercase.
	class Meta:
		managed = True
		db_table = 'n_a_goods_receive'
	objects = NA_BR_Goods_Receive()


class NAGoodsReturn(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    datereturn = models.DateTimeField(db_column='DateReturn')  # Field name made lowercase.
    condition = models.CharField(db_column='Condition', max_length=1)  # Field name made lowercase.
    fk_fromemployee = models.CharField(db_column='FK_FromEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_usedemployee = models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.IntegerField(db_column='IsCompleted')  # Field name made lowercase.
    minus = models.CharField(db_column='Minus', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_goods_lend = models.IntegerField(db_column='FK_Goods_Lend', blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_goods_return'


class NAMaintenance(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    requestdate = models.DateField(db_column='RequestDate', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    isstillguarantee = models.TextField(db_column='IsStillGuarantee')  # Field name made lowercase. This field type is a guess.
    expense = models.DecimalField(db_column='Expense', max_digits=10, decimal_places=4)  # Field name made lowercase.
    maintenanceby = models.CharField(db_column='MaintenanceBy', max_length=100)  # Field name made lowercase.
    personalname = models.CharField(db_column='PersonalName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    issucced = models.IntegerField(db_column='IsSucced', blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    objects = NA_BR_Maintenance()
    class Meta:
        managed = True
        db_table = 'n_a_maintenance'


class NAStock(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.IntegerField(db_column='FK_Goods')  # Field name made lowercase.
    totalqty = models.IntegerField(db_column='TotalQty')  # Field name made lowercase.
    tisused = models.IntegerField(db_column='TIsUsed')  # Field name made lowercase.
    tisnew = models.IntegerField(db_column='TIsNew')  # Field name made lowercase.
    tisrenew = models.IntegerField(db_column='TIsRenew')  # Field name made lowercase.
    isbroken = models.IntegerField(db_column='IsBroken')  # Field name made lowercase.
    tgoods_return = models.SmallIntegerField(db_column='TGoods_Return', blank=True, null=True)  # Field name made lowercase.
    tgoods_recieved = models.IntegerField(db_column='TGoods_Recieved', blank=True, null=True)  # Field name made lowercase.
    tmaintenance = models.SmallIntegerField(db_column='TMaintenance', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_stock'
class NAGoodsLending(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    fk_goods = models.ForeignKey(goods,db_column='FK_Goods')
    isnew = models.IntegerField(db_column='IsNew')
    fk_employee = models.ForeignKey(Employee,db_column='FK_Employee', related_name='fk_gl_employee_used_by')
    datelending = models.DateField(db_column='DateLending', blank=True, null=True)
    fk_stock = models.ForeignKey(NAStock, db_column='FK_Stock',related_name='fk_gl_stock')
    fk_responsibleperson = models.ForeignKey(Employee,db_column='FK_ResponsiblePerson', blank=True, null=True,related_name='fk_gl_employee_resp_person')
    interests = models.CharField(db_column='interests', max_length=150, blank=True, null=True)
    fk_sender = models.ForeignKey(Employee,db_column='FK_Sender',  blank=True, null=True,related_name='fk_gl_employee_sender')
    statuslent = models.CharField(db_column='Status', max_length=10, blank=True, null=True)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=50, blank=True, null=True)
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=50, blank=True, null=True)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    fk_maintenance = models.ForeignKey(NAMaintenance, db_column="FK_Maintenance", blank=True, null=True,related_name='fk_gl_maintenance')
    fk_return = models.ForeignKey(NAGoodsReturn, db_column='FK_RETURN',blank=True,null=True,related_name='fk_gl_goods_return')
    fk_receive = models.ForeignKey(NAGoodsReceive, db_column='FK_Receive',blank=True,null=True,related_name='fk_gl_goods_receive')
    fk_currentapp =models.ForeignKey('self', db_column='FK_CurrentApp',blank=True,null=True,related_name='fk_gl_parent')
    lastinfo = models.CharField(db_column='lastinfos', max_length=150, blank=True, null=True) 
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'n_a_goods_lending'
    objects = NA_BR_Goods_Lending()
class NAGoodsOutwards(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)  # Field name made lowercase.
    fk_goods = models.ForeignKey(goods,db_column='FK_Goods', max_length=30)  # Field name made lowercase.
    isnew = models.BooleanField(db_column='IsNew')  # Field name made lowercase.
    daterequest = models.DateTimeField(db_column='DateRequest')  # Field name made lowercase.
    datereleased = models.DateTimeField(db_column='DateReleased')  # Field name made lowercase.
    fk_employee = models.ForeignKey(Employee,db_column='FK_Employee', max_length=50, blank=True, null=True,related_name='used_by_outwards')  # Field name made lowercase.
    fk_usedemployee = models.ForeignKey(Employee,db_column='FK_UsedEmployee',related_name='rel_used_employee_outwards',null=True)# models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_frommaintenance = models.ForeignKey(Employee, related_name='rel_maintenance_outwards',db_column='FK_FromMaintenance', blank=True, null=True)  # Field name made lowercase.
    fk_responsibleperson = models.ForeignKey(Employee,db_column='FK_ResponsiblePerson', max_length=50, blank=True, null=True,related_name='rel_resp_person_outwards')  # Field name made lowercase.
    fk_sender = models.ForeignKey(Employee,related_name='rel_sender_outwards', db_column='FK_Sender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.ForeignKey(NAStock,related_name='rel_stock_outwards', db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    fk_lending = models.ForeignKey(NAGoodsLending,db_column='FK_Lending',related_name='rel_lending_outwards')
    fk_return = models.ForeignKey(NAGoodsLending,db_column='FK_Return',related_name='rel_return_outwards',null=True)
    fk_receive = models.ForeignKey(NAGoodsReceive,db_column='FK_Receive',related_name='rel_receive_outward',null=True)
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'n_a_goods_outwards'
    objects = NA_BR_Goods_Outwards()
class NAGoodsLost(models.Model):
    idapp = models.AutoField(db_column='IDApp',primary_key=True)
    fk_goods = models.ForeignKey(goods,db_column='FK_Goods')
    fk_goods_outwards = models.ForeignKey(NAGoodsOutwards,db_column='FK_Goods_Outwards')
    fk_goods_lending = models.ForeignKey(NAGoodsLending,db_column='FK_Goods_Lending')
    fk_maintenance = models.ForeignKey(NAMaintenance,db_column='FK_Maintenance')
    fk_fromgoods = models.CharField(db_column='FK_FromGoods',max_length=10)
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    fk_lostby = models.ForeignKey(Employee,db_column='FK_LostBy')
    status = models.CharField(db_column='Status',max_length=5)
    descriptions = models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)
    reason = models.CharField(db_column='Reason', max_length=250, blank=True, null=True)
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)

    objects = NA_BR_GoodsLost()
    class Meta:
        managed = True
        db_table = 'n_a_goods_lost'

class NAPriviledge(AbstractUser):
    idapp = models.AutoField(primary_key=True,db_column='IDApp')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=250,unique=True, blank=False,db_column='UserName')
    email = models.EmailField(unique=True, blank=True,db_column='Email')
    password = models.CharField(max_length=50,db_column='Password')
    picture = models.ImageField(null=True, blank=True, default='default.png',db_column='Picture')
    last_login=models.DateTimeField(db_column='Last_login')
    last_form = models.CharField(max_length=50,db_column='Last_form')
    computer_name = models.CharField(max_length=50,db_column='Computer_Name')
    ip_address = models.CharField(max_length=20,db_column='IP_Address')
    is_superuser = models.BooleanField(default=False,db_column='Is_SuperUser')
    is_staff = models.BooleanField(default=False,db_column='Is_Staff')
    is_active = models.BooleanField(default=False,db_column='InActive')
    USERNAME_FIELD = 'email' # use email to log in
    REQUIRED_FIELDS = ['username'] # required when user is created
    date_joined = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)
    createdby = models.CharField(db_column='CreatedBy', max_length=100, blank=True, null=True)
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)

    objects = NA_BR_Priviledge()

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'N_A_Priviledge'

class NAPriviledge_form(models.Model):
    idapp = models.AutoField(primary_key=True,db_column='IDApp')
    form_id = models.CharField(max_length=20,db_column='Form_id')
    form_name = models.CharField(max_length=30,db_column='Form_name')
    form_name_ori = models.CharField(max_length=50,db_column='Form_name_ori')

    class Meta:
        db_table = 'N_A_Priviledge_form'

class NASysPriviledge(models.Model):
    idapp = models.AutoField(primary_key=True,db_column='IDApp')
    fk_p_form = models.IntegerField(db_column='FK_PForm')
    permission = models.CharField(max_length=50,db_column='Permission')
    user_id = models.IntegerField(db_column='User_id')

    class Meta:
        db_table = 'N_A_Sys_Priviledge'