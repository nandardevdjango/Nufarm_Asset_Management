from enum import Enum
from datetime import date
from datetime import datetime
class CriteriaSearch(Enum):
	Equal = 1
	BeginWith = 2
	EndWith = 3
	NotEqual = 4
	Greater = 5
	Less = 6
	LessOrEqual = 7
	GreaterOrEqual = 8
	Like = 9
	In = 10
	NotIn = 11
	Beetween = 12
class StatusForm(Enum):
	Input = 1
	Edit = 2; InputOrEdit = 3; View = 4; 
class DataType(Enum):
	  BigInt = 1; Boolean = 2;Char = 3;DateTime = 4; Decimal = 5; Float = 6; Image = 7; Integer = 8;
	  Money = 9; NChar = 10; NVarChar = 11; VarChar = 12; Variant=13;

class ResolveCriteria:
	__query = "";
	def __init__(self,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar,columnKey='',value=None):
		self.criteria = criteria
		self.typeofData = typeofData
		self.valueData = value
		self.colKey = columnKey
	def DefaultModel(self):
		filterfield = self.colKey + '__istarswith'
		if self.criteria==CriteriaSearch.Beetween:
			if self.typeofData==DataType.Boolean or self.typeofData==DataType.Char or self.typeofData==DataType.NChar or self.typeofData==DataType.NVarChar \
				or self.typeofData==DataType.VarChar:
					raise ValueError('value type is in valid')
			if self.typeofData==DataType.DateTime:
				if ',' in str(self.valueData):
					strValueKeys = str(self.valueData).split(',')
					filterfield = self.colKey + '__range'
					return {filterfield:[datetime((str(strValueKeys[0])[0:3]),str(strValueKeys[0])[5:6],str(strValueKeys[0])[7:8]),datetime((str(strValueKeys[1])[0:3]),str(strValueKeys[1])[5:6],str(strValueKeys[1])[7:8])]}
			elif self.typeofData==DataType.BigInt or self.typeofData==DataType.Decimal or self.typeofData==DataType.Float or self.typeofData==DataType.Integer or self.typeofData==DataType.Money:
				return {filterfield:[self.valueData[0],self.valueData[1]]}
			else:
				raise ValueError('value type is in valid')
		elif self.criteria==CriteriaSearch.BeginWith:
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				return {filterfield:self.valueData}
			else:
				raise ValueError('value type is in valid')
		elif self.criteria==CriteriaSearch.EndWith:
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				filterfield = self.colKey + '__iendswith'
			else:
				raise ValueError('value type is in valid')
			return {filterfield:self.valueData}

	def Sql(self):
		if self.criteria==CriteriaSearch.Beetween:
			if self.typeofData==DataType.Boolean or self.typeofData==DataType.Char or self.typeofData==DataType.NChar or self.typeofData==DataType.NVarChar \
				or self.typeofData==DataType.VarChar:
					raise ValueError('value type is in valid')
			if self.typeofData==DataType.DateTime:
				values = str(self.valueData).split('-')
				startDate = values[0]
				endDate = values[1]
				self.__class__.__query = ' >= {0!s} AND ' + self.colKey + ' <= {1!s}'.format(startDate,endDate)
		elif self.criteria==CriteriaSearch.BeginWith:
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				ResolveCriteria.__query= " LIKE '{0!s}%'".format(str(self.valueData))
		elif self.criteria==CriteriaSearch.EndWith:
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				ResolveCriteria.__query = " LIKE '%{0!s}'".format(str(self.valueData))
		elif self.criteria == CriteriaSearch.Equal:
			ResolveCriteria.__query = ' = {0}'.format(self.valueData)
		elif self.criteria==CriteriaSearch.Greater:
			if self.typeofData==DataType.Integer or self.typeofData==DataType.Decimal or self.typeofData==DataType.Float or self.typeofData==DataType.Money \
				or self.typeofData==DataType.BigInt:
				ResolveCriteria.__query = ' > {0}'.format(float(self.valueData))
			elif self.typeofData==DataType.DateTime:
				ResolveCriteria.__query = ' > {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
		elif self.criteria==CriteriaSearch.GreaterOrEqual:
			if self.typeofData==DataType.Integer or self.typeofData== DataType.Decimal or self.typeofData==DataType.Float or self.typeofData==DataType.Money \
				or self.typeofData==DataType.BigInt:
				ResolveCriteria.__query = ' > {0}'.format(float(self.valueData))
			elif self.typeofData==DataType.DateTime:
				#format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses
				ResolveCriteria.__query = ' >= {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
		elif self.criteria==CriteriaSearch.In:
			rowFilter = " IN('"
			if ',' in str(self.valueData):
				strValueKeys = str(self.valueData).split(',')				
				for i in range(len(strValueKeys)):
					rowFilter += strValueKeys[i] + "'"
					if i < len(strValueKeys) -1:
						rowFilter += ","
				rowFilter += ")"
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				if rowFilter != " IN(')":
					ResolveCriteria.__query = rowFilter
				else:
					ResolveCriteria.__query = " IN ('{0!s}')".format(str(self.valueData))
			elif self.typeofData==DataType.DateTime:
			#format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses	
				ResolveCriteria.__query = ' IN {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
		elif self.criteria==CriteriaSearch.Less:
			if self.typeofData==DataType.Integer or self.typeofData== DataType.Decimal or self.typeofData==DataType.Float or self.typeofData==DataType.Money \
				or self.typeofData==DataType.BigInt:
				ResolveCriteria.__query = ' < {0}'.format(float(self.valueData))
			elif self.typeofData==DataType.DateTime:
				ResolveCriteria.__query = ' < {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
		elif self.criteria==CriteriaSearch.LessOrEqual:
			if self.typeofData==DataType.Integer or self.typeofData== DataType.Decimal or self.typeofData==DataType.Float or self.typeofData==DataType.Money \
				or self.typeofData==DataType.BigInt:
				ResolveCriteria.__query = ' <= {0}'.format(float(self.valueData))
			elif self.typeofData==DataType.DateTime:
				ResolveCriteria.__query = ' <= {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
		elif self.criteria==CriteriaSearch.Like:
			if self.typeofData==DataType.Char or self.typeofData==DataType.VarChar or self.typeofData==DataType.NVarChar:
				ResolveCriteria.__query = " LIKE '%{0!s}%'".format(str(self.valueData))
		elif self.criteria==CriteriaSearch.NotEqual:
				ResolveCriteria.__query = ' <>{0} '.format(str(self.valueData))
		return ResolveCriteria.__query

	def getDataType(strDataType):
		if strDataType == 'int':
			return DataType.Integer
		elif strDataType=='varchar':
			return DataType.VarChar
		elif strDataType == 'bigint':
			return DataType.BigInt
		elif strDataType == 'boolean':
			return DataType.Boolean
		elif strDataType == 'char':
			return DataType.Char
		elif strDataType == 'datetime':
			return DataType.DateTime
		elif strDataType == 'decimal':
			return DataType.Decimal
		elif strDataType == 'float':
			return DataType.Float
		elif strDataType == 'image':
			return DataType.Image
		elif strDataType == 'money':
			return DataType.Money
		elif strDataType == 'nchar':
			return DataType.Char
		elif strDataType =='nvarchar':
			return DataType.NVarChar
		else :
			return DataType.VarChar
	
	def getCriteriaSearch(strCriteria):
		if strCriteria == 'equal':
			return CriteriaSearch.Equal
		elif strCriteria == 'beginwith':
			return CriteriaSearch.BeginWith
		elif strCriteria == 'endwith':
			return CriteriaSearch.EndWith
		elif strCriteria == 'notequal':
			return CriteriaSearch.NotEqual
		elif strCriteria == 'greater':
			return CriteriaSearch.Greater
		elif strCriteria == 'less':
			return CriteriaSearch.Less
		elif CriteriaSearch == 'lessorequal':
			return CriteriaSearch.LessOrEqual
		elif strCriteria == 'greaterorequal':
			return CriteriaSearch.GreaterOrEqual
		elif strCriteria == 'like':
			return CriteriaSearch.Like
		elif strCriteria == 'in':
			return CriteriaSearch.In
		elif strCriteria == 'notin':
			return CriteriaSearch.NotIn
		elif strCriteria == 'beetween':
			return CriteriaSearch.Beetween
		else:
			return CriteriaSearch.Like
