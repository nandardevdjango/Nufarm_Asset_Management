from django.db import models
from dateutil.parser import parse
from django.db import transaction
from django.db import connection
from decimal import Decimal
from datetime import datetime
from django.db.models import Q
from NA_DataLayer.common import (
    Data, ResolveCriteria,
    commonFunct, decorators, Message,query,CriteriaSearch,DataType,StatusForm
)
#from django.db.models import OuterRef, Subquery
import NA_Models.models
#from NA_DataLayer.MasterData.NA_Employee import NA_BR_Employee
from distutils.util import strtobool
import math
class NA_BR_Goods_Outwards(models.Manager):
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		colkey = ''
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		if columnKey == 'goods':
			colKey = 'g.goodsname'
		elif columnKey == 'goodstype':
			colKey = 'ngd.TypeApp'
		elif columnKey == 'serialnumber':
			colKey = 'ngd.serialnumber'
		elif columnKey == 'daterequest':
			colKey = 'nga.daterequest'
		elif columnKey == 'datereleased':
			colKey = 'nga.datereleased'
		elif columnKey == 'isnew':
			colKey = 'nga.isnew'
		elif columnKey == 'for_employee':
			colKey = 'e.employee_name'
		elif columnKey == 'responsible_by':
			colKey = 'emp1.responsible_by'
		elif columnKey == 'senderby':
			colKey = 'emp2.senderby'
		elif columnKey == 'refgoodsfrom':
			colKey = 'ref.refgoodsfrom'
		elif columnKey == 'createdby':
			colKey = 'nga.createdby'
		elif columnKey == 'createddate':
			colKey = 'nga.ceateddate'
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Outwards_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query = """  CREATE TEMPORARY TABLE T_Outwards_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT nga.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,nga.daterequest,nga.datereleased,
		        nga.isnew,nga.fk_employee,e.employee_name as for_employee,nga.fk_usedemployee,
		        CASE 
			        WHEN(nga.fk_usedemployee IS NOT NUll) THEN(SELECT employee_name FROM `employee` WHERE idapp = nga.fk_usedemployee LIMIT 1)
			        END AS eks_employee,nga.fk_responsibleperson,emp1.responsible_by,nga.fk_sender,emp2.senderby,nga.fk_stock,
		        ref.refgoodsfrom,nga.createdby,nga.createddate,nga.equipment_desc,nga.descriptions
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
	def isGoodsNew(self, serialnumber):
		Used =NAGoodsHistory.objects(
		).filter(serialnumber=serialnumber).select_related('fk_outwards').first()
		if Used:
			return True
		Used =NAGoodsHistory.objects(
		).filter(serialnumber=serialnumber).select_related('fk_lending').first()
		return Used
	def getBrandForOutwards(self,searchText,orderFields,sortIndice,pageSize,PageIndex,userName):
		#get item from goods received
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Receive_Outwards_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_History_Outwards_" + userName		
		cur.execute(Query)
		Query = "DROP TEMPORARY TABLE IF EXISTS Temp_F_Outwards_" + userName
		cur.execute(Query)
		#Query new items
		Query = "CREATE TEMPORARY TABLE Temp_T_Receive_Outwards_" + userName  + """ ENGINE=MyISAM AS (SELECT g.idapp,g.itemcode as fk_goods,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS brandname,ngd.typeapp AS type,ngd.serialnumber, '' AS fk_usedemployee,'' AS usedemployee, 'not yet used' as lastinfo,ngd.idapp as fk_receive, \
					0 AS fk_outwards,0 as fk_lending,0 AS fk_return,0 AS fk_maintenance,0 AS fk_disposal,0 AS fk_lost FROM n_a_goods g INNER JOIN n_a_goods_receive ngr ON ngr.fk_goods = g.IDApp INNER JOIN n_a_goods_receive_detail ngd ON ngr.IDApp = ngd.FK_App \
					WHERE NOT EXISTS(SELECT IDApp FROM n_a_goods_history WHERE fk_goods = ngr.fk_goods AND serialnumber = ngd.serialnumber)) """
		cur.execute(Query)
	    # Query get last trans in history 		
		Query = "CREATE TEMPORARY TABLE Temp_T_History_Outwards_" + userName  + """ ENGINE=MyISAM AS (SELECT gh.idapp,gh.fk_goods,gh.goodsname,gh.brandname,gh.type,gh.serialnumber, \
                    CASE 
                        WHEN (gh.fk_return IS NOT NULL) THEN (SELECT e.NIK FROM employee e INNER JOIN n_a_goods_return ngn ON ngn.fk_usedemployee = e.idapp WHERE ngn.idapp = gh.fk_return) \
                        WHEN (gh.fk_lending IS NOT NULL) THEN ((SELECT e.NIK FROM employee e INNER JOIN n_a_goods_lending ngl ON ngl.fk_employee = e.idapp WHERE ngl.idapp = gh.fk_lending)) \
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
		Query = "CREATE TEMPORARY TABLE Temp_F_Outwards_" + userName + """ ENGINE=MyISAM AS (SELECT * FROM \
				(SELECT * FROM Temp_T_Receive_Outwards_""" + userName + """ \
					UNION \
				 SELECT * FROM Temp_T_History_Outwards_""" + userName + """\
				 )C WHERE (goodsname LIKE %s OR brandname LIKE %s)  OR (`Type` LIKE %s) OR (serialnumber = %s))"""
		cur.execute(Query,['%'+searchText+'%','%'+searchText+'%','%'+searchText+'%',searchText])
		if orderFields == '':
			Query  = "SELECT * FROM Temp_F_Outwards_" + userName + " ORDER BY brandname " + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)	
		else:
			Query  = "SELECT * FROM Temp_F_Outwards_" + userName + " ORDER BY " + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)				
		cur.execute(Query)
		result = query.dictfetchall(cur)

		Query = "SELECT COUNT(*) FROM Temp_F_Outwards_" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]

		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Receive_Outwards_" + userName
		cur = connection.cursor()
		cur.execute(Query)

		cur.close()
		return (result,totalRecords)
	def getLastDateTrans(self,pkkey,pkfrom):
		if pkfrom == 'fk_lending':
			Query = "SELECT DateReturn FROM n_a_goods_lending WHERE IDApp = %s"
		elif pkfrom == 'fk_return':
			Query = "SELECT DateReturn FROM n_a_goods_return WHERE IDApp = %s"
		elif pkfrom == 'fk_maintenance':
			Query = "SELECT EndDate FROM n_a_goods_maintenance WHERE IDApp = %s"
		else:
			return ''
		cur = connection.cursor()
		cur.execute(Query,[pkkey])
		row = cur.fetchone()
		return row[0]
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
			#cek apakah data sudah di 
			#jika ada ambil data transaksi terakhir yang mana transaksi ada 4 kelompok,lending,outwards,return,maintenance
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
				Query = """SELECT e.nik,e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.idapp = ngl.FK_Employee
							WHERE ngl.IDApp = %s"""
				cur.execute(Query,[fklending])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + '|' +  str(row[1]) + ', date lent ' + parse(str(row[2])).strftime('%d %B %Y') + ', interests ' + str(row[3])
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
			elif int(fkoutwards) > 0:
				Query = """SELECT e.nik,e.employee_name,ngo.datereleased,ngo.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.idapp = ngo.FK_Employee
							WHERE ngo.IDApp = %s"""
				cur.execute(Query,[fkoutwards])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + '|' + str(row[1]) + ', date released ' + parse(str(row[2])).strftime('%d %B %Y') + ', ' + str(row[3]) + ' (goods is still in use)'
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
			elif int(fkreturn) > 0:
				Query = """SELECT e.nik,e.employee_name,ngt.datereturn,ngt.descriptions FROM n_a_goods_return ngt INNER JOIN employee e ON e.idapp = ngt.FK_FromEmployee
							WHERE ngt.IDApp = %s"""
				cur.execute(Query,[fkreturn])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + ', date returned ' + parse(str(row[2])).strftime('%d %B %Y') + ', ' + str(row[3]) + ' (goods is already returned)'
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
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
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' + starDate + ', ' +  ' (goods is still in maintenance)'
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
					fk_lost_lending = 0;fk_lost_outwards = 0;fk_lost_maintenance = 0
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
							Query = """SELECT e.NIK,e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.idapp = ngl.FK_Employee
									WHERE ngl.IDApp = %s"""
							cur.execute(Query,[fk_lost_lending])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + ', date lent ' + parse(str(row[2])).strftime('%d %B %Y') + ', interests ' + str(row[3])
								fk_usedemployee = str(row[0])
								usedemployee = str(row[1])
						elif int(fk_lost_outwards) > 0:
							Query = """SELECT e.NIK,e.employee_name,ngo.datereleased,ngl.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.idapp = ngo.FK_Employee
									WHERE ngo.IDApp = %s"""
							cur.execute(Query,[fk_lost_outwards])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + ', date released ' + parse(str(row[2])).strftime('%d %B %Y') + ', ' + str(row[3]) + ' (goods is still in use)'
								fk_usedemployee = str(row[0])
								usedemployee = str(row[1])
						elif int(fk_lost_maintenance) > 0:
							Query = """SELECT CONCAT(IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,'')) as maintenanceby,StartDate,EndDate, IsFinished,IsSucced FROM n_a_maintenance WHERE IDApp  = %s"""
							cur.execute(Query,[fk_lost_maintenance])
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
		return(idapp,itemcode,goodsname,brandname,typeapp,fk_usedemployee,usedemployee,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance)
	def HasExists(self,idapp_fk_goods,serialnumber,datereq,daterel,fk_employee):
		return super(NA_BR_Goods_Outwards,self).get_queryset().filter(Q(fk_goods=idapp_fk_goods) & Q(serialnumber=serialnumber) & Q(fk_employee=fk_employee)).exists()#Q(member=p1) | Q(member=p2)
	def SaveData(self,Data,Status=StatusForm.Input):
		cur = connection.cursor()
		#get FK_stock
		Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
		cur.execute(Query,{'FK_Goods':Data['idapp_fk_goods']})
		row = []
		FKApp = 0
		if cur.rowcount > 0:
			row = cur.fetchone()
			fk_stock = row[0]
		try:
			with transaction.atomic():
				if Status == StatusForm.Input:
					#insert outwards
					#insert history
					#idapp, fk_goods:  isnew: idapp_fk_goods: idapp_fk_employee: 
					#daterequest:  datereleased : fk_responsibleperson:  idapp_fk_responsibleperson: 
					#fk_sender:  idapp_fk_sender: descriptions:  typeapp: serialnumber: 
					#fk_frommaintenance:  fk_return: fk_lending:  fk_receive:lastinfo: lastinfo,status:
					Query = """INSERT INTO `n_a_goods_outwards`(`FK_Goods`, `IsNew`, `DateRequest`, `DateReleased`, `FK_Employee`, `FK_UsedEmployee`, `FK_FromMaintenance`, `FK_ResponsiblePerson`, `FK_Sender`, `FK_Stock`, `SerialNumber`, `TypeApp`,
								`FK_Lending`,`equipment_desc`, `Descriptions`, `FK_Return`, `FK_Receive`, `CreatedDate`, `CreatedBy`, `lastinfo`) 
								VALUES (%(FK_Goods)s,%(IsNew)s,%(DateRequest)s,%(DateReleased)s,%(FK_Employee)s,%(FK_UsedEmployee)s,%(FK_FromMaintenance)s,%(FK_ResponsiblePerson)s,%(FK_Sender)s,%(FK_Stock)s,%(SerialNumber)s,%(TypeApp)s,
								%(FK_Lending)s,%(Equipment_Desc)s, %(Descriptions)s, %(FK_Return)s, %(FK_Receive)s, NOW(), %(CreatedBy)s, %(lastinfo)s)"""
					param = {'FK_Goods':Data['idapp_fk_goods'],'IsNew':Data['isnew'],'DateRequest':Data['daterequest'],'DateReleased':Data['datereleased'],
							'FK_Employee':Data['idapp_fk_employee'],'FK_UsedEmployee':Data['idapp_fk_usedemployee'],'FK_FromMaintenance':Data['fk_frommaintenance'],
							'FK_ResponsiblePerson':Data['idapp_fk_responsibleperson'],'FK_Sender':Data['idapp_fk_sender'],'FK_Stock':fk_stock,'SerialNumber':Data['serialnumber'],
							'TypeApp':Data['typeapp'],'FK_Lending':Data['fk_lending'],'Equipment_Desc':Data['equipment_desc'], 'Descriptions':Data['descriptions'], 'FK_Return':Data['fk_return'],
						    'FK_Receive':Data['fk_receive'], 'CreatedBy':Data['createdby'], 'lastinfo':Data['lastinfo']}
					cur.execute(Query,param)
					cur.execute('SELECT last_insert_id()')
					row = cur.fetchone()
					FKApp = row[0]
					#insert n_goods_history
					Query = """INSERT INTO n_a_goods_history(FK_Goods, TypeApp, SerialNumber, FK_Lending, FK_Outwards, FK_RETURN, FK_Maintenance, FK_Disposal, FK_LOST, CreatedDate, CreatedBy) \
							 VALUES (%(FK_Goods)s,%(TypeApp)s, %(SerialNumber)s, NULL,%(FK_Outwards)s, NULL, NULL, NULL, NULL, NOW(), %(CreatedBy)s )"""
					param = {'FK_Goods':Data['idapp_fk_goods'],'TypeApp':Data['typeapp'],'SerialNumber':Data['serialnumber'],'FK_Outwards':FKApp,'CreatedBy':Data['createdby']}
				else:
					Query = """ UPDATE n_a_goods_outwards SET FK_Employee=%(FK_Employee)s,DateRequest=%(DateRequest)s,DateReleased=%(DateReleased)s,FK_ResponsiblePerson=%(FK_ResponsiblePerson)s, \
								FK_Sender=%(FK_Sender)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s,Equipment_Desc=%(Equipment_Desc)s,Descriptions=%(Descriptions)s \
								WHERE idapp = %(idapp)s """
					param = {'idapp':Data['idapp'],'FK_Goods':Data['idapp_fk_goods'],'FK_Employee':Data['idapp_fk_employee'],'DateRequest':Data['daterequest'],'DateReleased':Data['datereleased'],'FK_ResponsiblePerson':Data['idapp_fk_responsibleperson'],
							'FK_Sender':Data['idapp_fk_sender'],'ModifiedBy':Data['modifiedby'],'Equipment_Desc':Data['equipment_desc'],'Descriptions':Data['descriptions']}
				cur.execute(Query,param)
				who = Data['createdby'] if Status == StatusForm.Input else Data['modifiedby']
				#(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare) = commonFunct.getTotalGoods(Data['idapp_fk_goods'],cur,who)
				TStock =  commonFunct.getTotalGoods(Data['idapp_fk_goods'],cur,who)
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

			if Status == StatusForm.Input:
				return FKApp
			else:
				return 'success'
		except Exception as e :
			cur.close()
			return repr(e)
	def HasReference(self,IDApp):
		cur = connection.cursor()
		Query = """SELECT EXISTS(SELECT IDApp FROM n_a_goods_lost WHERE FK_Goods_Outwards = %s) 
					OR EXISTS(SELECT IDApp FROM n_a_goods_return WHERE FK_Goods_Outwards = %s) """
		cur.execute(Query,[IDApp,IDApp])
		row = cur.fetchone()
		if cur.rowcount > 0:
			return int(row[0]) > 0
		else:
			return False
	def Delete(self,idapp,username):
		cur = connection.cursor()
		Query = """SELECT ns.IDApp,ngo.fk_goods,ngo.serialnumber,ngo.idapp FROM n_a_stock ns INNER JOIN n_a_goods_outwards ngo ON ngo.fk_goods = ns.fk_goods WHERE ngo.IDApp = %s LIMIT 1"""
		cur.execute(Query,[idapp])
		fk_stock = None
		fk_goods = None
		serialnumber = None
		fk_outwards = None
		with transaction.atomic():
			if cur.rowcount > 0:
				row = cur.fetchone()
				fk_stock = row[0]
				fk_goods = row[1]
				serialnumber = row[2]
				fk_outwards = row[3]
			else:
				Query = """SELECT ngr.fk_goods,ngd.serialnumber,ngd.idapp FROM n_a_goods_receive ngr INNER JOIN n_a_goods_outwards ngo ON ngo.fk_goods = ngr.fk_goods 
							INNER JOIN n_a_goods_receive_detail ngd ON ngd.fk_app = ngr.idapp AND ngo.serialnumber = ngd.serialnumber WHERE ngo.idapp =  %s"""
				cur.execute(Query,[idapp])
				row = cur.fetchone()
				fk_goods = row[1]
				serialnumber = row[2]
				fk_outwards = row[3]
			Query = """DELETE FROM n_a_goods_outwards WHERE idapp = %s"""
			cur.execute(Query,[idapp])
			Query = """DELETE FROM n_a_goods_history WHERE fk_goods = %s AND serialnumber = %s AND fk_outwards = %s"""
			cur.execute(Query,[fk_goods,serialnumber,idapp])
			TStock = commonFunct.getTotalGoods(fk_goods, cur, username)
			TotalSpare = TStock[6]
			totalUsed = TStock[2]
			totalNew = TStock[0]
			totalRenew = TStock[4]
			totalReturn = TStock[3]
			totalReceived = TStock[1]
			totalMaintenance = TStock[5]

			#Update n_a_stock
			Query = """UPDATE n_a_stock SET T_Goods_Spare=%(T_Goods_Spare)s,TIsUsed=%(TIsUsed)s,TIsNew=%(TIsNew)s,TIsRenew=%(TIsRenew)s,TGoods_Return=%(TGoods_Return)s,
					TGoods_Received=%(TGoods_Received)s,TMaintenance=%(TMaintenance)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s WHERE IDApp= %(fk_stock)s"""
			param = {'fk_stock':fk_stock,'T_Goods_Spare':TotalSpare,'TIsUsed':totalUsed,'TIsNew':totalNew,'TIsRenew':totalRenew,'TGoods_Return':totalReturn,
					'TGoods_Received':totalReceived,'TMaintenance':totalMaintenance,'ModifiedBy':username}
			cur.execute(Query,param)
			return "success"
	def getData(self,idapp):
		cur = connection.cursor()
			#/idapp, fk_goods, isnew, goods, idapp_fk_goods, fk_employee, idapp_fk_employee, fk_employee_employee
			#   //daterequest,datereleased, fk_stock, fk_responsibleperson, idapp_fk_responsibleperson, fk_responsibleperson_employee,
			# fk_sender, idapp_fk_sender, fk_sender_employee,  descriptions,fk_usedemployee,idapp_fk_usedemployee,fk_usedemployee_employee, typeapp, serialnumber,
			#   //brandvalue, fk_frommaintenance, fk_return, fk_lending, fk_receive,  lastinfo, initializeForm, hasRefData  
		Query = """SELECT g.itemcode AS fk_goods,ngo.isnew,g.goodsname AS goods,ngo.fk_goods AS idapp_fk_goods,emp.NIK AS fk_employee,\
					ngo.fk_employee AS idapp_fk_employee,emp.employee_name AS fk_employee_employee,ngo.daterequest,ngo.datereleased,ngo.fk_stock,\
					emp2.NIK AS fk_responsibleperson, ngo.FK_ResponsiblePerson AS idapp_fk_responsibleperson,IFNULL(ngo.lastinfo,'not yet used') AS lastinfo, \
					emp1.NIK AS fk_sender,ngo.fk_sender AS idapp_fk_sender,emp1.employee_name AS fk_sender_employee,ngo.equipment_desc, \
					ngo.descriptions,emp3.NIK AS fk_usedemployee,ngo.fk_usedemployee AS idapp_fk_usedemployee,emp3.employee_name AS fk_usedemployee_employee,ngo.typeapp,ngo.serialnumber, emp2.employee_name AS fk_responsibleperson_employee,g.brandname AS brandvalue, \
					IFNULL(ngo.fk_frommaintenance,0)AS fk_frommaintenance,IFNULL(ngo.fk_return,0) AS fk_return, \
					IFNULL(ngo.fk_lending,0) AS fk_lending,IFNULL(fk_receive,0) AS fk_receive, \
						CASE WHEN EXISTS(SELECT fk_goods FROM n_a_disposal WHERE fk_goods = ngo.fk_goods AND serialnumber = ngo.serialnumber) THEN 1 
							WHEN EXISTS(SELECT fk_goods FROM n_a_goods_lost WHERE fk_goods_outwards = ngo.idapp) THEN 1 
							 ELSE 0 
					END AS hasRefData  
					FROM n_a_goods g INNER JOIN n_a_goods_outwards ngo ON ngo.fk_goods = g.IDApp \
					INNER JOIN employee emp ON emp.IDApp = ngo.fk_employee 	\
					LEFT OUTER JOIN (SELECT IDApp, NIK,employee_name FROM employee)emp1 ON emp1.IDApp = ngo.fk_sender	\
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp2 ON emp2.IDApp = ngo.FK_ResponsiblePerson 
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp3 ON emp3.IDApp = ngo.fk_usedemployee WHERE ngo.idapp = %s""" 
		cur.execute(Query,[idapp])
		data = query.dictfetchall(cur)
		cur.close()
		return data
	def getReportAdHoc(self, idapp):
	#	"""main_display_add_hoc = ['GoodsName', 'BrandName', 'SerialNumber', 'Type',
    #    'DateReleased', 'ToEmployee', 'Equipment', 'Descriptions', 'Conditions', 'Eks_Employee', 'Sender']"""
	#	#buat dulu subquery
	#	to_employee = super(NA_BR_Goods_Outwards, self).get_queryset().filter(fk_employee=OuterRef('pk')).values('fk_employee')[:1]
	#	qs = super(NA_BR_Goods_Outwards, self).get_queryset() \
	#		.filter(refno__iexact=RefNo) \
	#		.select_related('n_a_goods','employee')
		cur = connection.cursor()
		Query = """SELECT g.GoodsName,IFNULL(ngd.brandName,g.brandName) AS BrandName,ngo.SerialNumber,ngd.TypeApp AS `Type`,
				ngo.DateReleased,Emp1.employee_name as ToEmployee,ngo.Descriptions,ngo.Equipment_Desc AS Equipment,
				CASE ngo.IsNew WHEN 0 THEN 'Bekas' WHEN 1 THEN 'Baru' ELSE 'Unknown' END AS Conditions,
				emp2.employee_name AS Eks_Employee,emp3.employee_name AS Sender
				FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.IDApp
				INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = ngo.FK_Goods
				INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
				AND ngo.SerialNumber = ngd.SerialNumber
				LEFT OUTER JOIN(SELECT IDApp, employee_name FROM employee)emp1 ON emp1.IDApp = ngo.fk_employee
				LEFT OUTER JOIN(SELECT IDApp,employee_name FROM employee)emp2 ON emp2.IDApp = ngo.FK_UsedEmployee
				LEFT OUTER JOIN(SELECT IDApp,employee_name FROM employee)emp3 ON emp3.IDApp = ngo.fk_sender
				WHERE ngo.IDApp = %s"""
		cur.execute(Query,[idapp])
		data = query.dictfetchall(cur)
		cur.close()
		return data
			
