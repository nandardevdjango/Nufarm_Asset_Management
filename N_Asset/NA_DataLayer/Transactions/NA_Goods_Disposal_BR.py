from django.db import models
from NA_DataLayer.common import *
from django.db import transaction;
from django.db import connection
from decimal import Decimal
from django.db.models import Q
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
import math
import datetime
class NA_BR_Goods_Disposal(models.Manager):
	def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		colkey = ''
		rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
		#datedisposal,afterrepair,lastrepairFrom,issold,sellingprice,proposedby,acknowledgeby,approvedby
		if columnKey == 'goods':
			colKey = 'g.goodsname'
		elif columnKey == 'goodstype':
			colKey = 'ngd.typeApp'
		elif columnKey == 'serialnumber':
			colKey = 'ngd.serialnumber'
		elif columnKey == 'datedisposal':
			colKey = 'ngds.datedisposal'
		elif columnKey == 'afterrepair':
			colKey = 'CONVERT((CASE WHEN(ngds.fk_maintenance IS NULL) THEN 0 ELSE 1 END),INT)'
		elif columnKey == 'lastrepairfrom':
			colKey = '(CASE WHEN (ngds.fk_maintenance IS NOT NULL) THEN(SELECT CONCAT(IFNULL(PersonalName,' '),', ',IFNULL(MaintenanceBy,'')) FROM n_a_maintenance WHERE idapp = ngds.fk_maintenance) ELSE '' END)'
		elif columnKey == 'issold':
			colKey = 'ngds.issold'
		elif columnKey == 'refgoodsfrom':
			colKey = 'ref.refgoodsfrom'
		elif columnKey == 'sellingprice':
			colKey = 'ngds.sellingprice'
		elif columnKey == 'proposedby':
			colKey = 'ngds.proposedby'
		elif columnKey == 'acknowledgeby':
			colKey = 'CONCAT(IFNULL(emp1.employee_name,''), ', ',IFNULL(emp2.employee_name,''))'
		elif columnKey == 'approvedby':
			colkey = 'IFNULL(emp3.employee_name,'')'
		elif columnKey == 'createdby':
			colKey = 'ngds.createdby'
		elif columnKey == 'createddate':
			colKey = 'ngds.createddate'
		elif columnKey == 'descriptions':
			colKey = 'ngds.descriptions'
		elif columnKey == 'soldto':
			colKey = "(SELECT CASE WHEN (ngds.sold_to = 'E') THEN (CONCAT('Employee ',IFNULL(emp4.employee_name,' '))) WHEN (ngds.sold_to = 'P') THEN (CONCAT('Non Employee ',IFNULL(ngds.sold_to_p_other,' '))) ELSE (CONCAT('Non Employee ',IFNULL(ngds.sold_to_p_other,' '))) END)"
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Disposal_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		#idapp,goods,type,serialnumber,bookvalue,datedisposal,afterrepair,lastrepairFrom,issold,sellingprice,proposedby,acknowledgeby,approvedby,descriptions,createdby,createddate	
		Query = """  CREATE TEMPORARY TABLE T_Disposal_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT ngds.idapp,g.goodsname AS goods,ngd.typeApp AS goodstype,ngd.serialnumber,
				ngds.bookvalue,	ngds.datedisposal,CONVERT((CASE WHEN(ngds.fk_maintenance IS NULL) THEN 0 ELSE 1 END),INT) AS afterrepair, 
				CASE WHEN (ngds.fk_maintenance IS NOT NULL) THEN(SELECT CONCAT(IFNULL(PersonalName,' '),', ',IFNULL(MaintenanceBy,'')) FROM n_a_maintenance WHERE idapp = ngds.fk_maintenance) ELSE '' END AS lastrepairfrom,
				ngds.islost,ref.refgoodsfrom,ngds.issold,ngds.sellingprice,
				CASE WHEN (ngds.sold_to = 'E') THEN (CONCAT('Employee ',IFNULL(emp4.employee_name,' '))) WHEN (ngds.sold_to = 'P') THEN (CONCAT('Non Employee ',IFNULL(ngds.sold_to_p_other,' '))) ELSE (CONCAT('Non Employee ',IFNULL(ngds.sold_to_p_other,' '))) END AS soldto,
				IFNULL(emp.responsible_by,'') AS proposedby,CONCAT(IFNULL(emp1.employee_name,''), ', ',IFNULL(emp2.employee_name,'')) AS acknowledgeby,IFNULL(emp3.employee_name,'') AS approvedby 
				,ngds.descriptions,ngds.createdby,ngds.createddate		       
		        FROM n_a_disposal ngds INNER JOIN n_a_goods g ON g.IDApp = ngds.FK_Goods 
		        INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = ngds.FK_Goods
		        INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
		        AND ngds.SerialNumber = ngd.SerialNumber
				INNER JOIN (SELECT nd.IDApp,CASE
							WHEN (nd.FK_Return IS NOT NULL) THEN 'Returned Eks Employee'
							WHEN (nd.fk_maintenance IS NOT NULL) THEN 'After Service(Maintenance)'
							WHEN (nd.FK_Lending IS NOT NULL) THEN '(After being Lent)'
							WHEN (nd.FK_Outwards IS NOT NULL) THEN '(Direct Return)'
							WHEN (nd.islost = 1) THEN 'goods has lost'
							ELSE 'Other (Uncategorized)'
							END AS refgoodsfrom FROM n_a_disposal nd)ref ON Ref.IDApp = ngds.IDApp
		        LEFT OUTER JOIN (SELECT idapp,employee_name AS responsible_by FROM employee) emp ON emp.idapp = ngds.fk_proposedby
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp1 ON emp1.idapp = ngds.FK_Acknowledge1
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp2 ON emp2.idapp = ngds.FK_Acknowledge2
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp3 ON emp3.idapp = ngds.FK_ApprovedBy
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp4 ON emp4.idapp = ngds.fk_sold_to_employee
		        WHERE """ + colKey + rs.Sql() + ")"
		cur.execute(Query)
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		if orderFields != '':
			#Query = """SELECT * FROM T_Receive_Manager """ + (("ORDER BY " + ",".join(orderFields)) if len(orderFields) > 1 else " ORDER BY " + orderFields[0]) + (" DESC" if sortIndice == "" else sortIndice) + " LIMIT " + str(pageSize*(0 if PageIndex <= 1 else PageIndex)) + "," + str(pageSize)
			Query = """SELECT * FROM T_Disposal_Manager_""" + userName + """ ORDER BY """ + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)
		else:			
			Query = """SELECT * FROM T_Disposal_Manager_""" + userName + """ ORDER BY IDApp LIMIT """ + strLimit + "," + str(pageSize)
		cur.execute(Query)
		result = query.dictfetchall(cur)
		#get countRows
		Query = """SELECT COUNT(*) FROM T_Disposal_Manager_""" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]
		cur.close()
		return (result,totalRecords)
	def getBookValue(self,cur,**kwargs):
			"""Function untuk mengambil nilai buku
			:param int idapp = idapp_fk_goods
			:param SerialNo
			:param DateDisposal
			return [int fk_acc_fa,float bookvalue,datetime StartCurBookValue,EndCurBookValue]
			"""
			fk_goods = 0
			serialno = ''
			datedisposal = None
			fk_goods = int(kwargs['idapp'])
			serialno = kwargs['SerialNo'];
			datedisposal = kwargs['DateDisposal']
			fkaccfa = 0
			bookvalue = 0
			startCurBookValue = None
			EndCurBookValue = None
			isNewCur = False
			Query = """SELECT EXISTS(SELECT fk_goods FROM n_a_acc_fa WHERE fk_goods = %(FK_Goods)s AND SerialNumber = %(SerialNO)s)"""
			if cur is None:
				cur = connection.cursor()
				isNewCur = True
			cur.execute(Query,{'FK_Goods':fk_goods,'SerialNO':kwargs['SerialNo']})
			row = cur.fetchone()
			if int(row[0]) > 0:
				Query1 = """SELECT idapp,DateDepreciation AS StartDate, bookvalue FROM n_a_acc_fa WHERE fk_goods = %(FK_Goods)s AND SerialNumber = %(SerialNO)s AND DateDepreciation <= %(DateDisposal)s ORDER BY DateDepreciation DESC LIMIT 1"""
				cur.execute(Query1,{'FK_Goods':fk_goods,'SerialNO':serialno,'DateDisposal':datedisposal})
				row = cur.fetchone()
				Query2 = """ SELECT DateDePreciation AS EndDate FROM n_a_acc_fa WHERE DateDepreciation > %(DateDisposal)s AND fk_goods = %(FK_Goods)s AND SerialNumber =  %(SerialNO)s ORDER BY DateDepreciation ASC LIMIT 1 """
				if row is not None:
					#return [int(row[0]),float(row[1])]
					fkaccfa = int(row[0])
					bookvalue = float(row[2])
					startCurBookValue = row[1]
					cur.execute(Query2,{'FK_Goods':fk_goods,'SerialNO':serialno,'DateDisposal':datedisposal})
					row = cur.fetchone()
					EndCurBookValue = row[0]
					if isNewCur:
						cur.close()
					return [fkaccfa,bookvalue,startCurBookValue,EndCurBookValue]
				else:
					if isNewCur:
						cur.close()
					return None
			else:
				cur.close()
				raise Exception(r"Can not find asset's book value")
	def getData(self,idapp):
			#idapp,fk_goods,goods,idapp_fk_goods,typeapp,serialnumber,brandvalue,bookvalue,fk_usedemployee,fk_usedemployee_employee,idapp_fk_usedemployee,datedisposal,issold,
	#sellingprice,fk_proposedby,fk_proposedby_employee,idapp_fk_proposedby,fk_Acknowledge1,fk_Acknowledge1_employee,idapp_fk_acknowledge1,fk_Acknowledge2,
	#fk_Acknowledge2_employee,idapp_fk_acknowledge2,descriptions,islost,fk_stock,fk_acc_fa,
	#fk_approvedby,fk_approvedby_employee,idapp_fk_approvedby,fk_maintenance,fk_return,fk_lending,fk_outwards,initializeForm,
		Query = """SELECT g.itemcode AS fk_goods,g.goodsname AS goods,gd.fk_goods AS idapp_fk_goods,gd.typeapp,gd.serialnumber, 
				CASE G.typeapp WHEN 'GA' THEN (SELECT Brand FROM n_a_ga_receive WHERE FK_Goods = gd.FK_Goods)
								WHEN 'IT' THEN (SELECT ngd.BrandName FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngd.fk_app = ngr.IDApp WHERE ngr.FK_Goods = gd.FK_goods AND ngd.serialnumber = gd.serialnumber)								
							    WHEN 'O' THEN IFNULL(g.BrandName,'Unknown Brand') END AS brandvalue,emp1.NIK AS fk_usedemployee,emp1.employee_name AS fk_usedemployee_employee,
					gd.fk_usedemployee AS idapp_fk_usedemployee,gd.datedisposal,gd.issold,gd.sellingprice,gd.sold_to,gd.fk_sold_to_employee AS idapp_fk_sold_to_employee,emp6.NIK AS fk_sold_to_employee,emp6.employee_name AS fk_sold_to_employee_employee,
				    gd.sold_to_p_other,gd.bookvalue,emp2.NIK AS fk_proposedby,emp2.employee_name AS fk_proposedby_employee,
				    gd.fk_proposedby AS idapp_fk_proposedby,emp3.NIK AS fk_acknowledge1,emp3.employee_name AS fk_acknowledge1_employee,gd.fk_Acknowledge1 as idapp_fk_acknowledge1,
					emp4.NIK AS fk_acknowledge2,emp4.employee_name AS fk_acknowledge2_employee,gd.fk_acknowledge2 as idapp_fk_acknowledge2,gd.descriptions,gd.islost,gd.fk_stock,gd.fk_acc_fa,
					emp5.NIK AS fk_approvedby,emp5.employee_name AS fk_approvedby_employee,gd.fk_approvedby AS idapp_fk_approvedby,gd.fk_maintenance,gd.fk_return,gd.fk_lending,gd.fk_outwards			
					FROM n_a_goods g INNER JOIN n_a_disposal gd ON gd.fk_goods = g.IDApp 
					LEFT OUTER JOIN employee emp1 ON emp1.IDApp = gd.fk_usedemployee 
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp2 ON emp2.IDApp = gd.fk_proposedby	
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp3 ON emp3.IDApp = gd.fk_Acknowledge1 
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp4 ON emp4.IDApp = gd.fk_Acknowledge2 
				    LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp5 ON emp5.IDApp = gd.fk_approvedby 
					LEFT OUTER JOIN (SELECT IDApp,NIK,employee_name FROM employee)emp6 ON emp6.IDApp = gd.fk_sold_to_employee 
					WHERE gd.idapp = %s""" 
		cur = connection.cursor()
		cur.execute(Query,[idapp])
		data = query.dictfetchall(cur)
		cur.close()
		return data

	def getBrandForDisposal(self,searchText,orderFields,sortIndice,pageSize,PageIndex,userName):
		cur = connection.cursor()
		Query =  "DROP TEMPORARY TABLE IF EXISTS Temp_T_History_Disposal_" + userName		
		cur.execute(Query)
		Query = " DROP TEMPORARY TABLE IF EXISTS Temp_F_Disposal_" + userName
		cur.execute(Query)
	    # Query get last trans in history 		
		Query = "CREATE TEMPORARY TABLE Temp_T_History_Disposal_" + userName  + """ ENGINE=MyISAM AS (SELECT gh.idapp,gh.fk_goods,gh.goodsname,gh.brandname,gh.type,gh.serialnumber, \
                    CASE 
                        WHEN (gh.fk_return IS NOT NULL) THEN (SELECT e.NIK FROM employee e INNER JOIN n_a_goods_return ngn ON ngn.fk_usedemployee = e.idapp WHERE ngn.idapp = gh.fk_return) \
                        WHEN (gh.fk_lending IS NOT NULL) THEN (SELECT e.NIK FROM employee e INNER JOIN n_a_goods_lending ngl ON ngl.fk_employee = e.idapp WHERE ngl.idapp = gh.fk_lending) \
						WHEN (gh.fk_lost IS NOT NULL) THEN (SELECT e.NIK FROM employee e INNER JOIN n_a_goods_lost ngls on ngls.FK_UsedBy = e.idapp WHERE ngls.idapp = gh.fk_lost) \
						END AS fk_usedemployee,
                   CASE 
						WHEN (gh.fk_return IS NOT NULL) THEN (SELECT e.employee_name FROM employee e INNER JOIN n_a_goods_return ngn ON ngn.fk_usedemployee = e.idapp WHERE ngn.idapp = gh.fk_return) \
						END AS usedemployee,
					CASE \
						WHEN (gh.fk_maintenance IS NOT NULL) THEN (SELECT CONCAT('Maintenance by ', IFNULL(maintenanceby,''), ' ',	IFNULL(PersonalName,''), \
							(CASE \
								WHEN (isfinished = 1 AND issucced = 1) THEN (CONCAT(' Date Returned  ',DATE_FORMAT(enddate,'%d %B %Y'),'goods is able to dispose/delete')) \
								WHEN (isfinished = 1 AND issucced = 0) THEN (CONCAT(' Date Returned ',DATE_FORMAT(enddate,'%d %B %Y'),'goods is able to dispose/delete')) \
								WHEN (isfinished = 0) THEN (CONCAT(' Date maintenance ',DATE_FORMAT(enddate,'%d %B %Y'),'goods is still in maintenance')) \
								END)) FROM n_a_maintenance WHERE IDApp = gh.fk_maintenance) \
						WHEN(gh.fk_lending IS NOT NULL) THEN((CASE \
																WHEN ((SELECT `status` FROM n_a_goods_lending WHERE idapp = gh.fk_lending) = 'L') THEN 'good is still lent' \
																ELSE ('goods is able to dispose/delete') \
																END)) \
						WHEN(gh.fk_outwards IS NOT NULL) THEN 'goods is still in use by other employee' \
						WHEN (gh.fk_return IS NOT NULL) THEN 'goods is able to dispose/delete' \
						WHEN (gh.fk_disposal IS NOT NULL) THEN 'goods has been disposed/deleted' \
						WHEN (gh.fk_lost IS NOT NULL) THEN 'goods has lost' \
						ELSE 'Unknown or uncategorized last goods position' \
						END AS lastinfo,
                        gh.fk_receive,gh.fk_outwards,gh.fk_lending,gh.fk_return,gh.fk_maintenance,gh.fk_lost  \
						FROM(\
							SELECT g.idapp,g.itemcode as  fk_goods,g.goodsname,IFNULL(ngd.brandName,g.brandName) AS brandName,ngd.typeapp as 'type',ngd.serialnumber,ngd.idapp AS fk_receive,ngh.fk_outwards,ngh.fk_lending, \
							ngh.fk_return,ngh.fk_maintenance,ngh.fk_disposal,ngh.fk_lost FROM \
							n_a_goods g INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail ngd ON ngd.fk_app = ngr.idapp \
							INNER JOIN n_a_goods_history ngh ON ngh.fk_goods = g.idapp AND ngh.serialnumber = ngd.serialnumber \
							WHERE ngh.createddate = (SELECT Max(CreatedDate) FROM n_a_goods_history WHERE fk_goods = g.idapp AND serialnumber = ngd.serialnumber)\
							UNION \
							SELECT g.idapp,g.itemcode as  fk_goods,g.goodsname,IFNULL(nggr.Brand,g.BrandName) AS BrandName,nggr.typeapp as 'type',nggr.Machine_No AS serialnumber,nggr.idapp AS fk_receive,ngh.fk_outwards,ngh.fk_lending, \
							ngh.fk_return,ngh.fk_maintenance,ngh.fk_disposal,ngh.fk_lost FROM \
							n_a_goods g INNER JOIN n_a_ga_receive nggr ON g.idapp = nggr.fk_goods \
							INNER JOIN n_a_goods_history ngh ON ngh.fk_goods = g.idapp AND ngh.serialnumber = nggr.Machine_No \
							WHERE ngh.createddate = (SELECT Max(CreatedDate) FROM n_a_goods_history WHERE fk_goods = g.idapp AND serialnumber = nggr.Machine_No) \
							)gh
                      )				
				"""
		cur.execute(Query)
		strLimit = '300'
		if int(PageIndex) <= 1:
			strLimit = '0'
		else:
			strLimit = str(int(PageIndex)*int(pageSize))
		#gabungkan jadi satu
		Query = "CREATE TEMPORARY TABLE Temp_F_Disposal_" + userName + """ ENGINE=MyISAM AS (
				 SELECT * FROM Temp_T_History_Disposal_""" + userName + """\
				  WHERE (goodsname LIKE %s OR brandname LIKE %s) OR (serialnumber = %s))"""
		cur.execute(Query,['%'+searchText+'%','%'+searchText+'%',searchText])
		if orderFields == '':
			Query  = "SELECT *,CONVERT((CASE lastinfo WHEN '(goods has been disposed/deleted)' THEN 1 \
								ELSE 0),INT) AS Ready FROM Temp_F_Disposal_" + userName + " ORDER BY goodsname " + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)	
		else:
			Query  = "SELECT * FROM Temp_F_Disposal_" + userName + " ORDER BY " + orderFields + (" DESC" if sortIndice == "" else ' ' + sortIndice) + " LIMIT " + strLimit + "," + str(pageSize)				
		cur.execute(Query)
		result = query.dictfetchall(cur)

		Query = "SELECT COUNT(*) FROM Temp_F_Disposal_" + userName
		cur.execute(Query)
		row = cur.fetchone()
		totalRecords = row[0]
		cur.close()
		return (result,totalRecords)
	def getLastTrans(self,SerialNO):
		idapp_fk_goods = 0
		itemcode = ''		
		goodsname = ''
		typeapp = ''
		brandname = ''
		serialnumber = ''
		lastinfo = 'unknown'
		islost = False
		bookvalue = 0
		fk_acc_fa = 0
		fk_usedemployee = 'NIK';usedemployee = 'unknown';fkaccfa = 0;fkreturn = 0;fklending = 0;fkoutwards = 0;fkmaintenance = 0;
		Query = """SELECT g.idapp,g.itemcode,g.goodsname,IFNULL(ngd.BrandName,g.BrandName) AS BrandName,ngd.typeapp FROM n_a_goods_receive_detail ngd INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngd.FK_App \
						LEFT OUTER JOIN n_a_goods g ON g.IDApp = ngr.FK_Goods WHERE ngd.serialnumber = %s AND g.typeapp = 'IT' """
		cur = connection.cursor()
		cur.execute(Query,[SerialNO])
		recCount =  cur.rowcount
		##idapp_fk_goods,itemcode,islost,fidapp_fk_usedemployee,fk_acc_fa,fk_maintenance,fk_return,fk_lending,fk_outwards,goods,brandname,typeapp,bookvalue,lastinfo
		category = 'IT'
		row = []
		if recCount > 0:
			row = cur.fetchone()
			typeapp = row[4]
			brandname = row[3]
			goodsname = row[2]
			itemcode = row[1]
			idapp_fk_goods = row[0]
		else:
			Query = """SELECT g.idapp,g.itemcode,g.goodsname,IFNULL(nggr.Brand,g.BrandName) AS BrandName,nggr.typeapp FROM n_a_ga_receive nggr INNER JOIN n_a_goods g ON g.IDApp = nggr.fk_goods \
				WHERE nggr.Machine_No = %s AND g.typeapp = 'GA'"""
			cur = connection.cursor()
			cur.execute(Query,[SerialNO])
			recCount =  cur.rowcount
			if recCount > 0:
				row = cur.fetchone()
				typeapp = row[4]
				brandname = row[3]
				goodsname = row[2]
				itemcode = row[1]
				idapp_fk_goods = row[0]
			else:
				cur.close()
				raise Exception('no such data')
			category = 'GA'
		#ambil nilai buku,default ambil tanggal akhir = sekarang
		bkData = self.getBookValue(cur,idapp=idapp_fk_goods,SerialNo=SerialNO,DateDisposal=datetime.date.today())
		if bkData is not None:
			bookvalue = bkData[0]
			fk_acc_fa = bkData[1]
		#cek apakah data sudah di disposed sebelumnya
		Query = """SELECT EXISTS(SELECT SerialNumber FROM n_a_disposal WHERE serialnumber =  %s AND fk_goods = %s)"""
		cur.execute(Query,[SerialNO,idapp_fk_goods])
		row = cur.fetchone()
		if int(row[0]) >0:
			cur.close()
			raise Exception('asset has been disposed/deleted')
		#cek apakah sudah ada transaksi untuk barang dengan serial number tsb
		Query = """SELECT EXISTS(SELECT serialnumber FROM n_a_goods_history WHERE serialnumber = %s AND fk_goods = %s)"""
		cur.execute(Query,[SerialNO,idapp_fk_goods])
		row = cur.fetchone()
		if int(row[0]) > 0:
			#cek apakah data sudah di 
			#jika ada ambil data transaksi terakhir yang mana transaksi ada 4 kelompok,lending,outwards,return,maintenance
			Query = """SELECT FK_Lending,FK_Outwards,FK_Return,FK_Maintenance,fk_lost FROM n_a_goods_history WHERE serialnumber = %s AND fk_goods = %s ORDER BY createddate DESC LIMIT 1 """
			cur.execute(Query,[SerialNO,idapp_fk_goods])
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
					fklost = row[4]
			if int(fklending)>0:#fklending hanya di goods IT 
				Query = """SELECT e.nik,e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.idapp = ngl.FK_Employee
							WHERE ngl.IDApp = %s"""
				cur.execute(Query,[fklending])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + '|' +  str(row[1]) + ', date lent ' + parse(str(row[2])).strftime('%d %B %Y') + ', interests ' + str(row[3])
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
			elif int(fkoutwards) > 0:
				if category == 'IT':
					Query = """SELECT e.nik,e.employee_name,ngo.datereleased,ngo.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.idapp = ngo.FK_Employee
							WHERE ngo.IDApp = %s"""
				else :
					Query = """SELECT e.nik,e.employee_name,nggo.datereleased,nggo.descriptions FROM n_a_ga_outwards nggo INNER JOIN employee e ON e.idapp = nggo.FK_Employee
							WHERE nggo.IDApp = %s"""
				cur.execute(Query,[fkoutwards])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + '|' + str(row[1]) + ', date released ' + parse(str(row[2])).strftime('%d %B %Y') + ', ' + str(row[3]) + ' (goods is still in use)'
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
			elif int(fkreturn) > 0:
				if category == 'IT':
					Query = """SELECT e.NIK,e.employee_name,ngt.datereturn,ngt.descriptions FROM n_a_goods_return ngt INNER JOIN employee e ON e.idapp = ngt.FK_FromEmployee
							WHERE ngt.IDApp = %s"""
				else:
					Query = """SELECT E.NIK,e.employee_name,nggt.datereturn,nggt.descriptions FROM n_a_goods_return nggt INNER JOIN employee e ON e.idapp = nggt.FK_FromEmployee
							WHERE ngt.IDApp = %s"""
				cur.execute(Query,[fkreturn])
				if cur.rowcount > 0:
					row = cur.fetchone()
					lastInfo = 'Last used by ' + str(row[0]) + '|' + str(row[1]) + ', date returned ' + parse(str(row[2]).strftime('%d %B %Y')) + ', ' + str(row[3]) + ' (goods is already returned)'
					fk_usedemployee = str(row[0])
					usedemployee = str(row[1])
			elif int(fkmaintenance) > 0:#nadisposal tidak ada reference dari maintenance, karena barang di hapus harus hanya hilang/sesudah ada fisiknya(direturn dari pegawai ke kantor atau dari daerah pegawai langsung di jual)/di return dari bengkel ke kantor
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
			elif int(fklost) > 0:
				Query = """SELECT fk_goods_lending,fk_goods_outwards,fk_maintenance,Reason,status FROM n_a_goods_lost WHERE idapp = %s"""
				cur.execute(Query,[fklost])
				lastInfo = "goods has lost "
				if cur.rowcount > 0:
					islost = True
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
						if int(fk_lost_lending) > 0:#fklending hanya di goods IT 
							Query = """SELECT e.NIK,e.employee_name,ngl.datelending,ngl.interests FROM n_a_goods_lending ngl INNER JOIN employee e ON e.idapp = ngl.FK_Employee
									WHERE ngl.IDApp = %s"""
							cur.execute(Query,[fk_lost_lending])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + '|' + str(row[1]) + ', date lent ' + parse(str(row[2])).strftime('%d %B %Y') + ', interests ' + str(row[3])
								fk_usedemployee = str(row[0])
								usedemployee = str(row[1])
						elif int(fk_lost_outwards) > 0:
							if category == 'IT':
								Query = """SELECT e.nik,e.employee_name,ngo.datereleased,ngo.descriptions FROM n_a_goods_outwards ngo INNER JOIN employee e ON e.idapp = ngo.FK_Employee
									WHERE ngo.IDApp = %s"""
							else :
								Query = """SELECT e.nik,e.employee_name,nggo.datereleased,nggo.descriptions FROM n_a_ga_outwards nggo INNER JOIN employee e ON e.idapp = nggo.FK_Employee
									WHERE nggo.IDApp = %s"""
							cur.execute(Query,[fk_lost_outwards])
							if cur.rowcount > 0:
								row = cur.fetchone()
								lastInfo = 'Last used by ' + str(row[0]) + '|' + str(row[1]) + ', date released ' + parse(str(row[2])).strftime('%d %B %Y') + ', ' + str(row[3]) + ' (goods is still in use)'
								fk_usedemployee = str(row[0])
								usedemployee = str(row[1])
						elif int(fk_lost_maintenance) > 0:#nadisposal tidak ada reference dari maintenance, karena barang di hapus harus hanya hilang/sesudah ada fisiknya(direturn dari pegawai ke kantor atau dari daerah pegawai langsung di jual)/di return dari bengkel ke kantor
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
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' +endDate + ', ' +  ' (goods is able to use)'
							elif isFinished == True and isSucced == False:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', date returned ' + endDate + ', ' +  ' (goods is unable to use)'
							elif not isFinished:
								lastInfo = 'Last maintenance by ' + str(row[0]) + ', start date maintenance ' +starDate + ', ' +  ' (goods is still in maintenance)'
						#elif fk_lost_outwards
						else:
							lastInfo = "goods has lost, but has been found "
		else:
			if category == 'IT':
				Query = """SELECT ngl.idapp as fk_receive,ngl.brandname,ngl.typeapp,ngr.datereceived FROM n_a_goods_receive_detail ngl INNER JOIN n_a_goods_receive ngr ON ngr.IDApp = ngl.FK_App WHERE ngl.serialnumber = %s"""
			else:
				Query = """SELECT nggr.idapp as fk_receive,nggr.brand,nggr.typeapp,nggr.datereceived FROM n_a_ga_receive nggr WHERE nggr.serialnumber = %s AND nggr.fk_goods = %"""
			cur.execute(Query,[SerialNO,idapp_fk_goods])
			dt = datetime.now()
			row = []
			if cur.rowcount > 0:
				dt = datetime.date(row[2])
				cur.close()
				raise Exception('goods has not been used (probably is still new, date received' + dt.strftime('%d %B %Y') + ')')
			else:
				cur.close()
				raise Exception('no such data')
		###idapp_fk_goods,itemcode,goods,brandname,typeappp,islost,idapp_fk_usedemployee,usedemployee,fk_acc_fa,lastinfo,bookvalue,fk_maintenance,fk_return,fk_lending,fk_outwards
		return(idapp_fk_goods,itemcode,goodsname,brandname,typeapp,islost,fk_usedemployee, usedemployee,fk_acc_fa,bookvalue,lastInfo,fkmaintenance,fkreturn,fklending,fkoutwards,fklost)
	def HasExists(self,idapp_fk_goods,serialnumber):
		return super(NA_BR_Goods_Disposal,self).get_queryset().filter(Q(fk_goods=idapp_fk_goods) & Q(serialnumber=serialnumber)).exists()#Q(member=p1) | Q(member=p2)
	def Delete(self,IDApp,userName):
		cur = connection.cursor()
		#delete di table na_disposal
		#delete di table history
		with transaction.atomic():
			Query = """SELECT FK_Goods FROM n_a_disposal WHERE IDApp = %s"""
			cur.execute(Query,[IDApp])
			fk_goods = '';
			if cur.rowcount > 0:
				row = cur.fetchone()
				if row is not None:
					fk_goods = row[0]
								 
			Query = """DELETE FROM n_a_disposal WHERE IDApp = %s""" 
			cur.execute(Query,[IDApp])
			Query = """DELETE FROM n_a_goods_history WHERE fk_disposal = %s"""
			cur.execute(Query,[IDApp])
			#update stock
			if fk_goods != '':
				Query = "SELECT COUNT(FK_Goods) FROM n_a_disposal WHERE FK_Goods =  %(FK_Goods)s"
				cur.execute(Query, {'FK_Goods': fk_goods})
				if cur.rowcount > 0:
					row = cur.fetchone()
					totalDisposal = int(row[0])
					Query = """UPDATE n_a_stock	SET	ModifiedDate=NOW(), ModifiedBy=%(ModifiedBy)s,TDisposal= %(TDisposal)s WHERE FK_Goods = %(FK_Goods)s """
					params = {'ModifiedBy':userName,'TDisposal':totalDisposal,'FK_Goods':fk_goods}
			return "success"
	def SaveData(self,Data,Status=StatusForm.Input):
		cur = connection.cursor()
		#get FK_stock
		Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
		cur.execute(Query,{'FK_Goods':Data['idapp_fk_goods']})
		row = []
		if cur.rowcount > 0:
			row = cur.fetchone()
			fk_stock = row[0]
		#ngke deui..., haduh.... lila...., super sibukkk....
		#save data
		try:
			with transaction.atomic():
				if Status == StatusForm.Input:
					Query = """INSERT INTO n_a_disposal
							(TypeApp, SerialNumber, DateDisposal, IsLost, IsSold, SellingPrice,Sold_To,FK_Sold_To_Employee,Sold_To_P_Other,
								BookValue, FK_Acc_FA, FK_Goods, FK_Lending, FK_Outwards, FK_Maintenance, FK_Acknowledge1, FK_Acknowledge2, FK_ApprovedBy,
								Descriptions, FK_ProposedBy, FK_Return,FK_Lost, FK_Stock, FK_UsedEmployee,CreatedDate, CreatedBy)
							VALUES (%(TypeApp)s, %(SerialNumber)s, %(DateDisposal)s, %(IsLost)s, %(IsSold)s, %(SellingPrice)s,%(Sold_To)s,%(FK_Sold_To_Employee)s,%(Sold_To_P_Other)s,
								%(BookValue)s, %(FK_Acc_FA)s, %(FK_Goods)s, %(FK_Lending)s, %(FK_Outwards)s, %(FK_Maintenance)s, 
								%(FK_Acknowledge1)s, %(FK_Acknowledge2)s, %(FK_ApprovedBy)s,%(Descriptions)s, 
								%(FK_ProposedBy)s, %(FK_Return)s,%(FK_Lost)s, %(FK_Stock)s, %(FK_UsedEmployee)s,NOW(), %(CreatedBy)s)"""
					params = {'TypeApp':Data['typeapp'], 'SerialNumber':Data['serialnumber'], 'DateDisposal':Data['datedisposal'], 'IsLost':Data['islost'], 'IsSold':Data['issold'], 'SellingPrice':Data['sellingprice'],
							'Sold_To':Data['sold_to'],'FK_Sold_To_Employee':Data['idapp_fk_sold_to_employee'],'Sold_To_P_Other':Data['sold_to_p_other'],
								'BookValue':Data['bookvalue'], 'FK_Acc_FA':Data['faaccfa'], 'FK_Goods':Data['fk_goods'], 'FK_Lending':Data['fk_lending'], 'FK_Outwards':Data['fk_outwards'], 
								'FK_Maintenance':Data['fk_maintenance'], 'FK_Acknowledge1':Data['idapp_fk_acknowledge1'], 'FK_Acknowledge2':Data['idapp_fk_acknowledge2'], 'FK_ApprovedBy':Data['idapp_fk_approvedby'],
								'Descriptions':Data['descriptions'], 'FK_ProposedBy':Data['idapp_fk_proposedby'], 'FK_Return':Data['fk_return'], 'FK_Lost':Data['fk_lost'],'FK_Stock':fk_stock, 'FK_UsedEmployee':Data['idapp_fk_usedemployee'],
								'CreatedBy':Data['createdby']}	
					cur.execute(Query,params)
					cur.execute('SELECT last_insert_id()')
					row = cur.fetchone()
					FKApp = row[0]
					Query = """INSERT INTO n_a_goods_history
								( SerialNumber,TypeApp,  FK_Disposal, FK_Goods, FK_Lending, FK_Lost, FK_Maintenance, FK_Outwards, FK_Return,CreatedDate, CreatedBy)
								VALUES (%(SerialNumber)s, %(TypeApp)s,%(FK_Disposal)s, %(FK_Goods)s, NULL, %(FK_Lost)s, %(FK_Maintenance)s, %(FK_Outwards)s, %(FK_Return)s, NOW(),%(Createdby)s)"""
					params = {'SerialNumber':Data['serialnumber'], 'TypeApp':Data['typeapp'],'FK_Disposal':FKApp, 'FK_Goods':Data['fk_goods'], 'FK_Lending':Data['fk_lending'], 
									'FK_Lost':Data['fk_lost'], 'FK_Maintenance':Data['fk_maintenance'], 'FK_Outwards':Data['fk_outwards'], 'FK_Return':Data['fk_return'], 'Createdby':Data['createdby']}
					cur.execute(Query,params)

					#update stock
					Query = "SELECT COUNT(FK_Goods) FROM n_a_disposal WHERE FK_Goods =  %(FK_Goods)s"
					cur.execute(Query, {'FK_Goods': Data['fk_goods']})
					if cur.rowcount > 0:
						row = cur.fetchone()
						totalDisposal = int(row[0])
						Query = """UPDATE n_a_stock	SET	ModifiedDate=NOW(), ModifiedBy=%(ModifiedBy)s,TDisposal= %(TDisposal)s WHERE FK_Goods = %(FK_Goods)s """
						params = {'ModifiedBy':Data['createdby'],'TDisposal':totalDisposal,'FK_Goods':Data['fk_goods']}
						cur.execute(Query,params)
				else:
					Query = """UPDATE n_a_disposal
							SET	DateDisposal=%(DateDisposal)s,
								IsLost=%(IsLost)s,
								IsSold=%(IsSold)s,
								SellingPrice=%(SellingPrice)s,
								Sold_To = %(Sold_To)s,
								FK_Sold_To_Employee = %(FK_Sold_To_Employee)s,
								Sold_To_P_Other = %(Sold_To_P_Other)s,
								BookValue=%(BookValue)s,
								FK_Acc_FA=%(FK_Acc_FA)s,
								FK_Goods=%(FK_Goods)s,
								FK_Lending=%(FK_Lending)s,
								FK_Outwards=%(FK_Outwards)s,
								FK_Maintenance=%(FK_Maintenance)s,
								FK_Acknowledge1=%(FK_Acknowledge1)s,
								FK_Acknowledge2=%(FK_Acknowledge2)s,
								FK_ApprovedBy=%(FK_ApprovedBy)s,
								Descriptions=%(Descriptions)s,
								FK_ProposedBy=%(FK_ProposedBy)s,
								FK_Return=%(FK_Return)s,
								FK_UsedEmployee=%(FK_UsedEmployee)s,
								ModifiedBy = %(ModifiedBy)s,
								ModifiedDate = NOW() 
							WHERE IDApp = %(IDApp)s """
					params = {'IDApp':Data['idapp'],'DateDisposal':Data['datedisposal'], 'IsLost':Data['islost'], 'IsSold':Data['issold'], 'SellingPrice':Data['sellingprice'],
							 'Sold_To':Data['sold_to'],'FK_Sold_To_Employee':Data['idapp_fk_sold_to_employee'],'Sold_To_P_Other':Data['sold_to_p_other'],
								'BookValue':Data['bookvalue'], 'FK_Acc_FA':Data['faaccfa'], 'FK_Goods':Data['fk_goods'], 'FK_Lending':Data['fk_lending'], 'FK_Outwards':Data['fk_outwards'], 
								'FK_Maintenance':Data['fk_maintenance'], 'FK_Acknowledge1':Data['idapp_fk_acknowledge1'], 'FK_Acknowledge2':Data['idapp_fk_acknowledge2'], 'FK_ApprovedBy':Data['idapp_fk_approvedby'],
								'Descriptions':Data['descriptions'], 'FK_ProposedBy':Data['idapp_fk_proposedby'], 'FK_Return':Data['fk_return'], 'FK_UsedEmployee':Data['idapp_fk_usedemployee'],
								'ModifiedBy':Data['modifiedby']}
					cur.execute(Query,params)			
			return "success"
		except Exception as e :
			cur.close()
			return repr(e)

		
