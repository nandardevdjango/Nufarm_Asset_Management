from django.db import models, connection
from NA_DataLayer.common import CriteriaSearch, ResolveCriteria, query, StatusForm, DataType, Data, Message

#idapp, requestdate, startdate, isstillguarante, expense,maintenanceby,personalname,enddate,fk_goods,issucced,descriptions,createddate,createdby
class NA_BR_Maintenance(models.Manager):
    def PopulateQuery(self, columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        cur = connection.cursor()
        rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
        Query = """SELECT m.idapp, m.requestdate, m.startdate, m.isstillguarantee, m.expense, m.maintenanceby, m.personalname,m.enddate,
        g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',m.typeapp) AS goods,m.serialnumber, m.issucced, m.descriptions, m.createddate,
        m.createdby FROM n_a_maintenance m INNER JOIN n_a_goods g ON m.fk_goods = g.idapp WHERE """ + columnKey + rs.Sql()
        cur.execute(Query)
        result = query.dictfetchall(cur)
        connection.close()
        return result
    def SaveData(self,statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Params = {"TypeApp":data["typeApp"],"SerialNumber":data["serialNum"],"RequestDate":data["requestdate"],"StartDate":data["startdate"],"IsStillGuarantee":data["isstillguarantee"],
                  "Expense":data["expense"],"MaintenanceBy":data["maintenanceby"],"PersonalName":data["personalname"],
                  "EndDate":data["enddate"],"FK_Goods":data["fk_goods"],"IsSucced":data["issucced"],"Descriptions":data["descriptions"]}
        if statusForm == StatusForm.Input:
            if self.dataExist(serialnumber=data['serialNum']):
                return (Data.Exists,Message.get_exists_info(self.get_createddate(data['serialNum'])['createddate']))
            else:
                Params['CreatedDate'] = data["createddate"]
                Params["CreatedBy"] = data["createdby"]
                Query = """INSERT INTO n_a_maintenance(typeapp,serialnumber,requestdate,startdate,isstillguarantee,expense,maintenanceby,personalname,enddate,
                fk_goods,issucced,descriptions,createddate,createdby) VALUES(%(TypeApp)s,%(SerialNumber)s,%(RequestDate)s,%(StartDate)s,%(IsStillGuarantee)s,%(Expense)s,
                %(MaintenanceBy)s,%(PersonalName)s,%(EndDate)s,%(FK_Goods)s,%(IsSucced)s,%(Descriptions)s,%(CreatedDate)s,%(CreatedBy)s)"""
        elif statusForm == StatusForm.Edit:
            Params['IDApp'] = data['idapp']
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Query = """UPDATE n_a_maintenance SET requestdate=%(RequestDate)s, startdate=%(StartDate)s, isstillguarantee=%(IsStillGuarantee)s,
            expense=%(Expense)s,maintenanceby=%(MaintenanceBy)s, personalname=%(PersonalName)s,enddate=%(EndDate)s,issucced=%(IsSucced)s,
            descriptions=%(Descriptions)s,modifieddate=%(ModifiedDate)s,modifiedby=%(ModifiedBy)s WHERE idapp=%(IDApp)s"""
        cur.execute(Query,Params)
        row = cur.lastrowid
        connection.close()
        return (Data.Success,Message.Success.value)
    
    def DeleteData(self,idapp):
        if self.dataExist(idapp=idapp):
            cur = connection.cursor()
            Query = """DELETE FROM n_a_maintenance WHERE idapp=%s"""
            cur.execute(Query,[idapp])
            return (Data.Success,Message.Success.value)
        else:
            return (Data.Lost,Message.Lost.value)
    def retriveData(self,idapp):
        if self.dataExist(idapp=idapp):
            cur = connection.cursor()
            Query = """SELECT m.fk_goods,g.itemcode, CONCAT(g.goodsname, ' ',g.brandname) as goods,m.typeapp AS typeApp,m.serialnumber AS serialNum,grt.minusdesc AS minus, m.requestdate,
            m.startdate, m.isstillguarantee, m.expense, m.maintenanceby,m.personalname, m.enddate, m.issucced, m.descriptions FROM n_a_maintenance m 
            INNER JOIN n_a_goods g ON m.fk_goods = g.idapp INNER JOIN n_a_goods_return grt on g.idapp = grt.fk_goods AND grt.serialnumber = m.serialnumber
            WHERE m.idapp = %(IDApp)s"""
            cur.execute(Query,{'IDApp':idapp})
            result = query.dictfetchall(cur)
            connection.close()
            return (Data.Success,result)
        else:
            return (Data.Lost,)

    def search_M_ByForm(self,value):
        cur = connection.cursor()
        Query = """SELECT g.idapp,g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grt.typeapp) AS goods,grt.serialnumber, 
        IF(NOW() <= grd.endofwarranty,'True','False') AS still_guarantee,grt.conditions,grt.minusdesc FROM n_a_goods_return grt INNER JOIN n_a_goods g ON grt.fk_goods = g.idapp 
        INNER JOIN n_a_goods_receive gr ON g.idapp = gr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON gr.idapp = grd.fk_app 
        AND grt.serialnumber = grd.serialnumber WHERE NOT EXISTS (SELECT m.fk_goods FROM n_a_maintenance m WHERE m.fk_goods = g.idapp)
        AND grt.conditions <> 'W' AND CONCAT(g.goodsname, ' ',g.brandname, ' ',g.typeapp) LIKE '%{0}%'""".format(value)
        cur.execute(Query)
        result = query.dictfetchall(cur)
        connection.close()
        return result

    def getGoods_data(self,idapp,serialnumber):
        cur = connection.cursor()
        if self.dataExist(serialnumber=serialnumber):
            return (Data.Exists,Message.get_exists_info(self.get_createddate(serialnumber)['createddate']))
        else:
            Query = """SELECT g.idapp,g.itemcode,g.goodsname,g.brandname,grt.typeapp, grt.serialnumber,grt.minusdesc, IF(NOW() <= grd.endofwarranty, 'True','False')
            AS still_guarantee FROM n_a_goods_return grt INNER JOIN n_a_goods g ON grt.fk_goods = g.idapp INNER JOIN n_a_goods_receive gr ON g.idapp = gr.fk_goods
            INNER JOIN n_a_goods_receive_detail grd ON gr.idapp = grd.fk_app AND grd.serialnumber = grt.serialnumber WHERE g.idapp = %s"""
            cur.execute(Query,[idapp])
            result = query.dictfetchall(cur)
            connection.close()
            if len(result) == 0:
                return (Data.Empty,)
            return (Data.Success,result[0])
    def dataExist(self,**kwargs):
        data = super(NA_BR_Maintenance, self).get_queryset().values('idapp')
        idapp = kwargs.get('idapp')
        if idapp is not None:
            return data.filter(idapp=idapp).exists()
        serialnumber = kwargs.get('serialnumber')
        if serialnumber is not None:
            return data.filter(serialnumber=serialnumber).exists()

    def get_createddate(self,serial_num):
        data = super(NA_BR_Maintenance,self).get_queryset().values('createddate').filter(serialnumber=serial_num)
        return data[0]