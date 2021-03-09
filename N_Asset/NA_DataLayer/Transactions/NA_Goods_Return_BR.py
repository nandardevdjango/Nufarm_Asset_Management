from django.db import models, connection, transaction
from NA_DataLayer.common import (CriteriaSearch, DataType, ResolveCriteria, query,
                                 StatusForm, Data,commonFunct,Message)
from django.db.models import Q
from django.db import connection
from NA_DataLayer.exceptions import NAError, NAErrorConstant
class NA_BR_Goods_Return(models.Manager):
    def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        # goodsname
        # brandname
        # itemcode
        # fromemployee
        # serialnumber
        # usedemployee
        # datereturn
        # conditions
        # minusdesc
        if columnKey == 'goodsname':
            colKey = 'g.goodsname'
        elif columnKey == 'serialnumber':
            colKey = 'ngr.serialnumber'
        elif columnKey == 'itemcode':
            colKey = 'g.itemcode'
        elif columnKey == 'brandname':
            colKey = 'ngd.BrandName'
        elif columnKey == 'fromemployee':
            colKey = 'emp1.fromemployee'
        elif columnKey == 'usedemployee':
            colKey = 'emp2.usedemployee'
        elif columnKey == 'conditions':
            colKey = 'ngr.conditions'
        elif columnKey == 'minusdesc':
            colKey = 'ngr.minusdesc'
        cur = connection.cursor()
        cur.execute("DROP TEMPORARY TABLE IF EXISTS T_GoodsReturn_Manager_" + userName)
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        Query = "CREATE TEMPORARY TABLE T_GoodsReturn_Manager_" + userName +  """ ENGINE=MyISAM AS(SELECT ngr.idapp,ngr.datereturn,CASE ngr.conditions WHEN 1 THEN 'Good' WHEN 2 THEN 'Less Good' WHEN 3 THEN 'Broken' ELSE 'Undetermined' END AS conditions, ngr.iscompleted,ngr.isaccepted,ngr.minusDesc,ngr.typeapp,ngr.serialnumber,
        ngr.descriptions, ngr.createddate, ngr.createdby, CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),' ',IFNULL(ngd.typeapp,'')) AS goods,emp1.fromemployee,
        emp2.usedemployee FROM n_a_goods_return ngr INNER JOIN n_a_goods g ON ngr.fk_goods = g.idapp
        INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngr.serialnumber LEFT OUTER JOIN
        (SELECT idapp, employee_name AS fromemployee FROM employee) AS emp1 ON ngr.fk_fromemployee = emp1.idapp
        LEFT OUTER JOIN (SELECT idapp,employee_name AS usedemployee FROM employee) AS emp2 ON ngr.fk_usedemployee = emp2.idapp
        WHERE """ + colKey + rs.Sql() + ")"
        cur.execute(Query)
        strLimit = '20'#ambil yang paling kecil di grid
        if int(PageIndex) <= 1:
            strLimit = '0'
        else:
            strLimit = str((int(PageIndex)-1) * int(pageSize))
        if orderFields != '':
            Query = """SELECT * FROM T_GoodsReturn_Manager_""" + userName + """ ORDER BY """ + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
        else:
            Query = """SELECT * T_GoodsReturn_Manager_""" + userName + """ ORDER BY IDApp LIMIT """ + strLimit + "," + str(pageSize)
        cur.execute(Query)
        result = query.dictfetchall(cur)
        # get countRows
        Query = """SELECT COUNT(*) FROM T_GoodsReturn_Manager_""" + userName
        cur.execute(Query)
        row = cur.fetchone()
        totalRecords = row[0]
        cur.close()
        return (result, totalRecords)
    def SaveData(self, statusForm=StatusForm.Input, **data):
        try:
            cur = connection.cursor()
            Params = {
            	'FK_Goods': data['fk_goods'], 'TypeApp': data['typeApp'], 'SerialNumber': data['serialNumber'],
            	'DateReturn': data['datereturn'], 'Conditions': data['conditions'],
            	'FK_fromemployee': data['idapp_fromemployee'], 'FK_usedemployee': data['idapp_usedemployee'],
            	'IsCompleted': data['iscompleted'], 'MinusDesc': data['minus'], 'IsAccepted': data['isaccepted'],
            	'Descriptions': data['descriptions']
            }
            fk_stock = None
            with transaction.atomic():
                if statusForm == StatusForm.Input:
                    Params['CreatedDate'] = data['createddate']
                    Params['CreatedBy'] = data['createdby']
                    fromgoods = None
                    value_fromgoods = None
                    if data['fk_goods_outwards'] != 'NULL' and data['fk_goods_outwards'] != '':
                    	fromgoods = 'FK_goods_outwards'
                    	value_fromgoods = data['fk_goods_outwards']
                    elif data['fk_goods_lend'] != 'NULL' and data['fk_goods_lend'] != '':
                    	fromgoods = 'FK_goods_lend'
                    	value_fromgoods = data['fk_goods_lend']
                    Params[fromgoods] = value_fromgoods
                    Query = """INSERT INTO n_a_goods_return
                    (fk_goods,typeapp,serialnumber,datereturn,conditions,fk_fromemployee,fk_usedemployee,iscompleted,minusDesc,
                    isaccepted,descriptions,createddate,createdby,""" + fromgoods + ")"
                    Query += """VALUES({})""".format(','.join('%(' +
                    											i+')s' for i in Params))
                    cur.execute(Query, Params)

                    # cur.execute("""SELECT last_insert_id()""")
                    idapp = cur.lastrowid

                    Query = """INSERT INTO n_a_goods_history (FK_Goods, TypeApp, SerialNumber,FK_RETURN, CreatedDate, CreatedBy)
                    VALUES (%(FK_Goods)s,%(TypeApp)s, %(SerialNumber)s, %(FK_Return)s, %(CreatedDate)s, %(CreatedBy)s)"""
                    Params = {
                    	'FK_Goods': data['fk_goods'], 'TypeApp': data['typeApp'], 'SerialNumber': data['serialNumber'],
                    	'FK_Return': idapp, 'CreatedDate': data['createddate'], 'CreatedBy': data['createdby']
                    }
                    cur.execute(Query, Params)
                elif statusForm == StatusForm.Edit:
                    Params['ModifiedDate'] = data['modifieddate']
                    Params['ModifiedBy'] = data['modifiedby']
                    Params['IDApp'] = data['idapp']
                    Query = """UPDATE n_a_goods_return SET fk_goods=%(FK_Goods)s, typeapp=%(TypeApp)s, serialnumber=%(SerialNumber)s,
                    datereturn=%(DateReturn)s, conditions=%(Conditions)s, fk_fromemployee=%(FK_fromemployee)s, fk_usedemployee=%(FK_usedemployee)s,
                    iscompleted=%(IsCompleted)s,isaccepted=%(IsAccepted)s, minusDesc=%(MinusDesc)s, descriptions=%(Descriptions)s, modifieddate=%(ModifiedDate)s,
                    modifiedby=%(ModifiedBy)s WHERE idapp=%(IDApp)s"""
                    cur.execute(Query, Params)
                    Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
                    cur.execute(Query, {'FK_Goods': data['fk_goods']})
                    if data['fk_goods_lend'] != 'NULL' and data['fk_goods_lend'] != "":
                        Query = """UPDATE n_a_goods_lending SET DateReturn=%(DateReturn)s WHERE IDApp=%(FK_Goods_Lend)s """
                        Params = {'DateReturn': data['datereturn'], 'FK_Goods_Lend': data['fk_goods_lend']}
                        cur.execute(Query, Params)

                Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
                cur.execute(Query,{'FK_Goods': data['fk_goods']})
                row = []
                if cur.rowcount > 0:
                	row = cur.fetchone()
                	fk_stock = row[0]
                who = data['createdby'] if statusForm == StatusForm.Input else data['modifiedby']
                TStock =  commonFunct.getTotalGoods(data['fk_goods'],cur,who)
                TotalSpare = TStock[6]
                totalUsed = TStock[2]
                totalNew = TStock[0]
                totalRenew = TStock[4]
                totalReturn = TStock[3]
                totalReceived = TStock[1]
                totalMaintenance = TStock[5]
                #Update n_a_stock
                Query = """UPDATE n_a_stock SET T_Goods_Spare=%(T_Goods_Spare)s,TIsUsed=%(TIsUsed)s,TIsNew=%(TIsNew)s,TIsRenew=%(TIsRenew)s,TGoods_Return=%(TGoods_Return)s,
                		TGoods_Received=%(TGoods_Received)s,TMaintenance=%(TMaintenance)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s WHERE IDApp = %(fk_stock)s"""
                param = {'fk_stock':fk_stock,'T_Goods_Spare':TotalSpare,'TIsUsed':totalUsed,'TIsNew':totalNew,'TIsRenew':totalRenew,'TGoods_Return':totalReturn,
                		'TGoods_Received':totalReceived,'TMaintenance':totalMaintenance,'ModifiedBy':who}
                cur.execute(Query,param)
                cur.close()
                return (Data.Success,)
        except Exception as e:
        	return commonFunct.response_default((Data.Empty,e))
    def DeleteData(self, idapp,who):
        sn = super(NA_BR_Goods_Return, self).get_queryset().filter(idapp=idapp).values('serialnumber')[0]['serialnumber']
        hasref = super(NA_BR_Goods_Return, self).get_queryset().filter(Q(idapp__gt=idapp) & Q(serialnumber=sn)).exists()
        if hasref:
        	return(Data.HasRef,Message.HasRef_del.value)
        data = super(NA_BR_Goods_Return, self).get_queryset().filter(Q(idapp=idapp))# & (NAGoodsOutwards_set__serialnumber=sn) && (NAGoodsOutwards_set_datereleased))
        dateret = data.values('datereturn')
        dateret = dateret[0]['datereturn']
        serialNumber = data.values('serialnumber')
        serialNumber = serialNumber[0]['serialnumber']
        fk_goods = data.values('fk_goods')
        fk_goods = fk_goods[0]['fk_goods']
        hasref = super(NA_BR_Goods_Return, self).get_queryset().filter(idapp=idapp,return_goods_lost__fk_goods_return=idapp).exists()
        if hasref:
        	return (Data.HasRef, Message.HasRef_del.value)
        cur = connection.cursor()
        Query = """SELECT * FROM n_a_goods_outwards WHERE datereleased > %(DateReturned)s AND SerialNumber = %(SerialNumber)s"""
        cur.execute(Query,{'DateReturned':dateret,'SerialNumber':serialNumber})
        if cur.rowcount>0:
        	return (Data.HasRef, Message.HasRef_del.value)
        Query = """SELECT * FROM n_a_goods_lending WHERE IDApp > %(IDApp)s AND DateReturn > %(DateReturned)s AND SerialNumber = %(SerialNumber)s"""
        cur.execute(Query,{'DateReturned':dateret,'SerialNumber':serialNumber,'IDApp':idapp})
        if cur.rowcount>0:
        	return (Data.HasRef, Message.HasRef_del.value)
        fk_stock = fk_goods
        with transaction.atomic():
        	Query = """DELETE FROM n_a_goods_return WHERE idapp=%(IDApp)s"""
        	cur.execute(Query, {'IDApp': idapp})

        	Query = """DELETE FROM n_a_goods_history WHERE fk_goods = %s AND serialnumber = %s AND fk_return = %s"""
        	cur.execute(Query,[fk_goods,serialNumber,idapp])

        	TStock =  commonFunct.getTotalGoods(fk_goods,cur,who)
        	TotalSpare = TStock[6]
        	totalUsed = TStock[2]
        	totalNew = TStock[0]
        	totalRenew = TStock[4]
        	totalReturn = TStock[3]
        	totalReceived = TStock[1]
        	totalMaintenance = TStock[5]
        	#Update n_a_stock
        	Query = """UPDATE n_a_stock SET T_Goods_Spare=%(T_Goods_Spare)s,TIsUsed=%(TIsUsed)s,TIsNew=%(TIsNew)s,TIsRenew=%(TIsRenew)s,TGoods_Return=%(TGoods_Return)s,
        			TGoods_Received=%(TGoods_Received)s,TMaintenance=%(TMaintenance)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s WHERE IDApp = %(fk_stock)s"""
        	param = {'fk_stock':fk_stock,'T_Goods_Spare':TotalSpare,'TIsUsed':totalUsed,'TIsNew':totalNew,'TIsRenew':totalRenew,'TGoods_Return':totalReturn,
        			'TGoods_Received':totalReceived,'TMaintenance':totalMaintenance,'ModifiedBy':who}
        	cur.execute(Query, param)
        #print(connection.queries)
        cur.close()
        return 'success'

    def retrieveData(self, idapp):
        cur = connection.cursor()
        Query = """SELECT ngr.typeApp,ngr.serialNumber,ngr.fk_goods,ngr.datereturn,ngr.conditions,
		ngr.minusDesc AS minus, ngr.iscompleted,ngr.isaccepted,ngr.fk_goods_outwards AS idapp_fk_goods_outwards,
		ngr.fk_goods_lend AS idapp_fk_goods_outwards, ngr.descriptions,
		CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),' ',IFNULL(ngd.typeapp,'')) AS goods,g.itemcode,emp1.fromemployee,
		emp1.nik_fromemployee,emp1.idapp_fromemployee,emp2.usedemployee,emp2.nik_usedemployee,
		emp2.idapp_usedemployee FROM n_a_goods_return ngr INNER JOIN n_a_goods g ON ngr.fk_goods = g.idapp
		INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngr.serialnumber
		LEFT OUTER JOIN
		(SELECT idapp AS idapp_fromemployee,nik AS nik_fromemployee,employee_name AS fromemployee FROM employee)
		AS emp1 ON ngr.fk_fromemployee = emp1.idapp_fromemployee
		LEFT OUTER JOIN
		(SELECT idapp AS idapp_usedemployee, nik AS nik_usedemployee,employee_name AS usedemployee FROM employee)
		AS emp2 ON ngr.fk_usedemployee = emp2.idapp_usedemployee WHERE ngr.idapp = %(IDApp)s"""
        cur.execute(Query, {'IDApp': idapp})
        result = query.dictfetchall(cur)
        cur.close()
        return result[0]
    def getLastTrans(self,SerialNO):
        """function untuk mengambil terakhir transaksi data, sebagai umpan balik ke user, barang ini terakhir di pake oleh siapa / belum di pakai sama sekali
        param : SerialNO
        """
        #ambil data brand dan typenya
        Query = """SELECT g.idapp,g.itemcode,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS BrandName,ngd.typeapp FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App \
        			LEFT OUTER JOIN n_a_goods g ON g.IDApp = ngr.FK_Goods WHERE ngd.serialnumber = %s"""
        cur = connection.cursor()
        cur.execute(Query,[SerialNO])
        #idapp,fk_goods,goodsname,brandName,type,serialnumber,lastinfo,fk_outwards,fk_lending,fk_return,fk_maintenance,fk_disposal,fk_lost
        idapp_fk_goods = 0
        itemcode = ''
        goodsname = ''
        #typeapp = ''
        #brandname = ''
        serialnumber = ''
        lastInfo = 'unknown'
        idapp_usedemployee = 0;fklending = 0;fkoutwards = 0;fk_usedemployee = 'NIK';usedemployee = 'unknown';
        row = []
        if cur.rowcount > 0:
        	row = cur.fetchone()
        	typeapp = row[4]
        	brandname = row[3]
        	goodsname = row[2]
        	itemcode = row[1]
        	idapp_fk_goods = row[0]
        else:
        	cur.close()
        	raise Exception('no such data')
        Query = """SELECT EXISTS(SELECT serialnumber FROM n_a_goods_history WHERE serialnumber = %s)"""
        cur.execute(Query,[SerialNO])
        row = cur.fetchone()
        if int(row[0]) > 0:
        	Query = """SELECT FK_Lending,FK_Outwards FROM n_a_goods_history WHERE serialnumber = %s ORDER BY createddate DESC LIMIT 1 """
        	cur.execute(Query,[SerialNO])
        	row = cur.fetchone()
        	if cur.rowcount > 0:
        		if row[0] is not None:
        			fklending = row[0]
        			Query = """SELECT g.idapp AS fk_goods,g.itemcode,g.goodsname,emp.NIK AS nik_usedemployee,emp.employee_name AS usedemployee,emp.idapp AS idapp_usedemployee,
        						@idapp_fk_goods_outwards := null AS idapp_fk_goods_outwards, ngl.idapp AS idapp_fk_goods_lend
        						FROM n_a_goods_lending AS ngl INNER JOIN employee AS emp ON emp.IDApp = ngl.fk_employee INNER JOIN n_a_goods g ON ngl.fk_goods = g.IDApp WHERE ngl.IDApp = %(FK_Lending)s """
        			cur.execute(Query,{'FK_Lending':fklending})
        			row = cur.fetchone()
        			if cur.rowcount > 0 :
        				#fk_goods,goods,nik_usedemployee,|usedemployee,idapp_usedemployee,idapp_fk_goods_outwards,idapp_fk_goods_lend
        				itemcode = row[1]
        				goodsname = row[2]
        				fk_usedemployee = row[3]
        				usedemployee = row[4]
        				idapp_usedemployee = row[5]
        				fklending = row[7]
        		elif row[1] is not None:
        			fkoutwards =row[1]
        			Query = """SELECT g.idapp AS fk_goods,g.itemcode,g.goodsname,emp.NIK AS nik_usedemployee,emp.employee_name AS usedemployee,emp.idapp AS idapp_usedemployee,
        						ngo.idapp as idapp_fk_goods_outwards,@idapp_fk_goods_lend := null AS idapp_fk_goods_lend
        						FROM n_a_goods_outwards AS ngo INNER JOIN employee AS emp ON emp.IDApp = ngo.fk_employee INNER JOIN n_a_goods g ON ngo.fk_goods = g.IDApp
        						WHERE ngo.IDApp = %(FK_Outwards)s"""
        			cur.execute(Query,{'FK_Outwards':fkoutwards})
        			row = cur.fetchone()
        		#fk_goods,itemcode,goods,nik_usedemployee,nik_usedemployee,idapp_usedemployee,idapp_fk_goods_outwards,idapp_fk_goods_lend WHERE ngo.IDApp = %(FK_Outwards)s
        			itemcode = row[1]
        			goodsname = row[2]
        			fk_usedemployee = row[3]
        			usedemployee = row[4]
        			idapp_usedemployee = row[5]
        			fkoutwards = row[6]
        return (Data.Success,{'idapp_fk_goods':idapp_fk_goods,'itemcode':itemcode,'goodsname':goodsname,'typeapp':typeapp,'fk_usedemployee':fk_usedemployee,
        						 'usedemployee':usedemployee,'idapp_usedemployee':idapp_usedemployee,'fkoutwards':fkoutwards,'fklending':fklending})
    def SearchGoods_byForm(self, searchText,orderFields,sortIndice,pageSize,PageIndex,userName):
        Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Return_SG_" + userName
        cur = connection.cursor()
        cur.execute(Query)

        Query = "CREATE TEMPORARY TABLE Temp_T_Return_SG_" + userName  + """ ENGINE=MyISAM AS (
        SELECT * FROM (
        	SELECT ngo.idapp,CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName), ' ',IFNULL(ngd.typeapp,'')) AS goods,
        	ngo.fk_goods, ngo.serialnumber, g.itemcode, ngd.typeapp, @fromgoods := 'GO' AS fromgoods,emp.employee_name
        	FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngo.serialnumber
        	INNER JOIN employee AS emp ON emp.IDApp = ngo.FK_Employee WHERE CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),IFNULL(ngd.typeapp,''))
        	LIKE \'{q}\' OR g.itemcode LIKE \'{q}\' or ngo.serialnumber LIKE \'{q}\' OR emp.employee_name LIKE \'{q}\'
        	AND NOT EXISTS (SELECT idapp FROM n_a_goods_return WHERE fk_goods_outwards = ngo.idapp)
        	UNION \n
        	SELECT ngl.idapp,CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),IFNULL(ngd.typeapp,'')) AS goods,
        	ngl.fk_goods, ngl.serialnumber, g.itemcode, ngd.typeapp, @fromgoods := 'GL' AS
        	fromgoods,emp.employee_name FROM n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngl.serialnumber
        	INNER JOIN employee AS emp on emp.IDApp = ngl.FK_Employee WHERE CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),IFNULL(ngd.typeapp,''))
        	LIKE \'{q}\' OR g.itemcode LIKE \'{q}\' or ngl.serialnumber LIKE \'{q}\' OR emp.employee_name LIKE \'{q}\'
        	AND NOT EXISTS (SELECT idapp FROM n_a_goods_return WHERE fk_goods_lend = ngl.idapp)
        	)C
        )
        """.format(
        q=('%' + searchText + '%')
        )
        cur.execute(Query)
        strLimit = '20'
        if int(PageIndex) <= 1:
        	strLimit = '0'
        else:
        	strLimit = str((int(PageIndex)-1) * int(pageSize))
        if orderFields == '':
        	Query  = "SELECT * FROM Temp_T_Return_SG_" + userName + " ORDER BY goods " + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
        else:
        	Query  = "SELECT * FROM Temp_T_Return_SG_" + userName + " ORDER BY " + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
        cur.execute(Query)
        result = query.dictfetchall(cur)

        Query = "SELECT COUNT(*) FROM Temp_T_Return_SG_" + userName
        cur.execute(Query)
        row = cur.fetchone()
        totalRecords = row[0]


        Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Return_SG_" + userName
        cur.execute(Query)
        cur.close()
        return (result,totalRecords)
    def getGoods_data(self, idapp, fromgoods):
        cur = connection.cursor()
        if fromgoods == 'GO':
        	Query = """SELECT ngo.idapp,CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),' ',IFNULL(ngd.typeapp,'')) AS goods, ngo.serialnumber,g.itemcode,
        	@fromgoods := 'GO' AS fromgoods,emp1.idapp_used_by,emp1.used_by,emp1.nik_used_by FROM n_a_goods_outwards ngo
        	INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngo.serialnumber LEFT OUTER JOIN (SELECT idapp AS idapp_used_by,nik AS nik_used_by,
        	employee_name AS used_by FROM employee) AS emp1 ON ngo.fk_employee = emp1.idapp_used_by WHERE
        	ngo.idapp = %(IDApp)s"""
        elif fromgoods == 'GL':
        	Query = """SELECT ngl.idapp,CONCAT(g.goodsname,' ',IFNULL(ngd.BrandName,g.BrandName),IFNULL(ngd.typeapp,'')) AS goods, ngl.serialnumber,g.itemcode,
        	@fromgoods := 'GL' AS fromgoods,emp1.idapp_used_by,emp1.used_by,emp1.nik_used_by FROM n_a_goods_lending ngl
        	INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN n_a_goods_receive_detail ngd ON ngd.serialnumber = ngl.serialnumber LEFT OUTER JOIN (SELECT idapp AS idapp_used_by,nik AS nik_used_by,
        	employee_name AS used_by FROM employee) AS emp1 ON ngl.fk_employee = emp1.idapp_used_by WHERE
        	ngl.idapp = %(IDApp)s"""
        cur.execute(Query, {'IDApp': idapp})
        result = query.dictfetchall(cur)
        cur.close()
        return (Data.Success, result)
def dataExists(self, **kwargs):
	idapp = kwargs.get('idapp')
	if idapp is not None:
		return super(NA_BR_Goods_Return, self).get_queryset().filter(idapp=idapp).exists()
	serialnumber = kwargs.get('serialnumber')
