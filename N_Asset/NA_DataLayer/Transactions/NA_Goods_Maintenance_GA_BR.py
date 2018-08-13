from django.db import models, connection
from NA_DataLayer.common import CriteriaSearch, ResolveCriteria, query, StatusForm, DataType, Data, Message
class NA_BR_GA_Maintenance(models.Manager):
	def PopulateQuery(self, columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
		return result