from django.db import models
from NA_DataLayer.common import *
from django.db import transaction;
from django.db import connection
from decimal import Decimal
from django.db.models import Q
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
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
		elif columnKey == 'sellingprice':
			colKey = 'ngds.sellingprice'
		elif columnKey == 'proposedby':
			colKey = 'ngds.proposedby'
		elif columnKey == 'createdby':
			colKey = 'ngds.createdby'
		elif columnKey == 'createddate':
			colKey = 'ngds.ceateddate'
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Disposal_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		#idapp,goods,type,serialnumber,bookvalue,datedisposal,afterrepair,lastrepairFrom,issold,sellingprice,proposedby,acknowledgeby,approvedby,descriptions,createdby,createddate	
		Query = """  CREATE TEMPORARY TABLE T_Disposal_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT ngds.idapp,g.goodsname AS goods,ngd.typeApp AS goodstype,ngd.serialnumber,
				ngds.bookvalue,CASE WHEN(ngds.fk_maintenance IS NULL) THEN 0 ELSE 1 END AS afterrepair, 
				CASE WHEN (ngds.fk_maintenance IS NOT NULL) THEN(SELECT CONCAT(IFNULL(PersonalName,' '),', ',IFNULL(MaintenanceBy,'')) FROM n_a_maintenance WHERE idapp = ngds.fk_maintenance) ELSE '' END AS lastrepairfrom,
				ngds.issold,ngds.sellingprice,IFNULL(emp.responsible_by,'') AS proposedby,CONCAT(IFNULL(emp1.employee_name,''), ', ',IFNULL(emp2.employee_name,'')) AS acknowledgeby,IFNULL(emp3.employee_name,'') AS approvedby 
				,ngds.descriptions,ngds.createdby,ngds.createddate		       
		        FROM n_a_disposal ngds INNER JOIN n_a_goods g ON g.IDApp = ngds.FK_Goods 
		        INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = ngds.FK_Goods
		        INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
		        AND ngds.SerialNumber = ngd.SerialNumber
		        LEFT OUTER JOIN (SELECT idapp,employee_name AS responsible_by FROM employee) emp ON emp.idapp = ngds.FK_ResponsiblePerson
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp1 ON emp1.idapp = ngds.FK_Acknowledge1
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp2 ON emp2.idapp = ngds.FK_Acknowledge2
				LEFT OUTER JOIN(SELECT idapp,employee_name FROM employee) emp3 ON emp3.idapp = ngds.FK_ApprovedBy
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