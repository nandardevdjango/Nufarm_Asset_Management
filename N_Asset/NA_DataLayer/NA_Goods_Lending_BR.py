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
class NA_BR_Goods_Lending(models.manager):
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
		elif columnKey == 'createddate':
			colKey = 'ngl.createddate'
		Query = "DROP TEMPORARY TABLE IF EXISTS T_Lending_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)
		Query = """ CREATE TEMPORARY TABLE T_Lending_Manager_""" + userName  + """ENGINE=MyISAM AS (SELECT g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,L.lentby,S.sentby,ngl.DateLending AS lentdate,ngl.Interests,R.responsibleby,
					Ref.refgoodsfrom,ngl.isnew,ngl.status, ngl.createdby,ngl.createddate
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