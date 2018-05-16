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
		"""  CREATE TEMPORARY TABLE T_Outwards_Manager_""" + userName  + """ ENGINE=MyISAM AS (SELECT nga.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,nga.daterequest,nga.datereleased,
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