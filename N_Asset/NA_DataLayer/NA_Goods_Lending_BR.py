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

		Query = "DROP TEMPORARY TABLE IF EXISTS T_Lending_Manager_" + userName
		cur = connection.cursor()
		cur.execute(Query)