from django.db import models, connection, transaction
from NA_DataLayer.common import CriteriaSearch, DataType, StatusForm, ResolveCriteria, Data, Message
from django.db.models import Q
from datetime import datetime

class NA_BR_Supplier(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        supplierData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            supplierData = super(NA_BR_Supplier,self).get_queryset().exclude(**{filterfield:[ValueKey]})
        if criteria==CriteriaSearch.Equal:
            return super(NA_BR_Supplier,self).get_queryset().filter(**{filterfield: ValueKey})
        elif criteria==CriteriaSearch.Greater:
            filterfield = columnKey + '__gt'
        elif criteria==CriteriaSearch.GreaterOrEqual:
            filterfield = columnKey + '__gte'
        elif criteria==CriteriaSearch.In:
            filterfield = columnKey + '__in'
        elif criteria==CriteriaSearch.Less:
            filterfield = columnKey + '__lt'
        elif criteria==CriteriaSearch.LessOrEqual:
            filterfield = columnKey + '__lte'
        elif criteria==CriteriaSearch.Like:
            filterfield = columnKey + '__contains'
            supplierData = super(NA_BR_Supplier,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
            supplierData = super(NA_BR_Supplier,self).get_queryset().filter(**rs.DefaultModel())

        supplierData = supplierData.values('suppliercode','suppliername','address','telp','hp','contactperson','inactive','createddate','createdby')
        return supplierData

    def SaveData(self, statusForm, **data):
        cur = connection.cursor()
        Params = {'suppliercode':data['suppliercode'], 'suppliername':data['suppliername'], 'address':data['address'], 'telp':data['telp'],\
            'hp':data['hp'], 'contactperson':data['contactperson'], 'inactive':data['inactive']}
        if statusForm == StatusForm.Input:
            check_exists = self.dataExist(suppliercode=data['suppliercode'],hp=data['hp'],telp=data['telp'])
            if check_exists[0]:
                return (Data.Exists,check_exists[1])
            else:
                Query = '''INSERT INTO n_a_supplier(SupplierCode, SupplierName, Address, Telp, Hp, ContactPerson, Inactive, CreatedDate, CreatedBy)
                values(%(suppliercode)s,%(suppliername)s,%(address)s,%(telp)s,%(hp)s,%(contactperson)s,%(inactive)s,%(createddate)s,%(createdby)s)'''
                Params['createddate'] = data['createddate']
                Params['createdby'] = data['createdby']
        elif statusForm == StatusForm.Edit:
            if self.dataExist(suppliercode=data['suppliercode'])[0]:
                if self.HasRef(data['suppliercode']):
                    return (Data.HasRef,Message.HasRef_edit.value)
                else:
                    check_exists = self.dataExist(
                        'update',
                        _exclude_supplierCode=data['suppliercode'],
                        hp=data['hp'],telp=data['telp']
                        )
                    if check_exists[0]:
                        return (Data.Exists,check_exists[1])
                    else:
                        Params['modifieddate'] = data['modifieddate']
                        Params['modifiedby'] = data['modifiedby']
                        Query = """UPDATE n_a_supplier SET SupplierName=%(suppliername)s, Address=%(address)s, Telp=%(telp)s, Hp=%(hp)s,
                        ContactPerson=%(contactperson)s, Inactive=%(inactive)s,ModifiedDate=%(modifieddate)s, ModifiedBy=%(modifiedby)s
                        WHERE SupplierCode=%(suppliercode)s"""
            else:
                return (Data.Lost,Message.get_lost_info(pk=data['suppliercode'],table='supplier'))
        cur.execute(Query,Params)
        rowId = cur.lastrowid
        connection.close()
        return (Data.Success,rowId)

    def delete_supplier(self,**kwargs):
        cur = connection.cursor()
        suppliercode = kwargs['suppliercode']
        check_exists = self.dataExist(suppliercode=suppliercode)
        if check_exists[0]:
            if self.HasRef(suppliercode):
                return (Data.HasRef,Message.HasRef_del.value)
            else:
                data = self.retriveData(suppliercode)[1][0] #tuple
                createddate = data['createddate']
                modifieddate = data.get('modifieddate')
                if isinstance(createddate,datetime):
                    data['createddate'] = createddate.strftime('%d %B %Y %H:%M:%S')
                dataPrms = {'SupplierCode':data['suppliercode'],'SupplierName':data['suppliername'],'Address':data['address'],'Telp':data['telp'],
                            'Hp':data['hp'],'ContactPerson':data['contactperson'],
                            'Inactive':data['inactive'],'CreatedBy':data['createdby'],'CreatedDate':data['createddate']}
                #============== INSERT TO LOG EVENT ===============
                Query = """INSERT INTO logevent(nameapp,descriptions,createddate,createdby) VALUES(\'Deleted Supplier\',JSON_OBJECT(\'deleted\',
                        JSON_ARRAY(%(SupplierCode)s,%(SupplierName)s,%(Address)s,%(Telp)s,%(Hp)s,%(ContactPerson)s,%(Inactive)s,
                        %(CreatedDate)s,%(CreatedBy)s"""
                if modifieddate is not None:
                    if isinstance(modifieddate,datetime):
                        data['modifieddate'] = modifieddate.strftime('%d %B %Y %H:%M:%S')
                    dataPrms['ModifiedDate'] = modifieddate
                    dataPrms['ModifiedBy'] = data['modifiedby']
                    Query = Query + """,%(ModifiedDate)s,%(ModifiedBy)s"""
                Query = Query + """)),NOW(),%(NA_User)s)"""
                try:
                    with transaction.atomic():
                        NA_User = 'Admin'
                        if 'NA_User' in kwargs:
                            NA_User = kwargs['NA_User']
                        dataPrms['NA_User'] = NA_User
                        cur.execute(Query,dataPrms)
                        #================= END INSERT LOG EVENT ===============
                        cur.execute("""DELETE FROM n_a_supplier where SupplierCode=%s""",[suppliercode])
                except Exception:
                    transaction.rollback()
                    connection.close()
                    raise
                connection.close()
                return (Data.Success,Message.Success.value)
        else:
            return (Data.Lost,Message.Lost)
    def retriveData(self, get_suppliercode):
        if self.dataExist(suppliercode=get_suppliercode)[0]:
            result = super(NA_BR_Supplier, self).get_queryset()\
                .filter(suppliercode=get_suppliercode).values(
                    'suppliercode','suppliername','address','telp','hp',
                    'contactperson','inactive','createddate','createdby')
            return (Data.Success,result)
        else:
            return (Data.Lost,)

    def dataExist(self,action='insert', **kwargs):
        data = super(NA_BR_Supplier,self).get_queryset()
        supplier_code = kwargs.get('suppliercode')
        hp = kwargs.get('hp')
        telp = kwargs.get('telp')
        if supplier_code and hp and telp is not None:
            exists = data.filter(suppliercode=supplier_code,hp=hp,telp=telp).exists()
            if exists:
                return (True,Message.Exists.value)
        if supplier_code is not None:
            exist_supCode = data.filter(suppliercode=supplier_code).exists()
            if exist_supCode:
                return (True,Message.get_specific_exists('Supplier','supplier code',supplier_code))
        if hp and telp is not None:
            sup_code = supplier_code
            if action == 'update':
                sup_code = kwargs.get('_exclude_supplierCode')
            exist_hp = data.exclude(suppliercode=sup_code).filter(hp=hp).exists()
            if exist_hp:
                return (True,Message.get_specific_exists('Supplier','HP',hp))
            exist_telp = data.exclude(suppliercode=sup_code).filter(telp=telp).exists()
            if exist_telp:
                return (True,Message.get_specific_exists('Supplier','Telp',telp))
        return (False,)
    def HasRef(self,supCode):
        cur = connection.cursor()
        Query = '''SELECT EXISTS(SELECT FK_Supplier FROM n_a_goods_receive WHERE FK_Supplier=%(suppliercode)s)'''
        Params = {'suppliercode':supCode}
        cur.execute(Query,Params)
        if cur.fetchone()[0] > 0:
            cur.close()
            return True
        else:
            cur.close()
            return False

    def getSupplierByForm(self,q):
        data = super(NA_BR_Supplier,self).get_queryset()\
            .values('suppliercode','suppliername','address')\
            .filter(
                Q(suppliercode__icontains=q) |
                Q(suppliername__icontains=q) |
                Q(address__icontains=q)
            )
        if data.exists():
            return data
        else:
            return Data.Empty