class decorators:
	def ajax_required(f):
		def wrap(request, *args, **kwargs):
			if not request.is_ajax():
				return HttpResponseBadRequest()
			return f(request, *args, **kwargs)
			wrap.__doc__=f.__doc__
			wrap.__name__=f.__name__
			return wrap
class query:
	def dictfetchall(cursor):
		"Return all rows from a cursor as a dict"
		columns = [col[0] for col in cursor.description]
		return [
			dict(zip(columns, row))
			for row in cursor.fetchall()
		]
	#	#buat function yang bisa menghasilkan TIsNew,T_Goods_Receive,T_GoodsReturn,T_IsRenew,TIsUsed,TMaintenance,T_GoodsLending
	#untuk mendapatkan jumlah yang benar dengan barang yang masuk kategory bekas(used) 
	#maka harus di cari dulu berapa yang bekasnya, bekas --->barang yang sudah masuk ke table goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost,maentenance

	#TIsNew diperoleh Total goods receive detail - Count group by fk_goods(union goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost
	#buat query union untuk mendapatkan barang mana saja yang sudah masuk barang bekas
	Query = """SELECT FK_goods,TypeApp,SerialNumber na_goods_outwards \
			UNION \
			SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_Lending \
			UNION \
			SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_return \
			UNION \
			SELECT FK_Goods,TypeApp,SerialNumber FROM na_maintenance \
			UNION \
			SELECT FK_Goods,TypeApp,SerialNumber FROM na_disposal \
			UNION
			SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_lost """

	#Query = """SELECT ngr.FK_goods,ngd.TypeApp,ngd.serialnumber,isReceive = 1,IsOutwards = 0,IsLending = 0,IsReturn = 0,IsMaintenance = 0,IsDisposal = 0,IsLost = 0 FROM na_goods_receive ngr INNER JOIN ngd ON ngr.IDApp = ngd.FKApp \
	#		UNION \
	#		SELECT FK_goods,TypeApp,SerialNumber,IsReceive = 0,IsOutwards = 1,IsLending = 0,IsReturn = 0,IsMaintenance,IsDisposal = 0,IsLost = 0 FROM na_goods_outwards \
	#		UNION \
	#		SELECT FK_Goods,TypeApp,SerialNumber,IsReceive = 0,IsOutwards = 0,IsLending = 1,IsReturn = 0,IsMaintenance,IsDisposal = 0,IsLost = 0 FROM na_goods_Lending \
	#		UNION \
	#		SELECT FK_Goods,TypeApp,SerialNumber,IsReceive = 0,IsOutwards = 0,IsLending = 1,IsReturn = 0,IsMaintenance,IsDisposal = 0,IsLost = 0 FROM na_maintenance \
	#		UNION \
	#		SELECT """
#	SELECT rows_changed
#FROM information_schema.table_statistics
#WHERE table_schema = 'na_m_s' AND table_name IN('n_a_goods_lending','n_a_goods_outwards','n_a_goods_receive_detail','n_a_goods_return','n_a_maintenance')
class commonFunct:
	def str2bool(v):
		return v.lower() in ("yes", "true", "t", "1")