from enum import Enum
from datetime import date
from datetime import datetime
from django.db import connection
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

class commonFunct:
	def str2bool(v):
		return v.lower() in ("yes", "true", "t", "1")

		#	#buat function yang bisa menghasilkan TIsNew,T_Goods_Receive,T_GoodsReturn,T_IsRenew,TIsUsed,TMaintenance,TotalSpare
	#untuk mendapatkan jumlah yang benar dengan barang yang masuk kategory bekas(used) 
	#maka harus di cari dulu berapa yang bekasnya, bekas --->barang yang sudah masuk ke table goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost,maentenance

	#TIsNew diperoleh Total goods receive detail - Count (group by fk_goods(union goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost)
	#buat query union untuk mendapatkan barang mana saja yang sudah di pakai
	def getTotalGoods(FKGoods,cur):
		"""FUNCTION untuk mengambil total-total data berdasarkan FK_goods yang di parameter, function ini akan mereturn value
		:param int FKGoods: idapp_fk_goods
		:param object cur: cursor active
		totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare dalam bentuk tuples
		totalNew adalah total barang yang baru yang belum pernah di pakai
		totalUsed adalah total barang yang sudah di keluarkan/terpakai
		totalReceived adalah total barang yang di terima
		totalReturn adalah total barang yang di kembalikan pakai query count distinct
		totalRenew adalah ketersedian barang yang sudah di maintain/perbaiki dan bisa di ambil untuk baik di pinjam atau inventaris
		totalMaintenance adalah total barang yang sedang di perbaiki 
		totalSpare adalah total cadangan barang yang akan di pakai untuk peminjaman barang
		totalSpare akan terjadi bila ada transaksi di n_a_goods_lending dan status sudah R(returned)"""
		totalNew = 0;totalUsed = 0;totalReceived =0;totalReturn = 0;totalRenew = 0;totalMaintenance = 0;TotalSpare = 0;
		if(cur is None):
			cur = connection.cursor()

		Query = "DROP TEMPORARY TABLE IF EXISTS T_Goods_Used"
		cur.execute(Query)		
		Query = """"CREATE TEMPORARY TABLE T_Goods_Used \
				(INDEX cmpd_key (SerialNumber, FK_Goods))ENGINE=MyISAM AS(SELECT FK_goods,TypeApp,SerialNumber na_goods_outwards WHERE FK_goods = %(FK_Goods)s \
				UNION \
				SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_Lending WHERE FK_goods = %(FK_Goods)s  \
				UNION \
				SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_return WHERE FK_goods = %(FK_Goods)s\
				UNION \
				SELECT FK_Goods,TypeApp,SerialNumber FROM na_maintenance WHERE FK_goods = %(FK_Goods)s\
				UNION \
				SELECT FK_Goods,TypeApp,SerialNumber FROM na_disposal WHERE FK_goods = %(FK_Goods)s\
				UNION
				SELECT FK_Goods,TypeApp,SerialNumber FROM na_goods_lost) WHERE FK_goods = %(FK_Goods)s )"""
		cur.execute(Query,{'FK_Goods':FKGoods})
	
		#get totalused and totalReceived
		Query = """SELECT Rec.Total AS totalReceived,Rec.Total - Used.Total AS TotalNew,Used.Total AS TotalUsed FROM (SELECT ngr.FK_Goods,COUNT(ngr.FK_goods) AS Total FROM n_a_goods_receive INNER JOIN n_a_goods_receive_detail ngd \
					ON ngr.FK_goods = ngd.FKApp GROUP BY ngr.FK_Goods WHERE ngr.FK_goods = %(FK_Goods)s)T_Receive INNER JOIN (SELECT FK_Goods,COUNT(FK_Goods) AS Total FROM T_Goods_Used GROUP BY  FK_Goods)T_Used \
					ON Rec.FK_Goods = Used.FK_Goods """
		row = cur.execute(Query)
		totalNew = int(row['TotalNew'])
		totalReceived = int(row['totalReceived'])
		totalUsed = int(row['TotalUsed'])	
		
		#totalReturn 
		Query = """SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_goods_return WHERE FK_Goods = %(FK_Goods)s )C """
		cur.execute(Query,{'FK_Goods':FKGoods})
		totalReturn = int(cur.fetchone())

		#totalRenew
		#TotalRenew diperoleh di n_a_maintenance kondisi IsSucced = 1, dan belum ada di n_a_goods_lending dan n_a_goods_outwards,dan  n_a_disposal
		Query = """SELECT COUNT(mt.FK_Goods) FROM (SELECT DISTINCT mt.FK_Goods,mt.TypeApp,mt.SerialNumber FROM n_a_maintenance mt WHERE mt.IsSucced = 1 AND mt.IsFinished = 1 \
					AND NOT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_Maintenance = mt.IDApp)\
					AND NOT EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_FromMaintenance = mt.IDApp) \
					AND NOT EXISTS(SELECT IDApp FROM n_a_disposal WHERE FK_Maintenance = mt.IDApp) \
					AND mt.FK_Goods = %(FK_Goods)s)C """
		cur.execute(Query,{'FK_Goods':FKGoods})
		totalRenew = int(cur.fetchone())
		#TMaintenance
		#TMaintenance diperoleh di n_a_maintenance kondisi  IsFinished = 0
		Query = " SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_maintenance WHERE IsFinished = 0 AND FK_Goods = %(FK_Goods)s)C "
		cur.execute(Query,{'FK_Goods':FKGoods})
		totalMaintenance = int(cur.fetchone())		

		#TotalSpare
		#TotalSpare diperoleh di n_a_goods_lending dengan kondisi status = L dan tidak ada di n_a_goods_lost
		Query = """SELECT COUNT(FK_goods) FROM (SELECT DISCTINCT nl.FK_goods,nl.TypeApp,nl.SerialNumber FROM n_a_goods_lending nl WHERE nl.Status = 'R' \
					AND NOT EXISTS(SELECT FK_Goods FROM n_a_maintenance WHERE SerialNumber = nl.SerialNumber AND IsFinished = 0) \
					AND NOT EXISTS(SELECT FK_Goods FROM n_a_goods_outwards WHERE FK_Lending = nl.IDApp) \
					AND NOT EXISTS(SELECT FK_Goods FROM n_a_disposal WHERE SerialNumber = nl.SerialNumber) AND nl.FK_Goods =  %(FK_Goods)s)C """ 
		cur.execute(Query,{'FK_Goods':FKGoods})
		TotalSpare = int(cur.fetchone())
		
		cur.close();
		return(totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare)		  
		#dengan status
		#query = """SELECT COUNT
#FROM information_schema.table_statistics
#WHERE table_schema = 'na_m_s' AND table_name IN('n_a_goods_lending','n_a_goods_outwards','n_a_goods_receive_detail','n_a_goods_return','n_a_maintenance')