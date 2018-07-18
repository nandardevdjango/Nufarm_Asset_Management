from django.db import models, connection, transaction
from NA_DataLayer.common import (CriteriaSearch, DataType, ResolveCriteria, query,
                                 StatusForm, Data)
class NA_BR_Goods_Return_GA(models.Manager):
	def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
		cur = connection.cursor()
		rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
		Query = ''
		cur.execute(Query)
		result = query.dictfetchall(cur)
		cur.close()
		return result