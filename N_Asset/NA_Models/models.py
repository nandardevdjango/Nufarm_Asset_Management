from django.db import models, connections
from django.db.models import Q
from django_mysql.models import JSONField
from datetime import datetime
from NA_DataLayer.MasterData.NA_Goods_BR import NA_BR_Goods
from NA_DataLayer.MasterData.NA_Goods_BR import NA_BR_Goods,CustomManager
from NA_DataLayer.MasterData.NA_Suplier import NA_BR_Suplier
from NA_DataLayer.MasterData.NA_Employee import NA_BR_Employee
from NA_DataLayer.MasterData.NA_Priviledge_BR import NA_BR_Priviledge
from NA_DataLayer.MasterData.NA_Sys_Priviledge_BR import NA_BR_Sys_Priviledge

from NA_DataLayer.Transactions.NA_Goods_Receive_BR import NA_BR_Goods_Receive,CustomSuplierManager,custEmpManager
from NA_DataLayer.Transactions.NA_GoodsLost_BR import NA_BR_GoodsLost
from NA_DataLayer.Transactions.NA_Goods_Lending_BR import NA_BR_Goods_Lending
from NA_DataLayer.Transactions.NA_Goods_Outwards_BR import NA_BR_Goods_Outwards
from NA_DataLayer.Transactions.NA_Goods_Return_BR import NA_BR_Goods_Return
from NA_DataLayer.Transactions.NA_Goods_Receive_Other_BR import NA_BR_Goods_Receive_other

from NA_DataLayer.OtherPages.NA_Maintenance_BR import NA_BR_Maintenance
from NA_DataLayer.OtherPages.NA_Acc_FA import NA_Acc_FA_BR

from django.contrib.auth.models import AbstractUser

def forced_mariadb_connection(self):
    errors = []
    return errors

JSONField._check_mysql_version = forced_mariadb_connection

class NA_BaseModel(models.Model):
    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    createddate = models.DateTimeField(db_column='CreatedDate')
    createdby = models.CharField(db_column='CreatedBy', max_length=100)
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)
    modifiedby = models.CharField(db_column='ModifiedBy', max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

class NA_MasterDataModel(NA_BaseModel):
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    inactive = models.PositiveSmallIntegerField(db_column='InActive')
    descriptions = models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)

    class Meta:
        abstract = True

class NA_TransactionModel(NA_BaseModel):
    fk_goods = models.ForeignKey('goods',db_column='FK_Goods', max_length=30)
    fk_employee = models.ForeignKey('Employee',db_column='FK_Employee')
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    serialnumber = models.CharField(db_column='SerialNumber',max_length=100)

    class Meta:
        abstract = True

class NA_GoodsReceiveModel(NA_BaseModel):
    datereceived = models.DateTimeField(db_column='DateReceived')
    fk_suplier = models.ForeignKey('NASuplier',db_column='FK_Suplier')
    totalpurchase = models.SmallIntegerField(db_column='TotalPurchase')
    totalreceived = models.SmallIntegerField(db_column='TotalReceived')
    descriptions =  models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)
    descbysystem =  models.CharField(db_column='DescBySystem', max_length=250, blank=True, null=True)
    refno =  models.CharField(db_column='REFNO', max_length=50)

    class Meta:
        abstract = True

class LogEvent(NA_MasterDataModel):
    inactive = None
    typeapp = None
    modifieddate = None
    modifiedby = None

    idapp = models.AutoField(db_column='IDApp', primary_key=True)
    nameapp = models.CharField(db_column='NameApp', max_length=30)
    descriptions = JSONField()
    createddate = models.DateTimeField(db_column='CreatedDate')
    createdby = models.CharField(db_column='CreatedBy', max_length=30)

    def __str__(self):
        return '{}'.format(self.nameapp)
    def __get_descriptions__(self):
        return self.descriptionsapp
    class Meta:
        db_table = 'LogEvent'

