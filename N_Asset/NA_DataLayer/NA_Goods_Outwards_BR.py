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
                        END AS fk_usedemployee
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