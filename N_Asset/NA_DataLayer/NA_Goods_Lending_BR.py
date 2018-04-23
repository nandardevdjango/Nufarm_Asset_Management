from django.db import models
from NA_DataLayer.common import *
from django.db.models import Count, Case, When,Value, CharField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from django.db.models import Q
from decimal import Decimal
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
class NA_BR_Goods_Lending(models.Manager):
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		colKey = ''
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		if columnKey == 'goods':
			colKey = 'g.goodsname'
		elif columnKey == 'typeapp':
			colKey = 'ngd.TypeApp'
		elif columnKey == 'serialnumber':
			colKey = 'ngd.serialnumber'
		elif columnKey == 'lentby':
			colKey = 'L.lentby'
		elif columnKey == 'sentby':
			colKey = 'S.sentby'
		elif columnKey == 'lentdate':
			colKey = 'ngl.DateLending'
		elif columnKey == 'intererests':
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
		Query = """ CREATE TEMPORARY TABLE T_Lending_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT ngl.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,L.lentby,S.sentby,ngl.DateLending AS lentdate,ngl.interests,R.responsibleby,
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
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS lentby FROM employee WHERE InActive = 0 AND InActive IS NOT NULL)L
										ON L.IDApp = ngl.FK_Employee
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS sentby FROM employee WHERE InActive = 0 AND InActive IS NOT NULL)S
										ON S.IDApp = ngl.FK_Employee
					LEFT OUTER JOIN(SELECT IDApp,Employee_Name AS responsibleby FROM employee WHERE InActive = 0 AND InActive IS NOT NULL)R
					ON R.IDApp = ngl.FK_Employee WHERE """ + colKey + rs.Sql() + ")"
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
		totalRecords = row
		cur.close()
		return (result,totalRecords)

	def UpdateStatus(self,idapp,newVal,UpdatedBy):		
		cur = connection.cursor()			
		with transaction.atomic():
			Query = """SELECT FK_Goods FROM n_a_goods_lending WHERE idapp = %(idapp)s LIMIT 1 """
			cur.execute(Query,{'idapp':idapp})
			row = cur.fetchone()
			FKGoods = int(row[0])

			Query = """UPDATE n_a_goods_lending SET status = %(newVal)s WHERE idapp = %(idapp)s """
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

			Query = """UPDATE n_a_stock SET T_Goods_Spare = %(TotalSpare),Modifiedby = %(UpdatedBy)s, ModifiedDate = NOW() WHERE FK_Goods = %(FK_Goods)s"""
			cur.execute(Query,{'TotalSpare':TotalSpare,'UpdatedBy':UpdatedBy,'FK_Goods':FKGoods})
			return 'success'
	def getInterest(self,SearchIntr):
		return super(NA_BR_Goods_Lending,self).get_queryset().filter(interests__istartswith=SearchIntr).values('interests').distinct()
	
	def getLastTrans(self,SerialNO):
		"""function untuk mengambil terakhir transaksi data, sebagai umpan balik ke user, barang ini terakhir di pake oleh siapa / belum di pakai sama sekali
		param : SerialNO
		"""
		#ambil data brand dan typenya
		Query = """SELECT g.itemcode,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS BrandName,ngd.typeapp FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App \
					LEFT OUTER JOIN n_a_goods g ON g.IDApp = ngr.FK_Goods WHERE ngd.serialnumber = %s"""
		cur = connection.cursor()
		cur.execute(Query,[SerialNO])
		typeapp = ''
		brandname = ''
		goodsname = ''
		itemcode = ''
		row = []
		if cur.rowcount > 0:
			row = cur.fetchone()
			typeapp = row[3]
			brandname = row[2]
			goodsname = row[1]
			itemcode = row[0]
		else:
			cur.close()
			raise Exception('no such data')
		#cek apakah sudah ada transaksi untuk barang dengan serial number tsb
		Query = """SELECT EXISTS(SELECT serialnumber FROM n_a_goods_history WHERE serialnumber = %s)"""
		cur.execute(Query,[SerialNO])
		row = cur.fetchone()
		lastInfo = 'unknown'
		if int(row[0]) > 0:
			#jika ada ambil data transaksi terakhir yang mana transaksi ada 4 kelompok,lending,outwards,return,maintenance,disposal
			Query = """SELECT FK_Lending,FK_Outwards,FK_RETURN,FK_Maintenance,FK_Disposal FROM n_a_goods_history WHERE serialnumber = %s ORDER BY createddate DESC LIMIT 1 """
			cur.execute(Query,[SerialNO])
			row = cur.fetchone()
			fklending = 0;fkoutwards = 0;fkmaintenance = 0;fkdisposal=0
			if cur.rowcount > 0:
				fklending = row[0]
				fkoutwards = row[1]
				fkreturn = row[2]
				fkmaintenance = row[3]
				fkdisposal = row[4]
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
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is able to use )'
					elif isFinished == True and isSucced == false:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + str(parse(endDate).strftime('%d %B %Y')) + ', ' +  ' (goods is not able to use )'
					elif not isFInished:
						lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' + str(parse(starDate).strftime('%d %B %Y')) + ', ' +  ' (goods is still in maintenance)'
			elif int(fkdisposal) > 0:
				Query = """SELECT Descriptions FROM n_a_disposal WHERE IDApp = %s"""
				cur.execute(Query,[fkdisposal])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = "goods is not able to use again " +  row[0]
		else:
			Query = """SELECT ngl.brandname,ngl.typeapp,ngr.datereceived FROM n_a_goods_receive_detail ngl INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngl.FK_App WHERE ngl.serialnumber = %s"""
			cur.execute(Query,[SerialNO])
			row = []
			if cur.rowcount > 0:
				row = cur.fetchone()
				typeapp = row[1]
				brandname = row[0]
			else:
				raise Exception('no such data')
			dt = datetime.date(row[2])
			lastInfo = 'goods is new, date received ' +dt.strftime('%d %B %Y')
		cur.close()
		return(itemcode,goodsname,typeapp,brandname,lastInfo)

	def getBrandForLending(self,serialNO,goodsName,BrandName):
		#get item from goods received
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Receive_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Lending_" + userName
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Maintenance_" + userName
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Disposal_" + userName
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Outwards_" + userName
		cur.execute(Query)
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_Lost_" + userName
		cur.execute(Query)

		#Query new items
		Query = """CREATE TEMPORARY TABLE T_Lending_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS BrandName,ngd.serialnumber, descriptions = 'not yet used' \
					FROM n_a_goods g INNER JOIN n_a_goods_receive ngr ON ngr.fk_goods = g.IDApp INNER JOIN n_a_goods_receive_detail ngd ON ngr.IDApp = ngd.FK_App \
					WHERE NOT EXISTS(SELECT IDApp FROM n_a_goods_history WHERE fk_goods = ngr.fk_goods AND serialnumber = ngd.serialnumber) """
	    # Query get last trans in history 
		

#SELECT *     
#FROM MyTable T1    
#WHERE date = (
#   SELECT max(date)
#   FROM MyTable T2
#   WHERE T1.username=T2.username
#)




	