class Employee(NA_MasterDataModel):
    nik = models.CharField(db_column='NIK', max_length=50)  # Field name made lowercase.
    employee_name = models.CharField(db_column='Employee_Name', max_length=150, blank=True, null=True)  # Field name made lowercase.
    jobtype = models.CharField(db_column='JobType', max_length=150, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1)  # Field name made lowercase.
    telphp = models.CharField(db_column='TelpHP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    territory = models.CharField(db_column='Territory', max_length=50, blank=True, null=True)  # Field name made lowercase.

    objects = NA_BR_Employee()
    customManager = custEmpManager()
    class Meta:
        managed = True
        db_table = 'employee'

    def __str__(self):
        return self.employee_name

class NASuplier(NA_MasterDataModel):
    idapp = None
    typeapp = None
    descriptions = None

    supliercode = models.CharField(db_column='SuplierCode', primary_key=True, max_length=30)  # Field name made lowercase.
    supliername = models.CharField(db_column='SuplierName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=150, blank=True, null=True)  # Field name made lowercase.
    telp = models.CharField(db_column='Telp', max_length=20, blank=True, null=True)  # Field name made lowercase.
    hp = models.CharField(db_column='HP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    contactperson = models.CharField(db_column='ContactPerson', max_length=100, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.supliername

    #NA = NA_BR_Suplier()
    objects = NA_BR_Suplier() #default manager
    customManager = CustomSuplierManager()
    class Meta:
        managed = True
        db_table = 'n_a_suplier'

class NAAccFa(NA_BaseModel):
    modifieddate = None
    modifiedby = None
    fk_goods = models.ForeignKey('goods',db_column='FK_Goods', related_name='AccFA_goods',to_field='idapp')  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber',max_length=50)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    year = models.DecimalField(db_column='Year', max_digits=10, decimal_places=2)  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    depr_expense = models.DecimalField(db_column='Depr_Expense', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    depr_accumulation = models.DecimalField(db_column='Depr_Accumulation', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=30, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.
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

class NADisposal(NA_BaseModel):
    modifiedby = None
    modifieddate = None
    fk_goods = models.CharField(db_column='FK_Goods', max_length=30, blank=True, null=True)  # Field name made lowercase.
    datedisposal = models.DateField(db_column='DateDisposal')  # Field name made lowercase.
    ishasvalue = models.IntegerField(db_column='IsHasValue', blank=True, null=True)  # Field name made lowercase.
    issold = models.IntegerField(db_column='IsSold', blank=True, null=True)  # Field name made lowercase.
    sellingprice = models.DecimalField(db_column='SellingPrice', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    FK_ResponsiblePerson = models.CharField(db_column='FK_ResponsiblePerson', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_acc_fa = models.CharField(db_column='FK_Acc_FA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.IntegerField(db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.
    bookvalue = models.DecimalField(db_column='BookValue', max_digits=10, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_disposal'

class goods(NA_MasterDataModel):
	itemcode = models.CharField(db_column='ItemCode', max_length=30)  # Field name made lowercase.
	goodsname = models.CharField(db_column='GoodsName', max_length=150)  # Field name made lowercase.
	brandname = models.CharField(db_column='BrandName', max_length=100, blank=True, null=True)  # Field name made lowercase.
	priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=30, decimal_places=4)  # Field name made lowercase.
	depreciationmethod = models.CharField(db_column='DepreciationMethod', max_length=3)  # Field name made lowercase.
	unit = models.CharField(db_column='Unit', max_length=30)  # Field name made lowercase.
	economiclife = models.DecimalField(db_column='EconomicLife', max_digits=10, decimal_places=2)  # Field name made lowercase.
	placement = models.CharField(db_column='Placement', max_length=50, blank=True, null=True)  # Field name made lowercase.

	class Meta:
		db_table = 'n_a_goods'
		managed = True
	objects =  NA_BR_Goods()
	customs = CustomManager()
	def __str__(self):
		return self.goodsname

class NAGoodsReceive(NA_GoodsReceiveModel):
	idapp_fk_goods =models.ForeignKey(goods,db_column='fk_goods')
	idapp_fk_receivedby = models.ForeignKey(Employee, db_column='FK_ReceivedBy', max_length=50, related_name='fk_receivedBy')
	idapp_fk_p_r_by = models.ForeignKey(Employee, db_column = 'FK_P_R_By', max_length = 50, blank = True, null = True, related_name = 'fk_p_r_by')
	class Meta:
		managed = True
		db_table = 'n_a_goods_receive'
	objects = NA_BR_Goods_Receive()

class NA_GoodsReceive_detail(NA_BaseModel):
    fk_app = models.ForeignKey(NAGoodsReceive, db_column='FK_App')
    brandname = models.CharField(max_length=100, db_column='BrandName')
    priceperunit = models.DecimalField(db_column='PricePerUnit', max_digits=30, decimal_places=4)
    typeapp = models.CharField(db_column='TypeApp', max_length=32)
    warranty = models.DecimalField(max_digits=6, decimal_places=2, db_column='Warranty')
    endofwarranty = models.DateTimeField(null=True, blank=True, db_column='EndOfWarranty')
    serialnumber = models.CharField(db_column='SerialNumber',max_length=100)

    class Meta:
        db_table = 'n_a_goods_receive_detail'

class NAGoodsReturn(NA_TransactionModel):
    datereturn = models.DateTimeField(db_column='DateReturn')  # Field name made lowercase.
    conditions = models.CharField(db_column='Conditions', max_length=1)  # Field name made lowercase.
    fk_fromemployee = models.CharField(db_column='FK_FromEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_usedemployee = models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iscompleted = models.IntegerField(db_column='IsCompleted')  # Field name made lowercase.
    minusDesc = models.CharField(db_column='MinusDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fk_goods_outwards = models.IntegerField(db_column='FK_Goods_Outwards')
    fk_goods_lend = models.IntegerField(db_column='FK_Goods_Lend', blank=True, null=True)  # Field name made lowercase.
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)  # Field name made lowercase.

    objects = NA_BR_Goods_Return()
    class Meta:
        managed = True
        db_table = 'n_a_goods_return'
    def __str__(self):
        return self.fk_goods.goodsname

class NAMaintenance(NA_TransactionModel):
    fk_employee = None

    requestdate = models.DateField(db_column='RequestDate', blank=True, null=True)
    startdate = models.DateField(db_column='StartDate')
    isstillguarantee = models.TextField(db_column='IsStillGuarantee')
    expense = models.DecimalField(db_column='Expense', max_digits=10, decimal_places=4)
    maintenanceby = models.CharField(db_column='MaintenanceBy', max_length=100)
    personalname = models.CharField(db_column='PersonalName', max_length=100, blank=True, null=True)
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)
    typeapp = models.CharField(db_column='TypeApp',max_length=32)
    issucced = models.IntegerField(db_column='IsSucced', blank=True, null=True)
    descriptions = models.CharField(db_column='Descriptions', max_length=200, blank=True, null=True)

    objects = NA_BR_Maintenance()
    class Meta:
        managed = True
        db_table = 'n_a_maintenance'

class NAStock(NA_BaseModel):
    fk_goods = models.IntegerField(db_column='FK_Goods')  # Field name made lowercase.
    totalqty = models.IntegerField(db_column='TotalQty')  # Field name made lowercase.
    tisused = models.IntegerField(db_column='TIsUsed')  # Field name made lowercase.
    tisnew = models.IntegerField(db_column='TIsNew')  # Field name made lowercase.
    tisrenew = models.IntegerField(db_column='TIsRenew')  # Field name made lowercase.
    isbroken = models.IntegerField(db_column='IsBroken')  # Field name made lowercase.
    tgoods_return = models.SmallIntegerField(db_column='TGoods_Return', blank=True, null=True)  # Field name made lowercase.
    tgoods_recieved = models.IntegerField(db_column='TGoods_Recieved', blank=True, null=True)  # Field name made lowercase.
    tmaintenance = models.SmallIntegerField(db_column='TMaintenance', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'n_a_stock'
class NAGoodsHistory(NA_TransactionModel):
    fk_lending = models.IntegerField(db_column='FK_Lending', blank=True, null=True)  # Field name made lowercase.
    fk_outwards = models.IntegerField(db_column='FK_Outwards', blank=True, null=True)  # Field name made lowercase.
    fk_return = models.IntegerField(db_column='FK_RETURN', blank=True, null=True)  # Field name made lowercase.
    fk_maintenance = models.IntegerField(db_column='FK_Maintenance', blank=True, null=True)  # Field name made lowercase.
    fk_disposal = models.IntegerField(db_column='FK_Disposal', blank=True, null=True)  # Field name made lowercase.
    fk_lost = models.IntegerField(db_column='FK_LOST', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'n_a_goods_history'
class NAGoodsLending(NA_TransactionModel):
    isnew = models.IntegerField(db_column='IsNew')
    datelending = models.DateField(db_column='DateLending', blank=True, null=True)
    fk_stock = models.ForeignKey(NAStock, db_column='FK_Stock',related_name='fk_gl_stock')
    fk_responsibleperson = models.ForeignKey(Employee,db_column='FK_ResponsiblePerson', blank=True, null=True,related_name='fk_gl_employee_resp_person')
    interests = models.CharField(db_column='interests', max_length=150, blank=True, null=True)
    fk_sender = models.ForeignKey(Employee,db_column='FK_Sender',  blank=True, null=True,related_name='fk_gl_employee_sender')
    statuslent = models.CharField(db_column='Status', max_length=10, blank=True, null=True)
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

class NAGoodsOutwards(NA_TransactionModel):
    isnew = models.BooleanField(db_column='IsNew')  # Field name made lowercase.
    daterequest = models.DateTimeField(db_column='DateRequest')  # Field name made lowercase.
    datereleased = models.DateTimeField(db_column='DateReleased')  # Field name made lowercase.
    fk_usedemployee = models.ForeignKey(Employee,db_column='FK_UsedEmployee',related_name='rel_used_employee_outwards',null=True)# models.CharField(db_column='FK_UsedEmployee', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_frommaintenance = models.ForeignKey(Employee, related_name='rel_maintenance_outwards',db_column='FK_FromMaintenance', blank=True, null=True)  # Field name made lowercase.
    fk_responsibleperson = models.ForeignKey(Employee,db_column='FK_ResponsiblePerson', max_length=50, blank=True, null=True,related_name='rel_resp_person_outwards')  # Field name made lowercase.
    fk_sender = models.ForeignKey(Employee,related_name='rel_sender_outwards', db_column='FK_Sender', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fk_stock = models.ForeignKey(NAStock,related_name='rel_stock_outwards', db_column='FK_Stock', blank=True, null=True)  # Field name made lowercase.
    fk_lending = models.ForeignKey(NAGoodsLending,db_column='FK_Lending',related_name='rel_lending_outwards')
    fk_return = models.ForeignKey(NAGoodsLending,db_column='FK_Return',related_name='rel_return_outwards',null=True)
    fk_receive = models.ForeignKey(NAGoodsReceive,db_column='FK_Receive',related_name='rel_receive_outward',null=True)
    class Meta:
        managed = True
        db_table = 'n_a_goods_outwards'
    objects = NA_BR_Goods_Outwards()

class NAGoodsLost(NA_TransactionModel):
    fk_employee = None
    fk_goods_outwards = models.ForeignKey(NAGoodsOutwards,db_column='FK_Goods_Outwards')
    fk_goods_lending = models.ForeignKey(NAGoodsLending,db_column='FK_Goods_Lending')
    fk_maintenance = models.ForeignKey(NAMaintenance,db_column='FK_Maintenance')
    
    fromgoods = models.CharField(db_column='FromGoods',max_length=10)
    fk_lostby = models.ForeignKey(Employee,db_column='FK_LostBy',related_name='lost_by')
    fk_usedby = models.ForeignKey(
        Employee,
        db_column='FK_UsedBy',
        null=True,
        blank=True,
        related_name='used_by'
    )
    fk_responsibleperson = models.ForeignKey(
        Employee,
        db_column='FK_ResponsiblePerson', 
        blank=True, 
        null=True, 
        related_name='resp_person_goods_lost'
    )
    status = models.CharField(db_column='Status',max_length=5)
    descriptions = models.CharField(db_column='Descriptions', max_length=250, blank=True, null=True)
    reason = models.CharField(db_column='Reason', max_length=250, blank=True, null=True)

    objects = NA_BR_GoodsLost()
    class Meta:
        managed = True
        db_table = 'n_a_goods_lost'

class NAPriviledge(AbstractUser,NA_BaseModel):

    IT = 'IT'
    GA = 'GA'

    DIVISI_CHOICES = (
        (IT,'IT'),
        (GA,'GA')
    )

    SUPER_USER = 1
    USER = 2
    GUEST = 3

    ROLE_CHOICES = (
        (GUEST,'Guest'),
        (USER,'User'),
        (SUPER_USER,'Super User')
    )

    createddate = None

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=250,unique=True, blank=False,db_column='UserName')
    email = models.EmailField(unique=True, blank=True,db_column='Email')
    divisi = models.CharField(max_length=5,db_column='Divisi',choices=DIVISI_CHOICES)
    password = models.CharField(max_length=128,db_column='Password')
    picture = models.ImageField(null=True, blank=True, default='default.png',db_column='Picture')
    last_login=models.DateTimeField(db_column='Last_login')
    last_form = models.CharField(max_length=50,db_column='Last_form')
    computer_name = models.CharField(max_length=50,db_column='Computer_Name')
    ip_address = models.CharField(max_length=20,db_column='IP_Address')

    role = models.IntegerField(choices=ROLE_CHOICES,default=GUEST,db_column='Role')
    is_superuser = models.BooleanField(default=False,db_column='Is_SuperUser')
    is_staff = models.BooleanField(default=False,db_column='Is_Staff')
    is_active = models.BooleanField(default=True,db_column='Is_Active')
    USERNAME_FIELD = 'email' # use email to log in
    REQUIRED_FIELDS = ['username'] # required when user is created
    date_joined = models.DateTimeField(db_column='Date_Joined', blank=True, null=True)

    objects = NA_BR_Priviledge()

    def __str__(self):
        return self.username

    def has_permission(self,action,form_name_ori):
        """
        this function for check if user has permission
        param
        :action: ==> e.g (Allow View,Allow Edit .. etc) use attribute NASysPriviledge.Allow_View .. etc
        :form_name_ori: this is form name ori e.g (n_a_suplier) use attribute NAPriviledge_form.Suplier_form .. etc

        usage : must be instance of model
        rimba = NAPriviledge.objects.get(username='rimba47prayoga') or from request : request.user.has_permission
        rimba.has_permission(NASysPriviledge.Allow_Add,NAPriviledge_form.Suplier_form)

        return boolean
        """
        if action not in NASysPriviledge.ALL_PERMISSION:
            raise ValueError('uncategorize, cannot resolve action %s' % action)

        if form_name_ori not in NAPriviledge_form.ALL_FORM:
            raise ValueError('uncategorize, cannot resolve form %s' % form_name_ori)

        is_has = self.nasyspriviledge_set.filter(
            fk_p_form__form_name_ori=form_name_ori,
            permission=action,
            inactive=False
        ).exists()
        return is_has

    #============ Permission for Employee form =============
    @property
    def allow_view_employee(self):
        return self.has_permission(
            NASysPriviledge.Allow_View,
            NAPriviledge_form.Employee_form
        )

    @property
    def allow_add_employee(self):
        return self.has_permission(
            NASysPriviledge.Allow_Add,
            NAPriviledge_form.Employee_form
        )
    @property
    def allow_edit_employee(self):
        return self.has_permission(
            NASysPriviledge.Allow_Edit,
            NAPriviledge_form.Employee_form
        )
    @property
    def allow_delete_employee(self):
        return self.has_permission(
            NASysPriviledge.Allow_Delete,
            NAPriviledge_form.Employee_form
        )


    #============ Permission for Suplier form =============
    @property
    def allow_view_suplier(self):
        return self.has_permission(
            NASysPriviledge.Allow_View,
            NAPriviledge_form.Suplier_form
        )

    @property
    def allow_add_suplier(self):
        return self.has_permission(
            NASysPriviledge.Allow_Add,
            NAPriviledge_form.Suplier_form
        )
    @property
    def allow_edit_suplier(self):
        return self.has_permission(
            NASysPriviledge.Allow_Edit,
            NAPriviledge_form.Suplier_form
        )
    @property
    def allow_delete_suplier(self):
        return self.has_permission(
            NASysPriviledge.Allow_Delete,
            NAPriviledge_form.Suplier_form
        )


    #============ Permission for Goods form =============
    @property
    def allow_view_goods(self):
        return self.has_permission(
            NASysPriviledge.Allow_View,
            NAPriviledge_form.Goods_form
        )

    @property
    def allow_add_goods(self):
        return self.has_permission(
            NASysPriviledge.Allow_Add,
            NAPriviledge_form.Goods_form
        )
    @property
    def allow_edit_goods(self):
        return self.has_permission(
            NASysPriviledge.Allow_Edit,
            NAPriviledge_form.Goods_form
        )
    @property
    def allow_delete_goods(self):
        return self.has_permission(
            NASysPriviledge.Allow_Delete,
            NAPriviledge_form.Goods_form
        )

    #============ Permission for Goods form =============
    @property
    def allow_view_goods_receive(self):
        return self.has_permission(
            NASysPriviledge.Allow_View,
            NAPriviledge_form.Goods_Receive_form
        )

    @property
    def allow_add_goods_receive(self):
        return self.has_permission(
            NASysPriviledge.Allow_Add,
            NAPriviledge_form.Goods_Receive_form
        )
    @property
    def allow_edit_goods_receive(self):
        return self.has_permission(
            NASysPriviledge.Allow_Edit,
            NAPriviledge_form.Goods_Receive_form
        )
    @property
    def allow_delete_goods_receive(self):
        return self.has_permission(
            NASysPriviledge.Allow_Delete,
            NAPriviledge_form.Goods_Receive_form
        )


    #============ Permission for Goods form =============
    @property
    def allow_view_priviledge(self):
        return self.has_permission(
            NASysPriviledge.Allow_View,
            NAPriviledge_form.Priviledge_form
        )

    @property
    def allow_add_priviledge(self):
        return self.has_permission(
            NASysPriviledge.Allow_Add,
            NAPriviledge_form.Priviledge_form
        )
    @property
    def allow_edit_priviledge(self):
        return self.has_permission(
            NASysPriviledge.Allow_Edit,
            NAPriviledge_form.Priviledge_form
        )
    @property
    def allow_delete_priviledge(self):
        return self.has_permission(
            NASysPriviledge.Allow_Delete,
            NAPriviledge_form.Priviledge_form
        )

    class Meta:
        managed = True
        db_table = 'N_A_Priviledge'

class NAPriviledge_form(models.Model):

    Employee_form = 'employee'
    Suplier_form = 'n_a_suplier'
    Goods_form = 'goods'
    Goods_Receive_form = 'n_a_goods_receive'
    Priviledge_form = 'n_a_priviledge'

    MASTER_DATA_FORM = [
        Employee_form,
        Suplier_form,
        Goods_form,
        Priviledge_form
    ]
    TRANSACTION_FORM = [
        Goods_Receive_form
    ]

    ALL_FORM = MASTER_DATA_FORM + TRANSACTION_FORM

    FORM_NAME_ORI_CHOICES = (
        (Employee_form,'employee'),
        (Suplier_form,'n_a_suplier'),
        (Goods_form,'goods'),
        (Goods_Receive_form,'n_a_goods_receive'),
        (Priviledge_form,'n_a_priviledge')
    )

    idapp = models.AutoField(primary_key=True,db_column='IDApp')
    form_id = models.CharField(max_length=20,db_column='Form_id')
    form_name = models.CharField(max_length=30,db_column='Form_name')
    form_name_ori = models.CharField(
        max_length=50,
        db_column='Form_name_ori',
        choices=FORM_NAME_ORI_CHOICES
    )

    class Meta:
        db_table = 'N_A_Priviledge_form'

    def __str__(self):
        return self.form_name

    @classmethod
    def get_form_IT(cls,must_iterate=False):
        fk_form = cls.objects\
            .filter(
                Q(form_name_ori='goods') |
                Q(form_name_ori='n_a_suplier') |
                Q(form_name_ori='employee')
            )
        if must_iterate:
            fk_form = fk_form.iterator() #technic for loop queryset, improve performance
        return fk_form

    @staticmethod
    def get_form_GA(must_iterate):
        """
        not yet determine
        """
        raise NotImplementedError

    @classmethod
    def get_form_Guest(cls,must_iterate=False):
        fk_form = cls.objects\
            .filter(
                Q(form_name_ori='goods') |
                Q(form_name_ori='n_a_suplier') |
                Q(form_name_ori='employee')
            )
        if must_iterate:
            fk_form = fk_form.iterator() #technic for loop queryset, improve performance
        return fk_form

    @classmethod
    def get_user_form(cls,role,divisi,must_iterate=False):
        """
        return queryset
        """
        if int(role) == NAPriviledge.GUEST:
            return cls.get_form_Guest(must_iterate)

        if divisi == NAPriviledge.IT:
            return cls.get_form_IT(must_iterate)
        elif divisi == NAPriviledge.GA:
            return cls.get_form_GA(must_iterate)

class NASysPriviledge(NA_BaseModel):

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
        (Allow_View,'Allow View'),
        (Allow_Add,'Allow Add'),
        (Allow_Edit,'Allow Edit'),
        (Allow_Delete,'Allow Delete')
    )

    fk_p_form = models.ForeignKey(NAPriviledge_form,db_column='FK_PForm')
    permission = models.CharField(max_length=50,db_column='Permission',choices=PERMISSION_CHOICES)
    user_id = models.ForeignKey(NAPriviledge,db_column='User_id',on_delete=models.CASCADE)
    inactive = models.IntegerField(db_column='InActive',null=True,blank=True,default=0)

    objects = NA_BR_Sys_Priviledge()
    class Meta:
        db_table = 'N_A_Sys_Priviledge'

    def __str__(self):
        return '{username} : {form_name} - {permission}'.format(
            username=self.user_id.username,
            form_name=self.fk_p_form.form_name,
            permission=self.permission
        )

    @staticmethod
    def default_permission_IT(form_name_ori):
        """
        return list of permissions [Allow View, Allow Add, etc.]
        """

        permissions = []
        if form_name_ori in NAPriviledge_form.MASTER_DATA_FORM:
            permissions.append(NASysPriviledge.Allow_View)
            permissions.append(NASysPriviledge.Allow_Add)
            permissions.append(NASysPriviledge.Allow_Edit)
            permissions.append(NASysPriviledge.Allow_Delete)
            return permissions
        else:
            raise ValueError()

    @staticmethod
    def default_permission_GA(form_name_ori):
        """
        not yet determine
        """
        raise NotImplementedError

    @staticmethod
    def default_permission_Guest(form_name_ori):
        return [NASysPriviledge.Allow_View]

    @classmethod
    def set_data_permission(cls,user,data):
        """
        not return anything, but append dict to paratemer list
        to save memory
        """
        permissions = None
        if int(user.role) == NAPriviledge.GUEST:
            permissions = cls.default_permission_Guest
        else:
            if user.divisi == NAPriviledge.IT:
                permissions = cls.default_permission_IT
            elif user.divisi == NAPriviledge.GA:
                permissions = cls.default_permission_GA

        fk_forms = NAPriviledge_form.get_user_form(user.role,user.divisi,must_iterate=True)
        if permissions is not None:
            for fk_form in fk_forms: #loop queryset
                for permission in permissions(fk_form.form_name_ori):
                    data.append({
                        'fk_p_form':fk_form, #foreign key in models must be instance
                        'permission':permission,
                        'user_id': user
                    })
        else:
            raise ValueError('')

    @classmethod
    def set_permission(cls,user):
        data = []
        cls.set_data_permission(user,data)
        sys_priviledge = cls.objects.bulk_create([
            cls(**field) for field in data
        ])
        return 'successfully added permission'

    @classmethod
    def set_custom_permission(cls,user_id,fk_form,permissions):
        user = NAPriviledge.objects.get(idapp=user_id)
        fk_p_form = NAPriviledge_form.objects.get(idapp=fk_form)
        len_permissions = len(permissions)
        if len_permissions > 1:
            data = []
            for permission in permissions:
                data.append({
                    'fk_p_form':fk_p_form,
                    'permission':permission,
                    'user_id':user
                })
            sys_priviledge = cls.objects.bulk_create([
                cls(**field) for field in data
            ])
        elif len_permissions == 1:
            sys_priviledge = cls()
            sys_priviledge.fk_p_form = fk_p_form
            sys_priviledge.permission = permissions[0]
            sys_priviledge.user_id = user
            sys_priviledge.save()
        elif len_permissions < 1:
            raise ValueError('permission cannot be null')
        return 'successfully added custom permission'

class NAGoodsReceive_other(NA_GoodsReceiveModel):
    fk_goods =models.ForeignKey(goods,db_column='fk_goods')
    fk_receivedby = models.ForeignKey(Employee, db_column='FK_ReceivedBy', max_length=50, related_name='fk_receivedBy_other')  # Field name made lowercase.
    fk_p_r_by = models.ForeignKey(Employee,db_column='FK_P_R_By', max_length=50, blank=True, null=True, related_name='fk_p_r_by_other')

    objects = NA_BR_Goods_Receive_other()
    class Meta:
        db_table = 'n_a_goods_receive_other'