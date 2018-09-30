from django.db import models
from NA_DataLayer.common import *
from django.db.models import  Count, Case, When,Value, CharField,IntegerField,BooleanField
from django.db import transaction;
from django.db import connection
from django.core import exceptions
from decimal import Decimal, DecimalException
from django.db.models import F
from django.db.models import Q
from decimal import Decimal
from NA_DataLayer.common import commonFunct
from NA_DataLayer.Transactions.NA_Goods_Receive_BR import NA_BR_Goods_Receive
class NA_BR_Goods_Receive_Detail(models.Manager):
	def getHeaderData(self,refNo):
		"""
		return idapp,idapp_fk_goods,goods_desc,datereceived,supliername,employee_receieved,employee_pr,totalpurchase,totalreceived
		"""

		self.__class__.c = connection.cursor()
		cur = self.__class__.c
		Query = """SELECT ngr.idapp,ngr.FK_goods AS idapp_fk_goods, goodsname as goods_desc,g.economiclife, \
		ngr.datereceived,sp.suppliername,emp1.employee_received,emp2.employee_pr,ngr.totalpurchase,ngr.totalreceived FROM n_a_goods_receive AS ngr \
		INNER JOIN n_a_supplier AS sp ON sp.SupplierCode = ngr.FK_Supplier LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_receivedby,employee_name AS employee_received FROM employee) AS Emp1 \
		ON emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_p_r_by,employee_name AS employee_pr FROM employee) AS Emp2 ON Emp2.IDApp = ngr.FK_P_R_By \
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE ngr.refno = %s"""
		cur.execute(Query,[refNo])
		data = query.dictfetchall(cur)
		cur.close()
		return data
	def getDetailData(self,fkApp,idapp_fk_goods):
		#NAData = super(NA_BR_Goods_Receive_Detail,self).get_queryset().filter(refno__exact=refno).values('brandname')
		#NDATA = NData.annotate(no=Value(None,output_field=IntegerField()),HasRef=Value(False,output_field=BooleanField()),isnew=Value(False,output_field=BooleanField())).values('idapp','fk_app','itemcode','no',
		#									'brandname','typeapp','priceperunit','serialnumber','warranty','endofwarranty',
		#									'createdby','createddate','modifiedby','modifieddate','HasRef','isnew')
		return NA_BR_Goods_Receive.getDetailData(fkApp,idapp_fk_goods)