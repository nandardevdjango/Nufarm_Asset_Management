from django.db import models, connection, transaction
from NA_DataLayer.common import CriteriaSearch, ResolveCriteria, query, StatusForm, DataType, Data, Message
from dateutil.parser import parse
from django.db.models import Q
#idapp, requestdate, startdate, isstillguarante, expense,maintenanceby,personalname,enddate,fk_goods,issucced,descriptions,createddate,createdby


class NA_BR_Maintenance(models.Manager):
    def PopulateQuery(self, orderFields, sortIndice, pageSize, PageIndex, userName, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        colKey = 'g.goodsname'
        if columnKey == 'goods':
            colKey = 'g.goodsname'
        elif columnKey == 'typeapp':
            colKey = 'm.TypeApp'
        elif columnKey == 'serialnumber':
            colKey = 'm.serialnumber'
        elif columnKey == 'requestdate':
            colKey = 'm.requestdate'
        elif columnKey == 'startdate':
            colKey = 'm.startdate'
        elif columnKey == 'enddate':
            colKey = 'm.enddate'
        elif columnKey == 'isstillguarantee':
            colKey = 'm.isstillguarantee'
        elif columnKey == 'maintenanceby':
            colKey = 'm.maintenanceby'
        elif columnKey == 'personalname':
            colKey = 'm.personalname'
        elif columnKey == 'isfinished':
            colKey = 'm.isfinished'
        elif columnKey == 'issucced':
            colKey = 'm.issucced'
        elif columnKey == 'expense':
            colKey = 'm.expense'
        elif columnKey == 'createdby':
            colKey = 'm.createdby'
        elif columnKey == 'createddate':
            colKey = 'm.createddate'
        elif columnKey == 'descriptions':
            colKey = 'm.descriptions'
        cur = connection.cursor()
        cur.execute(
            "DROP TEMPORARY TABLE IF EXISTS T_Maintenance_Manager_" + userName)
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        Query = "CREATE TEMPORARY TABLE T_Maintenance_Manager_" + userName + """ ENGINE=MyISAM AS(SELECT m.idapp, m.requestdate, m.startdate, m.isstillguarantee, m.expense, m.maintenanceby, m.personalname,m.enddate,
        g.itemcode,CONCAT(g.goodsname, ' ',ngd.brandname, ' ',m.typeapp) AS goods,m.serialnumber, m.issucced,m.isfinished, m.descriptions, m.createddate,
        m.createdby FROM n_a_maintenance m INNER JOIN n_a_goods g ON m.fk_goods = g.idapp
        INNER JOIN n_a_goods_receive ngr ON ngr.fk_goods = g.IDApp INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp AND m.serialnumber = ngd.serialnumber WHERE """ + colKey + rs.Sql() + ")"
        cur.execute(Query)
        strLimit = '20'  # ambil yang paling kecil di grid
        if int(PageIndex) <= 1:
            strLimit = '0'
        else:
            strLimit = str((int(PageIndex)-1) * int(pageSize))
        if orderFields != '':
            Query = "SELECT * FROM T_Maintenance_Manager_" + userName + " ORDER BY " + orderFields + \
                (" DESC" if sortIndice == "" else ' ' + sortIndice) + \
                " LIMIT " + strLimit + "," + str(pageSize)
        else:
            Query = "SELECT * T_Maintenance_Manager_" + userName + \
                " ORDER BY IDApp LIMIT " + strLimit + "," + str(pageSize)
        cur.execute(Query)
        result = query.dictfetchall(cur)
        # get countRows
        Query = """SELECT COUNT(*) FROM T_Maintenance_Manager_""" + userName
        cur.execute(Query)
        row = cur.fetchone()
        totalRecords = row[0]
        cur.close()
        return (result, totalRecords)
        # return result

    def SaveData(self, statusForm=StatusForm.Input, **data):
        try:
            cur = connection.cursor()
            with transaction.atomic():
                Params = {"TypeApp": data["typeApp"], "SerialNumber": data["serialNum"], "RequestDate": data["requestdate"], "StartDate": data["startdate"], "IsStillGuarantee": data["isstillguarantee"],
                          "Expense": data["expense"], "MaintenanceBy": data["maintenanceby"], "PersonalName": data["personalname"],
                          "EndDate": data["enddate"], "FK_Goods": data["fk_goods"], "IsSucced": data["issucced"], "isFinished": data['isfinished'], "Descriptions": data["descriptions"]}
                if statusForm == StatusForm.Input:
                    if self.dataExist(serialnumber=data['serialNum'], fk_goods=data['fk_goods'], startdate=data['startdate'], enddate=data['enddate']):
                        return (Data.Exists, Message.get_exists_info(self.get_createddate(data['serialNum'])['createddate']))
                    else:
                        Params['CreatedDate'] = data["createddate"]
                        Params["CreatedBy"] = data["createdby"]
                        Query = """INSERT INTO n_a_maintenance(typeapp,serialnumber,requestdate,startdate,isstillguarantee,expense,maintenanceby,personalname,enddate,
                        fk_goods,isfinished,issucced,descriptions,createddate,createdby) VALUES(%(TypeApp)s,%(SerialNumber)s,%(RequestDate)s,%(StartDate)s,%(IsStillGuarantee)s,%(Expense)s,
                        %(MaintenanceBy)s,%(PersonalName)s,%(EndDate)s,%(FK_Goods)s,%(isFinished)s,%(IsSucced)s,%(Descriptions)s,%(CreatedDate)s,%(CreatedBy)s)"""
                    # insert GA_History
                    cur.execute(Query, Params)
                    FKApp = cur.lastrowid
                    Query = """INSERT INTO n_a_goods_history(FK_Goods, TypeApp, SerialNumber, FK_Lending, FK_Outwards, FK_RETURN, FK_Maintenance, FK_Disposal, FK_LOST, CreatedDate, CreatedBy) \
                    		 VALUES (%(FK_Goods)s,%(TypeApp)s, %(SerialNumber)s, NULL,NULL, NULL, %(FK_Maintenance)s, NULL, NULL, NOW(), %(CreatedBy)s )"""
                    Params = {'FK_Goods': data['fk_goods'], 'TypeApp': data['typeApp'],
                              'SerialNumber': data['serialNum'], 'FK_Maintenance': FKApp, 'CreatedBy': data['createdby']}
                elif statusForm == StatusForm.Edit:
                    Params['IDApp'] = data['idapp']
                    Params['ModifiedDate'] = data['modifieddate']
                    Params['ModifiedBy'] = data['modifiedby']
                    Query = """UPDATE n_a_maintenance SET requestdate=%(RequestDate)s, startdate=%(StartDate)s, isstillguarantee=%(IsStillGuarantee)s,
                    expense=%(Expense)s,maintenanceby=%(MaintenanceBy)s, personalname=%(PersonalName)s,enddate=%(EndDate)s,issucced=%(IsSucced)s,isfinished=%(isFinished)s,
                    descriptions=%(Descriptions)s,modifieddate=%(ModifiedDate)s,modifiedby=%(ModifiedBy)s WHERE idapp=%(IDApp)s"""
                cur.execute(Query, Params)
                cur.close()
        except Exception as e:
            cur.close()
            return (Data.Empty, e.message)
        return (Data.Success, Message.Success.value)

    def DeleteData(self, idapp):
        try:
            cur = connection.cursor()
            with transaction.atomic():
                Query = """DELETE FROM n_a_maintenance WHERE idapp=%s"""
                cur.execute(Query, [idapp])
                Query = """DELETE FROM n_a_goods_history WHERE FK_Maintenance = %s"""
                cur.execute(Query, [idapp])
                cur.close()
        except Exception as e:
            cur.close()
            return (Data.Empty, e.message)
        return (Data.Success, Message.Success.value)

    def retriveData(self, idapp):
        cur = connection.cursor()
        Query = """SELECT m.fk_goods,g.itemcode, CONCAT(g.goodsname, ' ',g.brandname, ' ', m.typeapp) as goods,m.typeapp AS typeApp,m.serialnumber AS serialNum,grt.minusdesc AS minus, m.requestdate,
        m.startdate, m.isstillguarantee, m.expense, m.maintenanceby,m.personalname, m.enddate,m.isfinished, m.issucced, m.descriptions,
        CASE WHEN (EXISTS(SELECT FK_Goods FROM n_a_disposal WHERE FK_Goods = m.fk_goods AND SerialNumber = m.serialnumber)) THEN 'True'
             WHEN (EXISTS(SELECT FK_Goods FROM n_a_goods_deletion WHERE FK_Goods = m.fk_goods AND SerialNumber = m.serialnumber)) THEN 'True'
             WHEN (EXISTS(SELECT FK_Goods FROM n_a_goods_lending WHERE FK_Goods = m.fk_goods AND FK_Maintenance = m.IDApp)) THEN 'True'
             WHEN (EXISTS(SELECT FK_Goods FROM n_a_goods_lost WHERE FK_Goods = m.fk_goods AND SerialNumber = m.serialnumber)) THEN 'True'
             WHEN (EXISTS(SELECT FK_Goods FROM n_a_goods_outwards WHERE FK_Goods = m.fk_goods AND FK_FromMaintenance = m.IDApp)) THEN 'True'
             ELSE 'False'
        END AS hasRefData FROM n_a_maintenance m
        INNER JOIN n_a_goods g ON m.fk_goods = g.idapp INNER JOIN n_a_goods_return grt on g.idapp = grt.fk_goods AND grt.serialnumber = m.serialnumber
        WHERE m.idapp = %(IDApp)s"""
        cur.execute(Query, {'IDApp': idapp})
        result = query.dictfetchall(cur)
        connection.close()
        return (Data.Success, result)

    def search_M_ByForm(self, searchText, orderFields, sortIndice, pageSize, PageIndex, userName, includeNotYetUsed=False):
        cur = connection.cursor()
        # Query = """SELECT g.idapp,g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grt.typeapp) AS goods,grt.serialnumber,
        # IF(NOW() <= grd.endofwarranty,'True','False') AS still_guarantee,grt.conditions,grt.minusdesc FROM n_a_goods_return grt INNER JOIN n_a_goods g ON grt.fk_goods = g.idapp
        # INNER JOIN n_a_goods_receive gr ON g.idapp = gr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON gr.idapp = grd.fk_app
        # AND grt.serialnumber = grd.serialnumber WHERE NOT EXISTS (SELECT m.fk_goods FROM n_a_maintenance m WHERE m.fk_goods = g.idapp)
        # AND grt.conditions <> 'W' AND CONCAT(g.goodsname, ' ',g.brandname, ' ',g.typeapp) LIKE '%{0}%'""".format(value)
        Query = "DROP TEMPORARY TABLE IF EXISTS T_Search_Maintenance_" + userName
        cur = connection.cursor()
        cur.execute(Query)

        Query = """ CREATE TEMPORARY TABLE T_Search_Maintenance_""" + userName + """ ENGINE=MyISAM AS (
                SELECT ngh.fk_goods AS idapp,ngh.itemcode,CONCAT(ngh.goodsname, ' ',ngh.brandname, ' ',ngh.typeapp) AS goods,ngh.typeapp,ngh.serialNumber,
                IF(NOW() <= ngh.endofwarranty,'True','False') AS still_guarantee,
                CASE
                	WHEN ngh.FK_Return IS NOT NULL THEN
                		(CASE
                			WHEN (SELECT conditions FROM n_a_goods_return WHERE IDApp = ngh.FK_return) <> 1 THEN
                					(SELECT CASE conditions WHEN 2 THEN 'Less Good'
                												   WHEN 3 THEN 'Broken'
                							  						ELSE 'Other/Undetermined'
                							  END
                					 FROM n_a_goods_return WHERE IDApp = 3)
                			ELSE 'Still good'
                		 END)
                	ELSE ''
                END AS conditions,
                CASE
                	WHEN ngh.FK_Return IS NOT NULL THEN (SELECT minusdesc FROM n_a_goods_return WHERE IDApp = ngh.FK_return)
                	ELSE ''
                END AS minusdesc,
                CASE
                    WHEN (ngh.fk_return IS NOT NULL) THEN (SELECT emp.Employee_Name FROM employee emp INNER JOIN n_a_goods_return ngr ON ngr.FK_FromEmployee = emp.IDApp WHERE ngr.IDApp = ngh.fk_return)
                    WHEN (ngh.fk_lending IS NOT NULL) THEN (SELECT emp.Employee_Name FROM employee emp INNER JOIN n_a_goods_lending ngl ON ngl.FK_Employee = emp.IDApp WHERE ngl.IDApp = ngh.fk_lending)
                    WHEN (ngh.fk_outwards IS NOT NULL) THEN (SELECT emp.Employee_Name FROM employee emp INNER JOIN n_a_goods_outwards ngo ON ngo.FK_Employee = emp.IDApp WHERE ngo.IDApp = ngh.fk_outwards)
                    ELSE ''
                END AS lastUsedInfo
                FROM(
                SELECT ngr.fk_goods,g.ItemCode,g.goodsname,ngd.brandName,ngd.typeapp,ngd.SerialNumber,ngd.idapp AS fk_receive,ngh0.fk_outwards,ngh0.fk_lending,
                ngh0.fk_return,ngd.endofwarranty FROM n_a_goods g INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail ngd ON ngd.fk_app = ngr.idapp"""

        if includeNotYetUsed:
            Query = Query + """ LEFT OUTER JOIN """
        else:
            Query = Query + """ INNER JOIN """
        Query = Query + """(SELECT ngh1.* FROM n_a_goods_history ngh1 INNER JOIN n_a_goods_receive_detail ngd1 ON ngd1.SerialNumber = ngh1.SerialNumber
                INNER JOIN n_a_goods_receive ngr1 ON ngr1.IDApp = ngd1.FK_App
                WHERE ngh1.createddate = (SELECT Max(CreatedDate) FROM n_a_goods_history
                							where serialnumber = ngh1.serialnumber AND ngh1.FK_Goods = ngr1.fk_goods))
                ngh0 ON ngh0.fk_goods = g.idapp AND ngh0.serialnumber = ngd.serialnumber)ngh
                WHERE (CONCAT(ngh.goodsname, ' ',ngh.brandname, ' ',ngh.typeapp) LIKE '%{0}%' OR ngh.SerialNumber LIKE '%{1}%')
                AND NOT EXISTS(SELECT FK_Goods FROM n_a_goods_lost WHERE SerialNumber = ngh.SerialNumber)
                AND NOT EXISTS(SELECT FK_Goods FROM n_a_disposal WHERE SerialNumber = ngh.SerialNumber)
                AND NOT EXISTS(SELECT FK_Goods FROM n_a_goods_deletion WHERE SerialNumber = ngh.SerialNumber))
                """.format(searchText, searchText)
        cur.execute(Query)
        strLimit = '20'  # ambil yang terkecil
        if int(PageIndex) <= 1:
            strLimit = '0'
        else:
            strLimit = str((int(PageIndex)-1) * int(pageSize))
        if orderFields == '':
            Query = """SELECT * FROM T_Search_Maintenance_""" + userName + """ ORDER BY goods """ + \
                (" DESC" if sortIndice == "" else ' ' +
                 sortIndice)  # + " LIMIT " + strLimit + "," + str(pageSize)
            # Query = Query + " ORDER BY CONCAT(ngh.goodsname, ' ',ngh.brandname, ' ',ngh.typeapp) " + (" DESC" if sortIndice == "" else " " + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
        else:
            # allOrderFields = ['itemcode','goodsname','serialNumber','still_guarantee']
            # # orderFields = (ordertext for i in range(len))
            # for field in allOrderFields:
            #     if field in orderFields:
            #         orderFields = orderFields.replace(field, 'ngh.' + field)
            # orderFields= (orderFields.replace(field, 'ngh.' + field) for field in allOrderFields if field in orderFields)
            Query = """SELECT * FROM T_Search_Maintenance_""" + userName + """ ORDER BY """ + orderFields + \
                (" DESC" if sortIndice == "" else ' ' +
                 sortIndice)  # + " LIMIT " + strLimit + "," + str(pageSize)
            # Query  = Query + " ORDER BY " + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
        cur.execute(Query)
        result = query.dictfetchall(cur)
        # get countRows
        # Query = """SELECT COUNT(*) FROM T_Search_Maintenance_""" + userNam
        # cur.execute(Query)
        # row = cur.fetchone()
        # totalRecords = row[0]
        cur.close()
        # return (result,totalRecords)
        return result

    def getGoods_data(self, idapp, serialnumber):
        cur = connection.cursor()
        if self.dataExist(serialnumber=serialnumber):
            return (Data.Exists, Message.get_exists_info(self.get_createddate(serialnumber)['createddate']))
        else:
            Query = """SELECT g.idapp,g.itemcode,g.goodsname,g.brandname,grt.typeapp, grt.serialnumber,grt.minusdesc, IF(NOW() <= grd.endofwarranty, 'True','False')
            AS still_guarantee FROM n_a_goods_return grt INNER JOIN n_a_goods g ON grt.fk_goods = g.idapp INNER JOIN n_a_goods_receive gr ON g.idapp = gr.fk_goods
            INNER JOIN n_a_goods_receive_detail grd ON gr.idapp = grd.fk_app AND grd.serialnumber = grt.serialnumber WHERE g.idapp = %s"""
            cur.execute(Query, [idapp])
            result = query.dictfetchall(cur)
            connection.close()
            if len(result) == 0:
                return (Data.Empty,)
            return (Data.Success, result[0])

    def dataExist(self, **kwargs):
        SN = kwargs.get('idapp')
        startdate = kwargs.get('startdate')
        enddate = kwargs.get('enddate')
        fk_goods = kwargs.get('fk_goods')
        startdate1 = parse(startdate).strftime('%Y-%m-%d')
        startdate2 = parse(startdate).strftime('%Y-%m-%d %H:%M:%S')
        enddate1 = parse(enddate).strftime('%Y-%m-%d')
        enddate2 = parse(enddate).strftime('%Y-%m-%d %H:%M:%S')
        filterdate = {'startdate__range': [parse(startdate1), parse(
            startdate2)], 'enddate__range': [parse(enddate1), parse(enddate2)]}
        xdata = super(NA_BR_Maintenance, self).get_queryset().filter(
            Q(fk_goods=fk_goods) & Q(serialnumber=SN)).filter(**filterdate)
        return xdata.exists()

        #     return data.filter(idapp=idapp).exists()
        # serialnumber = kwargs.get('serialnumber')
        # if serialnumber is not None:
        #     return data.filter(Q(serialnumber__iexact=SN)&Q()).exists()
    def getPersonalName(self, personname):
        data = super(NA_BR_Maintenance, self).get_queryset().values(
            'personalname').filter(personalname=personname).distinct()
        if data:
            return data[0]
        else:
            return data

    def getMaintenanceBy(self, maintenance_by):
        data = super(NA_BR_Maintenance, self).get_queryset().values(
            'maintenanceby').filter(maintenanceby__icontains(maintenance_by)).distinct()
        if data:
            return data[0]
        else:
            return data

    def get_createddate(self, serial_num):
        data = super(NA_BR_Maintenance, self).get_queryset().values(
            'createddate').filter(serialnumber=serial_num)
        return data[0]

    def getDatabySN(self, sn):
        return super(NA_BR_Maintenance, self).get_queryset() \
            .filter(serialnumber__iexact=sn).order_by('-startdate')[:1].get()

    def getLastTrans(self, SerialNO):
        """function untuk mengambil terakhir transaksi data, sebagai umpan balik ke user, barang ini terakhir di pake oleh siapa / belum di pakai sama sekali
        param : SerialNO
        """
        # ambil data brand dan typenya
        Query = """SELECT g.idapp,g.itemcode,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS BrandName,ngd.typeapp,IF(NOW() <= ngd.endofwarranty,'True','False') AS still_guarantee FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App \
        			LEFT OUTER JOIN n_a_goods g ON g.IDApp = ngr.FK_Goods WHERE ngd.serialnumber = %s"""
        cur = connection.cursor()
        cur.execute(Query, [SerialNO])
        # idapp,fk_goods,goodsname,brandName,type,serialnumber,lastinfo,fk_outwards,fk_lending,fk_return,fk_maintenance,fk_disposal,fk_lost
        idapp = 0
        itemcode = ''
        goodsname = ''
        typeapp = ''
        brandname = ''
        serialnumber = ''
        minusdesc = ''
        still_guarantee = ''
        fkreceive = 0
        fkreturn = 0
        fklending = 0
        fkoutwards = 0
        nik_usedemployee = ''
        usedemployee = ''
        row = []
        if cur.rowcount > 0:
            row = cur.fetchone()
            still_guarantee = row[5]
            typeapp = row[4]
            brandname = row[3]
            goodsname = row[2]
            itemcode = row[1]
            idapp = row[0]
        else:
            cur.close()
            raise Exception('no such data')
        # cek apakah sudah ada transaksi untuk barang dengan serial number tsb
        Query = """SELECT EXISTS(SELECT serialnumber FROM n_a_goods_history WHERE serialnumber = %s)"""
        cur.execute(Query, [SerialNO])
        row = cur.fetchone()

        if int(row[0]) > 0:
                # cek apakah data sudah di
                # jika ada ambil data transaksi terakhir yang mana transaksi ada 4 kelompok,lending,outwards,return,maintenance
            Query = """SELECT FK_Outwards,FK_Lending,FK_RETURN FROM n_a_goods_history WHERE serialnumber = %s ORDER BY createddate DESC LIMIT 1 """
            cur.execute(Query, [SerialNO])
            row = cur.fetchone()
            if cur.rowcount > 0:
                if row[0] is not None:
                    fkoutwards = row[0]
                if row[1] is not None:
                    fklending = row[1]
                if row[2] is not None:
                    fkreturn = row[2]
            if int(fkreturn) > 0:
                Query = """SELECT emp.nik,emp.Employee_Name,minusdesc FROM n_a_goods_return ngt INNER JOIN employee emp ON emp.idapp = ngt.FK_FromEmployee WHERE ngt.IDApp = %s"""
                cur.execute(Query, [fkreturn])
                if cur.rowcount > 0:
                    row = cur.fetchone()
                    nik_usedemployee = str(row[0])
                    usedemployee = str(row[1])
                    minusdesc = row[2]
            if int(fklending) > 0:
                Query = """SELECT emp.nik,emp.Employee_Name FROM employee emp INNER JOIN n_a_goods_lending ngl ON ngl.FK_Employee = emp.IDApp WHERE ngl.IDApp = %s"""
                cur.execute(Query, [fklending])
                if cur.rowcount > 0:
                    row = cur.fetchone()
                    nik_usedemployee = str(row[0])
                    usedemployee = str(row[1])
            elif int(fkoutwards) > 0:
                Query = """SELECT e.idapp,e.nik,e.employee_name,ngo.datereleased,ngo.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.idapp = ngo.FK_Employee
                WHERE ngo.IDApp = %s"""
                cur.execute(Query, [fkoutwards])
                if cur.rowcount > 0:
                    row = cur.fetchone()
                    nik_usedemployee = str(row[0])
                    usedemployee = str(row[1])
        cur.close()
        # idapp,itemcode,goodsname,brandname,typeapp,fk_usedemployee,nik_usedemployee,usedemployee,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance
        return(idapp, itemcode, goodsname+' ' + brandname + ' ' + typeapp, typeapp, 'NIK : ' + nik_usedemployee + ', ' + usedemployee, still_guarantee, minusdesc)
