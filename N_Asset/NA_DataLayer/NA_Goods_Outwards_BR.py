from django.db import models
from NA_DataLayer.common import *
from django.db import transaction;
from django.db import connection
from decimal import Decimal
from django.db.models import Q
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
class NA_BR_Goods_Outwards(models.Manager):
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		colKey = ''
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		if columnKey == 'goods':
			colKey = 'g.goodsname'
		elif columnKey == 'goodstype':
			colKey = 'ngd.TypeApp'
		elif columnKey == 'serialnumber':
			colkey = 'ngd.serialnumber'
		elif columnKey == 'daterequest':
			colkey = 'nga.daterequest'
		elif columnKey == 'datereleased':
			colkey = 'nga.datereleased'
		elif columnKey == 'isnew':
			colkey = 'nga.isnew'
		elif columnKey == 'for_employee':
			colkey = 'e.employee_name'
		elif columnKey == 'responsible_by':
			colkey = 'emp1.responsible_by'
		elif columnKey == 'senderby':
			colkey = 'emp2.senderby'
		elif columnKey == 'refgoodsfrom':
			colkey = 'ref.refgoodsfrom'
		elif columnKey == 'createdby':
			colkey = 'nga.createdby'
		elif columnKey == 'createddate':
			colkey = 'nga.ceateddate'
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Outwards_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query = """  CREATE TEMPORARY TABLE T_Outwards_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT nga.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,nga.daterequest,nga.datereleased,
		        nga.isnew,nga.fk_employee,e.employee_name as for_employee,nga.fk_usedemployee,
		        CASE 
			        WHEN(nga.fk_usedemployee IS NOT NUll) THEN(SELECT employee_name FROM `employee` WHERE idapp = nga.fk_usedemployee LIMIT 1)
			        END AS eks_employee,nga.fk_responsibleperson,emp1.responsible_by,nga.fk_sender,emp2.senderby,nga.fk_stock,
		        ref.refgoodsfrom,nga.createdby,nga.createddate,nga.descriptions
		        FROM n_a_goods_outwards nga INNER JOIN n_a_goods g ON g.IDApp = nga.FK_Goods 
		        INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = nga.FK_Goods
		        INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
		        AND nga.SerialNumber = ngd.SerialNumber
		        INNER JOIN (SELECT ng.IDApp,CASE
								        WHEN (ng.FK_Receive IS NOT NULL) THEN 'Receive PR (New)'
								        WHEN (ng.FK_RETURN IS NOT NULL) THEN 'RETURN Eks Employee'
								        WHEN (ng.FK_FromMaintenance IS NOT NULL) THEN 'After Service(Maintenance)'
								        WHEN (ng.FK_Lending IS NOT NULL) THEN 'RETURN (After being Lent)'
								        ELSE 'Other (Uncategorized)'
								        END AS refgoodsfrom FROM n_a_goods_Outwards ng)ref ON Ref.IDApp = nga.IDApp
			        INNER JOIN employee e on e.IDApp = nga.FK_Employee
			        LEFT OUTER JOIN (SELECT idapp,employee_name AS responsible_by FROM employee) emp1 ON emp1.idapp = nga.FK_ResponsiblePerson
			        LEFT OUTER JOIN (SELECT idapp,employee_name AS senderby FROM employee) emp2 ON emp2.idapp = nga.FK_Sender WHERE """ + colKey + rs.Sql() + ")"
		cur.execute(Query)
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		if orderFields != '':
			#Query = """SELECT * FROM T_Receive_Manager """ + (("ORDER BY " + ",".join(orderFields)) if len(orderFields) > 1 else " ORDER BY " + orderFields[0]) + (" DESC" if sortIndice == "" else sortIndice) + " LIMIT " + str(pageSize*(0 if PageIndex <= 1 else PageIndex)) + "," + str(pageSize)
			Query = """SELECT * FROM T_Outwards_Manager_""" + userName + """ ORDER BY """ + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
		else:			
			Query = """SELECT * FROM T_Outwards_Manager_""" + userName + """ ORDER BY IDApp LIMIT """ + strLimit + "," + str(pageSize)
		cur.execute(Query)
		result = query.dictfetchall(cur)
		#get countRows
		Query = """SELECT COUNT(*) FROM T_Outwards_Manager_""" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]
		cur.close()
		return (result,totalRecords)

	def getBrandForOutwards(self,searchText,orderFields,sortIndice,pageSize,PageIndex,userName):
		#get item from goods received
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Receive_Outwards_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_History_Outwards_" + userName		
		cur.execute(Query)
		
		#Query new items
		Query = "CREATE TEMPORARY TABLE Temp_T_Receive_Outwards" + userName  + """ ENGINE=MyISAM AS (SELECT g.idapp,g.itemcode as fk_goods,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS brandname,ngd.typeapp AS type,ngd.serialnumber, 'not yet used' as lastinfo,ngd.idapp as fk_receive, \
					0 AS fk_outwards,0 as fk_lending,0 AS fk_return,0 AS fk_maintenance,0 AS fk_disposal,0 AS fk_lost FROM n_a_goods g INNER JOIN n_a_goods_receive ngr ON ngr.fk_goods = g.IDApp INNER JOIN n_a_goods_receive_detail ngd ON ngr.IDApp = ngd.FK_App \
					WHERE NOT EXISTS(SELECT IDApp FROM n_a_goods_history WHERE fk_goods = ngr.fk_goods AND serialnumber = ngd.serialnumber)) """
		cur.execute(Query)
	    # Query get last trans in history 		
		Query = "CREATE TEMPORARY TABLE Temp_T_History_Outwards" + userName  + """ ENGINE=MyISAM AS (SELECT gh.idapp,gh.fk_goods,gh.goodsname,gh.brandname,gh.type,gh.serialnumber, \
                    CASE 
                        WHEN (gh.fk_return IS NOT NULL) THEN (SELECT e.NIK FROM employee e INNER JOIN n_a_goods_return ngn ON ngn.fk_usedemployee = e.idapp WHERE ngn.idapp = gh.fk_return) \
                        WHEN (gh.fk_lending IS NOT NULL) THEN ((SELECT e.NIK FROM employee e INNER JOIN n_a_goods_lending ngl ON ngl.fk_employee = e.idapp WHERE ngl.idapp = gh.fk_lending) \
						END AS fk_usedemployee,
                    CASE 
                    WHEN (gh.fk_return IS NOT NULL) THEN (SELECT e.employee_name FROM employee e INNER JOIN n_a_goods_return ngn ON ngn.fk_usedemployee = e.idapp WHERE ngn.idapp = gh.fk_return) \
                    END AS usedemployee,
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
						END AS lastinfo,
                        gh.fk_receive,gh.fk_outwards,gh.fk_lending,gh.fk_return,gh.fk_maintenance,gh.fk_disposal,gh.fk_lost  \
						FROM(			\
							SELECT g.idapp,g.itemcode as  fk_goods,g.goodsname,IFNULL(ngd.brandName,g.brandName) AS brandName,ngd.typeapp as 'type',ngd.serialnumber,ngd.idapp AS fk_receive,ngh.fk_outwards,ngh.fk_lending, \
							ngh.fk_return,ngh.fk_maintenance,ngh.fk_disposal,ngh.fk_lost FROM \
							n_a_goods g INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail ngd ON ngd.fk_app = ngr.idapp \
							INNER JOIN n_a_goods_history ngh ON ngh.fk_goods = g.idapp AND ngh.serialnumber = ngd.serialnumber \
							WHERE ngh.createddate = (SELECT Max(CreatedDate) FROM n_a_goods_history WHERE fk_goods = g.idapp AND serialnumber = ngd.serialnumber))gh
                             )				
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
		fkreceive = 0;fkreturn = 0;fklending = 0;fkoutwards = 0;fkmaintenance = 0;fkdisposal=0;fklost=0;fk_usedemployee = 'NIK';usedemployee = 'unknown';	
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
					lastInfo = 'Last used by ' + str(row[0]) + ', date lent ' + str(parse(row[1]).strftime('%d %B %Y')) + ', interests ' + str(row[2])
			elif int(fkoutwards) > 0:
				Query = """SELECT e.employee_name,ngo.datereleased,ngl.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.NIK = ngo.FK_Employee
							WHERE ngo.IDApp = %s"""
				cur.execute(Query,[fkoutwards])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date released ' + str(parse(row[1]).strftime('%d %B %Y')) + ', ' + str(row[2]) + ' (goods is still in use)'
			elif int(fkreturn) > 0:
				Query = """SELECT e.employee_name,ngt.datereturn,ngt.descriptions FROM n_a_goods_return ngt INNER JOIN employee e ON e.NIK = ngt.FK_FromEmployee
							WHERE ngt.IDApp = %s"""
				cur.execute(Query,[fkreturn])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date returned ' + str(parse(row[1]).strftime('%d %B %Y')) + ', ' + str(row[2]) + ' (goods is already returned)'
			elif int(fkmaintenance) > 0:
				Query = """SELECT CONCAT(IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,'')) as maintenanceby,StartDate,EndDate, IsFinished,IsSucced FROM n_a_maintenance WHERE IDApp  = %s"""
				cur.execute(Query,[fkmaintenance])
				if cur.rowcount > 0:
					row = cur.fetchone()
					isFinished = False;isSucced = False;starDate = datetime.now();endDate = datetime.now()
					if row[3] is not None:
						isFinished = strtobool(row[2])
					if row[4] is not None:
						isSucced = strtobool(row[3])
					if row[1] is not None:
						starDate =  str(parse(row[1]).strftime('%d %B %Y'))
					if row[2] is not None:
						endDate =  str(parse(row[1]).strftime('%d %B %Y'))
					if isFinished and isSucced:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is able to use)'
					elif isFinished == True and isSucced == false:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is unable to use )'
					elif not isFInished:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' + str(parse(starDate).strftime('%d %B %Y')) + ', ' +  ' (goods is still in maintenance)'
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
								lastInfo = 'Last used by ' + str(row[0]) + ', date lent ' + str(parse(row[1]).strftime('%d %B %Y')) + ', interests ' + str(row[2])
						elif int(fk_lost_outwards) > 0:
							Query = """SELECT e.employee_name,ngo.datereleased,ngl.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.NIK = ngo.FK_Employee
									WHERE ngo.IDApp = %s"""
							cur.execute(Query,[fkoutwards])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + ', date released ' + str(parse(row[1]).strftime('%d %B %Y')) + ', ' + str(row[2]) + ' (goods is still in use)'
						elif int(fk_lost_maintenance) > 0:
							Query = """SELECT CONCAT(IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,'')) as maintenanceby,StartDate,EndDate, IsFinished,IsSucced FROM n_a_maintenance WHERE IDApp  = %s"""
							cur.execute(Query,[fkmaintenance])
							if cur.rowcount > 0:
								row = cur.fetchone()
								isFinished = False;isSucced = False;starDate = datetime.now();endDate = datetime.now()
								if row[3] is not None:
									isFinished = strtobool(row[2])
									if row[4] is not None:
										isSucced = strtobool(row[3])
								if row[1] is not None:
									starDate =  str(parse(row[1]).strftime('%d %B %Y'))
								if row[2] is not None:
									endDate =  str(parse(row[1]).strftime('%d %B %Y'))
							if isFinished and isSucced:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is able to use)'
							elif isFinished == True and isSucced == false:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is unable to use )'
							elif not isFInished:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' + str(parse(starDate).strftime('%d %B %Y')) + ', ' +  ' (goods is still in maintenance)'
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
			dt = datetime.date(row[2])
			lastInfo = 'goods is new, date received ' + dt.strftime('%d %B %Y')
		cur.close()
		#idapp,fk_goods,goodsname,brandName,type,serialnumber,lastinfo,fk_outwards,fk_lending,fk_return,fk_maintenance,fk_disposal,fk_lost
		return(idapp,itemcode,goodsname,brandname,typeapp,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance)