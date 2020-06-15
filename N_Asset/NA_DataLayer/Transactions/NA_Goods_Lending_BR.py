from django.db import models
from NA_DataLayer.common import *
from django.db import transaction;
from django.db import connection
from decimal import Decimal
from django.db.models import Q
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
class NA_BR_Goods_Lending(models.Manager):
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		colKey = ''
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		if columnKey == 'goods':
			colKey = 'g.goodsname'
		elif columnKey == 'goodstype':
			colKey = 'ngd.TypeApp'
		elif columnKey == 'serialnumber':
			colKey = 'ngd.serialnumber'
		elif columnKey == 'lentby':
			colKey = 'L.lentby'
		elif columnKey == 'sentby':
			colKey = 'S.sentby'
		elif columnKey == 'lentdate':
			colKey = 'ngl.DateLending'
		elif columnKey == 'interests':
			colKey = 'ngl.interests'
		elif columnKey == 'responsibleby':
			colKey = 'R.responsibleby'
		elif columnKey == 'refgoodsfrom':
			colKey = 'Ref.refgoodsfrom'
		elif columnKey == 'isnew':
			colKey = 'ngl.isnew'
		elif columnKey == 'status':
			colKey = 'ngl.status'
		elif columnKey == 'createdby':
			colKey = 'ngl.createdby'
		elif columnKey == 'descriptions':
			colKey = 'ngl.descriptions'			
		elif columnKey == 'createddate':
			colKey = 'ngl.createddate'
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Lending_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query = """ CREATE TEMPORARY TABLE T_Lending_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT ngl.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,L.lentby,S.sentby,ngl.DateLending AS lentdate,ngl.DateReturn as datereturn,ngl.interests,R.responsibleby,
					Ref.refgoodsfrom,ngl.isnew,ngl.status, ngl.descriptions,ngl.createdby,ngl.createddate
					FROM n_a_goods g INNER JOIN n_a_goods_lending ngl ON G.IDApp = ngl.FK_Goods
					INNER JOIN (SELECT ngl.IDApp,CASE
						WHEN (ngl.FK_Receive IS NOT NULL) THEN 'Receive PR (New)'
						WHEN (ngl.FK_RETURN IS NOT NULL) THEN 'RETURN Eks Employee'
						WHEN (ngl.FK_Maintenance IS NOT NULL) THEN 'Service(Maintenance)'
						WHEN (ngl.FK_CurrentApp IS NOT NULL) THEN 'RETURN (After being Lent)'
						ELSE 'Other (Uncategorized)'
					END AS refgoodsfrom FROM n_a_goods_lending ngl)Ref ON Ref.IDApp = ngl.IDApp
					INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = g.IDApp
					INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
					AND ngl.SerialNumber = ngd.SerialNumber AND ngl.TypeApp = ngd.TypeApp
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS lentby FROM employee)L
										ON L.IDApp = ngl.FK_Employee
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS sentby FROM employee)S
										ON S.IDApp = ngl.FK_Sender
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS responsibleby FROM employee)R
					ON R.IDApp = ngl.FK_ResponsiblePerson WHERE """ + colKey + rs.Sql() + ")"
		cur.execute(Query)
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		if orderFields != '':
			#Query = """SELECT * FROM T_Receive_Manager """ + (("ORDER BY " + ",".join(orderFields)) if len(orderFields) > 1 else " ORDER BY " + orderFields[0]) + (" DESC" if sortIndice == "" else sortIndice) + " LIMIT " + str(pageSize*(0 if PageIndex <= 1 else PageIndex)) + "," + str(pageSize)
			Query = """SELECT * FROM T_Lending_Manager_""" + userName + """ ORDER BY """ + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
		else:			
			Query = """SELECT * FROM T_Lending_Manager_""" + userName + """ ORDER BY IDApp LIMIT """ + strLimit + "," + str(pageSize)
		cur.execute(Query)
		result = query.dictfetchall(cur)
		#get countRows
		Query = """SELECT COUNT(*) FROM T_Lending_Manager_""" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]
		cur.close()
		return (result,totalRecords)

	def UpdateStatus(self,idapp,newVal,UpdatedBy):		
		cur = connection.cursor()			
		with transaction.atomic():
			Query = """SELECT FK_Goods FROM n_a_goods_lending WHERE idapp = %(idapp)s LIMIT 1 """
			cur.execute(Query,{'idapp':idapp})
			row = cur.fetchone()
			FKGoods = int(row[0])

			if newVal == "R":
				Query = """UPDATE n_a_goods_lending SET status = %(newVal)s, datereturn = NOW() WHERE idapp = %(idapp)s """
			else:
				Query = """UPDATE n_a_goods_lending SET status = %(newVal)s, datereturn = NULL WHERE idapp = %(idapp)s """
			cur.execute(Query,{'newVal':newVal,'idapp':idapp})				

			Query = """SELECT COUNT(FK_goods) FROM (SELECT DISTINCT nl.FK_goods,nl.TypeApp,nl.SerialNumber FROM n_a_goods_lending nl WHERE nl.Status = 'R' 
			AND NOT EXISTS(SELECT FK_Goods FROM n_a_maintenance WHERE SerialNumber = nl.SerialNumber AND IsFinished = 0) 
			AND NOT EXISTS(SELECT FK_Goods FROM n_a_goods_outwards WHERE FK_Lending = nl.IDApp) 
			AND NOT EXISTS(SELECT FK_Goods FROM n_a_disposal WHERE SerialNumber = nl.SerialNumber) AND nl.FK_Goods =  %(FK_Goods)s)C """ 
			cur.execute(Query,{'FK_Goods':FKGoods})
			TotalSpare = 0
			if cur.rowcount >0:
				row = cur.fetchone()
				TotalSpare = int(row[0])
				#update langsung Stock

			Query = """UPDATE n_a_stock SET T_Goods_Spare = %(TotalSpare)s,Modifiedby = %(UpdatedBy)s, ModifiedDate = NOW() WHERE FK_Goods = %(FK_Goods)s"""
			cur.execute(Query,{'TotalSpare':TotalSpare,'UpdatedBy':UpdatedBy,'FK_Goods':FKGoods})
			return 'success'
	def getInterest(self,SearchIntr):
		return super(NA_BR_Goods_Lending,self).get_queryset().filter(interests__istartswith=SearchIntr).values('interests').distinct()
	
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
		idapp = 0
		itemcode = ''		
		goodsname = ''
		typeapp = ''
		brandname = ''
		serialnumber = ''
		lastInfo = 'unknown'
		fkreceive = 0;fkreturn = 0;fklending = 0;fkoutwards = 0;fkmaintenance = 0;fkdisposal=0;fklost=0;		
		row = []
		if cur.rowcount > 0:
			row = cur.fetchone()
			typeapp = row[4]
			brandname = row[3]
			goodsname = row[2]
			itemcode = row[1]
			idapp = row[0]
		else:
			cur.close()
			raise Exception('no such data')
		#cek apakah sudah ada transaksi untuk barang dengan serial number tsb
		Query = """SELECT EXISTS(SELECT serialnumber FROM n_a_goods_history WHERE serialnumber = %s)"""
		cur.execute(Query,[SerialNO])
		row = cur.fetchone()
		
		if int(row[0]) > 0:
			#jika ada ambil data transaksi terakhir yang mana transaksi ada 4 kelompok,lending,outwards,return,maintenance,disposal
			Query = """SELECT FK_Lending,FK_Outwards,FK_RETURN,FK_Maintenance,FK_Disposal,fk_lost FROM n_a_goods_history WHERE serialnumber = %s ORDER BY createddate DESC LIMIT 1 """
			cur.execute(Query,[SerialNO])
			row = cur.fetchone()
			if cur.rowcount > 0:
				if row[0] is not None:
					fklending = row[0]
				if row[1] is not None:
					fkoutwards =row[1]
				if row[2] is not None:
					fkreturn = row[2]
				if row[3] is not None:
					fkmaintenance = row[3]
				if row[4] is not None:
					fkdisposal = row[4]
				if row[5] is not None:
					fklost = row[5]
			if int(fklending)>0:
				Query = """SELECT e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.NIK = ngl.FK_Employee
							WHERE ngl.IDApp = %s"""
				cur.execute(Query,[fklending])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date lent ' + parse(str(row[1])).strftime('%d %B %Y') + ', interests ' + str(row[2])
			elif int(fkoutwards) > 0:
				Query = """SELECT e.employee_name,ngo.datereleased,ngl.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.NIK = ngo.FK_Employee
							WHERE ngo.IDApp = %s"""
				cur.execute(Query,[fkoutwards])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date released ' + parse(str(row[1])).strftime('%d %B %Y') + ', ' + str(row[2]) + ' (goods is still in use)'
			elif int(fkreturn) > 0:
				Query = """SELECT e.employee_name,ngt.datereturn,ngt.descriptions FROM n_a_goods_return ngt INNER JOIN employee e ON e.NIK = ngt.FK_FromEmployee
							WHERE ngt.IDApp = %s"""
				cur.execute(Query,[fkreturn])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date returned ' + parse(str(row[1])).strftime('%d %B %Y') + ', ' + str(row[2]) + ' (goods is already returned)'
			elif int(fkmaintenance) > 0:
				Query = """SELECT CONCAT(IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,'')) as maintenanceby,StartDate,EndDate, IsFinished,IsSucced FROM n_a_maintenance WHERE IDApp  = %s"""
				cur.execute(Query,[fkmaintenance])
				if cur.rowcount > 0:
					row = cur.fetchone()
					isFinished = False;isSucced = False;starDate = datetime.now();endDate = datetime.now()
					if row[3] is not None:
						isFinished = strtobool(row[3])
					if row[4] is not None:
						isSucced = strtobool(row[4])
					if row[1] is not None:
						starDate =  parse(str(row[1])).strftime('%d %B %Y')
					if row[2] is not None:
						endDate =  parse(str(row[2])).strftime('%d %B %Y')
					if isFinished and isSucced:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + endDate + ', ' +  ' (goods is able to use)'
					elif isFinished == True and isSucced == False:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + endDate + ', ' +  ' (goods is unable to use )'
					elif not isFinished:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' +starDate + ', ' +  ' (goods is still in maintenance)'
			elif int(fkdisposal) > 0:
				Query = """SELECT Descriptions FROM n_a_disposal WHERE IDApp = %s"""
				cur.execute(Query,[fkdisposal])
				lastInfo = "goods is not able to use again " 
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = "goods is not able to use again " +  row[0]
			elif int(fklost) > 0:
				Query = """SELECT fk_goods_lending,fk_goods_outwards,fk_maintenance,Reason,status FROM n_a_goods_lost WHERE idapp = %s"""
				cur.execute(Query,[fklost])
				lastInfo = "goods has lost "
				if cur.rowcount > 0:
					row = cur.fetchone()
					fk_lost_lending = 0;fk_lost_outwards = 0;fk_lost_maintenance = 0;
					if row[0] is not None:
						fk_lost_lending = row[0]
					if  row[1] is not None:
						fk_lost_outwards = row[1]
					if row[2] is not None:
						fk_lost_maintenance = row[2]
					reason = row[3]
					lost_status = row[4]
					if lost_status == "F":
						if int(fk_lost_lending) > 0:
							Query = """SELECT e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.NIK = ngl.FK_Employee
									WHERE ngl.IDApp = %s"""
							cur.execute(Query,[fk_lost_lending])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + ', date lent ' + parse(str(row[1])).strftime('%d %B %Y') + ', interests ' + str(row[2])
						elif int(fk_lost_outwards) > 0:
							Query = """SELECT e.employee_name,ngo.datereleased,ngl.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.NIK = ngo.FK_Employee
									WHERE ngo.IDApp = %s"""
							cur.execute(Query,[fkoutwards])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + ', date released ' + parse(str(row[1])).strftime('%d %B %Y') + ', ' + str(row[2]) + ' (goods is still in use)'
						elif int(fk_lost_maintenance) > 0:
							Query = """SELECT CONCAT(IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,'')) as maintenanceby,StartDate,EndDate, IsFinished,IsSucced FROM n_a_maintenance WHERE IDApp  = %s"""
							cur.execute(Query,[fkmaintenance])
							if cur.rowcount > 0:
								row = cur.fetchone()
								isFinished = False;isSucced = False;starDate = datetime.now();endDate = datetime.now()
								if row[3] is not None:
									isFinished = strtobool(row[3])
									if row[4] is not None:
										isSucced = strtobool(row[4])
								if row[1] is not None:
									starDate =  parse(str(row[1])).strftime('%d %B %Y')
								if row[2] is not None:
									endDate =  parse(str(row[2])).strftime('%d %B %Y')
							if isFinished and isSucced:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + endDate + ', ' +  ' (goods is able to use)'
							elif isFinished == True and isSucced == False:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + endDate + ', ' +  ' (goods is unable to use )'
							elif not isFinished:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' + starDate + ', ' +  ' (goods is still in maintenance)'
						#elif fk_lost_outwards
						else:
							lastInfo = "goods has lost, but has been found "
		else:
			Query = """SELECT ngl.idapp as fk_receive,ngl.brandname,ngl.typeapp,ngr.datereceived FROM n_a_goods_receive_detail ngl INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngl.FK_App WHERE ngl.serialnumber = %s"""
			cur.execute(Query,[SerialNO])
			row = []
			if cur.rowcount > 0:
				row = cur.fetchone()
				fkreceive = row[0]
				typeapp = row[2]
				brandname = row[1]

			else:
				raise Exception('no such data')
			dt = datetime.date(row[3])
			lastInfo = 'goods is new, date received ' + dt.strftime('%d %B %Y')
		cur.close()
		#idapp,fk_goods,goodsname,brandName,type,serialnumber,lastinfo,fk_outwards,fk_lending,fk_return,fk_maintenance,fk_disposal,fk_lost
		return(idapp,itemcode,goodsname,brandname,typeapp,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance)
	def hasExists(self,idapp_fk_goods,serialnumber,datelent):
		#An error occurred: FieldError('Related Field got invalid lookup: iexact',)
		return super(NA_BR_Goods_Lending,self).get_queryset().filter(Q(fk_goods=idapp_fk_goods) & Q(serialnumber=serialnumber) & Q(datelending=datelent)).exists()#Q(member=p1) | Q(member=p2)
	def getBrandForLending(self,searchText,orderFields,sortIndice,pageSize,PageIndex,userName):
		#get item from goods received
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Receive_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_History_" + userName		
		cur.execute(Query)
		
		#Query new items
		Query = "CREATE TEMPORARY TABLE Temp_T_Receive_" + userName  + """ ENGINE=MyISAM AS (SELECT g.idapp,g.itemcode as fk_goods,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS brandname,ngd.typeapp AS type,ngd.serialnumber, 'not yet used' as lastinfo,ngd.idapp as fk_receive, \
					0 AS fk_outwards,0 as fk_lending,0 AS fk_return,0 AS fk_maintenance,0 AS fk_disposal,0 AS fk_lost FROM n_a_goods g INNER JOIN n_a_goods_receive ngr ON ngr.fk_goods = g.IDApp INNER JOIN n_a_goods_receive_detail ngd ON ngr.IDApp = ngd.FK_App \
					WHERE NOT EXISTS(SELECT IDApp FROM n_a_goods_history WHERE fk_goods = ngr.fk_goods AND serialnumber = ngd.serialnumber)) """
		cur.execute(Query)
	    # Query get last trans in history 		
		Query = "CREATE TEMPORARY TABLE Temp_T_History_" + userName  + """ ENGINE=MyISAM AS (SELECT gh.idapp,gh.fk_goods,gh.goodsname,gh.brandname,gh.type,gh.serialnumber, \
					CASE \
						WHEN (gh.fk_maintenance IS NOT NULL) THEN (SELECT CONCAT('Maintenance by ', IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,''), \
							(CASE \
								WHEN (isfinished = 1 AND issucced = 1) THEN (CONCAT(' Date Returned  ',DATE_FORMAT(enddate,'%d %B %Y'),' (goods is able to use)')) \
								WHEN (isfinished = 1 AND issucced = 0) THEN (CONCAT(' Date Returned ',DATE_FORMAT(enddate,'%d %B %Y'),' (goods is unable to use)')) \
								WHEN (isfinished = 0) THEN (CONCAT(' Date maintenance ',DATE_FORMAT(enddate,'%d %B %Y'),' (goods is still in maintenance)')) \
								END)) FROM n_a_maintenance WHERE IDApp = gh.fk_maintenance) \
						WHEN(gh.fk_lending IS NOT NULL) THEN((CASE \
																WHEN ((SELECT `status` FROM n_a_goods_lending WHERE idapp = gh.fk_lending) = 'L') THEN 'good is still lent' \
																ELSE ('goods is able to use') \
																END)) \
						WHEN(gh.fk_outwards IS NOT NULL) THEN 'goods is still in use by other employee' \
						WHEN (gh.fk_return IS NOT NULL) THEN 'goods is able to use' \
						WHEN (gh.fk_disposal IS NOT NULL) THEN 'goods is unabled to use(been disposed,auction,broken,etc)' \
						WHEN (gh.fk_lost IS NOT NULL) THEN 'goods has lost' \
						ELSE 'Unknown or uncategorized last goods position' \
						END AS lastinfo,gh.fk_receive,gh.fk_outwards,gh.fk_lending,gh.fk_return,gh.fk_maintenance,gh.fk_disposal,gh.fk_lost  \
						FROM(			\
							SELECT g.idapp,g.itemcode as  fk_goods,g.goodsname,IFNULL(ngd.brandName,g.brandName) AS brandName,ngd.typeapp as 'type',ngd.serialnumber,ngd.idapp AS fk_receive,ngh.fk_outwards,ngh.fk_lending, \
							ngh.fk_return,ngh.fk_maintenance,ngh.fk_disposal,ngh.fk_lost FROM \
							n_a_goods g INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail ngd ON ngd.fk_app = ngr.idapp \
							INNER JOIN n_a_goods_history ngh ON ngh.fk_goods = g.idapp AND ngh.serialnumber = ngd.serialnumber \
							WHERE ngh.createddate = (SELECT Max(CreatedDate) FROM n_a_goods_history WHERE fk_goods = g.idapp AND serialnumber = ngd.serialnumber))gh)				
				"""
		cur.execute(Query)
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		#gabungkan jadi satu
		Query = "CREATE TEMPORARY TABLE Temp_F_" + userName + """ ENGINE=MyISAM AS (SELECT * FROM \
				(SELECT * FROM Temp_T_Receive_""" + userName + """ \
					UNION \
				 SELECT * FROM Temp_T_History_""" + userName + """\
				 )C WHERE (goodsname LIKE %s OR brandname LIKE %s) OR (serialnumber = %s))"""
		cur.execute(Query,['%'+searchText+'%','%'+searchText+'%',searchText])
		if orderFields == '':
			Query  = "SELECT * FROM Temp_F_" + userName + " ORDER BY brandname " + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)	
		else:
			Query  = "SELECT * FROM Temp_F_" + userName + " ORDER BY " + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)				
		cur.execute(Query)
		result = query.dictfetchall(cur)

		Query = "SELECT COUNT(*) FROM Temp_F_" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]
		cur.close()
		return (result,totalRecords)
	def SaveData(self,Data,Status=StatusForm.Input):
		cur = connection.cursor()
		#get FK_stock
		Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
		cur.execute(Query,{'FK_Goods':Data['idapp_fk_goods']})
		row = []
		if cur.rowcount > 0:
			row = cur.fetchone()
			fk_stock = row[0]
		try:
			with transaction.atomic():
				if Status == StatusForm.Input:
					Query = """INSERT INTO n_a_goods_lending(FK_Goods, IsNew, FK_Employee, DateLending, FK_Stock, FK_ResponsiblePerson, interests, FK_Sender, Status, CreatedDate, CreatedBy, SerialNumber, TypeApp, FK_Maintenance, Descriptions,lastinfo, FK_Receive, FK_RETURN, FK_CurrentApp) \
								VALUES (%(FK_Goods)s, %(IsNew)s, %(FK_Employee)s, %(DateLending)s, %(FK_Stock)s, %(FK_ResponsiblePerson)s, %(interests)s, %(FK_Sender)s, %(Status)s, NOW(), %(CreatedBy)s, %(SerialNumber)s, %(TypeApp)s, %(FK_Maintenance)s, %(Descriptions)s, %(lastinfo)s,%(FK_Receive)s, %(FK_RETURN)s, %(FK_CurrentApp)s)"""
					param = {'FK_Goods':Data['idapp_fk_goods'],'IsNew':Data['isnew'],'FK_Employee':Data['idapp_fk_employee'],'DateLending':Data['datelending'],'FK_Stock':fk_stock,'FK_ResponsiblePerson':Data['idapp_fk_responsibleperson'],'interests':Data['interests'],
							'FK_Sender':Data['idapp_fk_sender'],'Status':Data['statuslent'],'CreatedBy':Data['createdby'],'SerialNumber':Data['serialnumber'],'TypeApp':Data['typeapp'],'FK_Maintenance':Data['fk_maintenance'],'Descriptions':Data['descriptions'],
							'lastinfo':Data['lastinfo'],'FK_Receive':Data['fk_receive'],
							'FK_RETURN':Data['fk_return'],'FK_CurrentApp':Data['fk_currentapp'],}
					cur.execute(Query,param)
					cur.execute('SELECT last_insert_id()')
					row = cur.fetchone()
					FKApp = row[0]

					#insert n_goods_history
					Query = """INSERT INTO n_a_goods_history(FK_Goods, TypeApp, SerialNumber, FK_Lending, FK_Outwards, FK_RETURN, FK_Maintenance, FK_Disposal, FK_LOST, CreatedDate, CreatedBy) \
							 VALUES (%(FK_Goods)s,%(TypeApp)s, %(SerialNumber)s, %(FK_Lending)s,NULL, NULL, NULL, NULL, NULL, NOW(), %(CreatedBy)s )"""
					param = {'FK_Goods':Data['idapp_fk_goods'],'TypeApp':Data['typeapp'],'SerialNumber':Data['serialnumber'],'FK_Lending':FKApp,'CreatedBy':Data['createdby']}
				elif Status == StatusForm.Edit:
					Query = """ UPDATE n_a_goods_lending SET FK_Employee=%(FK_Employee)s,DateLending=%(DateLending)s,FK_ResponsiblePerson=%(FK_ResponsiblePerson)s, \
								interests=%(interests)s,FK_Sender=%(FK_Sender)s,Status=%(Status)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s,Descriptions=%(Descriptions)s \
								WHERE idapp = %(idapp)s """
					param = {'idapp':Data['idapp'],'FK_Goods':Data['idapp_fk_goods'],'FK_Employee':Data['idapp_fk_employee'],'DateLending':Data['datelending'],'FK_ResponsiblePerson':Data['idapp_fk_responsibleperson'],'interests':Data['interests'],
							'FK_Sender':Data['idapp_fk_sender'],'Status':Data['statuslent'],'ModifiedBy':Data['modifiedby'],'Descriptions':Data['descriptions']}
				cur.execute(Query,param)

				#Update Stock
				who = Data['createdby'] if Status == StatusForm.Input else Data['modifiedby']
				Stock = commonFunct.getTotalGoods(Data['idapp_fk_goods'],cur,who)
				TNew = Stock[0]
				TSpare = Stock[6]
				if fk_stock > 0:
					if strtobool(str(Data['isnew'])) == 1:#jika ngambil dari barang baru, kurangi tisnew di stock
						Query = """UPDATE n_a_stock SET T_Goods_Spare=%s,TIsNew = %s, ModifiedBy=%s,ModifiedDate = NOW() WHERE IDApp = %s """
						cur.execute(Query,[TSpare,TNew,who,fk_stock])
					else:
						Query = """UPDATE n_a_stock SET T_Goods_Spare=%s,ModifiedBy=%s,ModifiedDate = NOW() WHERE IDApp = %s """
						cur.execute(Query,[TSpare,who,fk_stock])
				return 'success'

		except Exception as e :
			cur.close()
			return repr(e)
	def HasReference(self,IDApp):
		cur = connection.cursor()
		Query = """SELECT EXISTS(SELECT IDApp FROM n_a_goods_lost WHERE FK_Goods_Lending = %s)"""
		cur.execute(Query,[IDApp])
		row = cur.fetchone()
		if cur.rowcount > 1:
			return int(row[0]) > 1
		else:
			return False
	def Delete(self,idapp,username):
		cur = connection.cursor()
		Query = """SELECT ns.IDApp,ngl.fk_goods,ngl.serialnumber,ngl.fk_receive FROM n_a_stock ns INNER JOIN n_a_goods_lending ngl ON ngl.fk_goods = ns.fk_goods WHERE ngl.IDApp = %s LIMIT 1"""
		cur.execute(Query,[idapp])

		if cur.rowcount > 0:
			row = cur.fetchone()
			fk_stock = row[0]
			fk_goods = row[1]
			serialnumber = row[2]
			fk_receive = row[3]
			with transaction.atomic():
				Query = """DELETE FROM n_a_goods_lending WHERE idapp = %s"""
				cur.execute(Query,[idapp])
				Query = """DELETE FROM n_a_goods_history WHERE fk_goods = %s AND serialnumber = %s AND fk_lending = %s"""
				cur.execute(Query,[fk_goods,serialnumber,idapp])
				if fk_receive is not None:
					#barang berarti  ngambil dari 
					Query = """UPDATE n_a_stock SET TIsNew = TIsNew + 1, ModifiedBy = %s,ModifiedDate = NOW() WHERE IDApp = %s """
					cur.execute(Query,[username,fk_stock]) 
			return "success"
	def getData(self,idapp):
		cur = connection.cursor()
		#/idapp, fk_goods, isnew, goods, idapp_fk_goods, fk_employee, idapp_fk_employee, fk_employee_employee
		#    //datelending, fk_stock, fk_responsibleperson, idapp_fk_responsibleperson, fk_responsibleperson_employee,
		#    //interests, fk_sender, idapp_fk_sender, fk_sender_employee, statuslent, descriptions, typeapp, serialnumber,
		#    //brandvalue, fk_maintenance, fk_return, fk_currentapp, fk_receive, fk_disposal, fk_lost, lastinfo, initializeForm, hasRefData
		Query = """SELECT g.itemcode AS fk_goods,ngl.isnew,g.goodsname AS goods,ngl.fk_goods AS idapp_fk_goods,emp.NIK AS fk_employee,\
					ngl.fk_employee AS idapp_fk_employee,		emp.employee_name AS fk_employee_employee,ngl.datelending,ngl.fk_stock,\
					emp1.NIK AS fk_responsibleperson, ngl.FK_ResponsiblePerson AS idapp_fk_responsibleperson,ngl.interests,IFNULL(ngl.lastinfo,'not yet used') AS lastinfo, \
					emp2.NIK AS fk_sender,ngl.fk_sender AS idapp_fk_sender,emp2.employee_name AS fk_sender_employee,ngl.status AS statuslent, \
					ngl.descriptions,ngl.typeapp,ngl.serialnumber, 		emp1.employee_name AS fk_responsibleperson_employee,g.brandname AS brandvalue, \
					IFNULL(ngl.fk_maintenance,0)AS fk_maintenance,IFNULL(ngl.fk_return,0) AS fk_return, \
					IFNULL(ngl.fk_currentapp,0) AS fk_currentapp,IFNULL(fk_receive,0) AS fk_receive, \
						CASE WHEN EXISTS(SELECT fk_goods FROM n_a_disposal WHERE fk_goods = ngl.fk_goods AND serialnumber = ngl.serialnumber) THEN 1 
							WHEN EXISTS(SELECT fk_goods FROM n_a_goods_lost WHERE FK_Goods_Lending = ngl.idapp) THEN 1 
							 ELSE 0 
					END AS hasRefData  
					FROM n_a_goods g INNER JOIN n_a_goods_lending ngl ON ngl.fk_goods = g.IDApp \
					INNER JOIN employee emp ON emp.IDApp = ngl.fk_employee 	\
					LEFT OUTER JOIN (SELECT IDApp, NIK,employee_name FROM employee)emp1 ON emp1.IDApp = ngl.fk_sender	\
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp2 ON emp2.IDApp = ngl.FK_ResponsiblePerson WHERE ngl.idapp = %s""" 
		cur.execute(Query,[idapp])
		data = query.dictfetchall(cur)

		Query = """SELECT EXISTS(SELECT IDApp  FROM n_a_goods_lending WHERE fk_currentapp = %s) 
					OR EXISTS(SELECT IDApp FROM n_a_goods_lost WHERE FK_Goods_Lending = %s) """
		cur.execute(Query,[idapp,idapp])
		row = cur.fetchone()
		if row[0] > 0:
			data[0]['hasRefData'] = True
		isnew =  commonFunct.str2bool(str(data[0]['isnew']))
		data[0]['isnew'] = isnew
		cur.close()

		return data

	def getDatabySN(self, sn):
		return super(NA_BR_Goods_Lending, self).get_queryset() \
			.filter(serialnumber__iexact=sn).order_by('-datereturn')[:1].get()






	

