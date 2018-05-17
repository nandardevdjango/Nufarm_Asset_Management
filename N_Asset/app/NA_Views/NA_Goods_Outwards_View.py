from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsOutwards
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
#from NA_DataLayer.jqgrid import JqGrid
from django.conf import settings 
from NA_DataLayer.common import decorators
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.views.decorators.csrf import ensure_csrf_cookie
from distutils.util import strtobool
from decimal import Decimal
import math
def NA_Goods_Outwards(request):
	populate_combo = []
	#jieun heula query
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Goods Type','columnName':'typeapp','dataType':'varchar'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'For Employee','columnName':'for_employee','dataType':'varchar'})
	populate_combo.append({'label':'Date Requested','columnName':'daterequest','dataType':'datetime'})
	populate_combo.append({'label':'Date Released','columnName':'datereleased','dataType':'datetime'})
	populate_combo.append({'label':'Sender ','columnName':'senderby','dataType':'varchar'})
	populate_combo.append({'label':'Responsible By','columnName':'responsibleby','dataType':'varchar'})	
	populate_combo.append({'label':'Goods From','columnName':'refgoodsfrom','dataType':'varchar'})
	populate_combo.append({'label':'IsNew','columnName':'isnew','dataType':'boolean'})
	populate_combo.append({'label':'Created By','columnName':'createdby','dataType':'varchar'})
	populate_combo.append({'label':'Created Date','columnName':'createddate','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Outwards.html',{'populateColumn':populate_combo})
def NA_Goods_Outwards_Search(request):
	try:
		IcolumnName = request.GET.get('columnName');
		IvalueKey =  request.GET.get('valueKey')
		IdataType =  request.GET.get('dataType')
		Icriteria =  request.GET.get('criteria')
		Ilimit = request.GET.get('rows', '')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
		dataType = ResolveCriteria.getDataType(str(IdataType))
		if(Isord is not None and str(Isord) != '') or(Isidx is not None and str(Isidx) != ''):
			NAData = NAGoodsOutwards.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsOutwards.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		#column idapp,goods,goodstype,serialnumber,daterequest,datereleased,isnew,fk_employee,for_employee,fk_usedemployee,eks_employee,
		#fk_responsibleperson,responsible_by,fk_sender,senderby,fk_stock,refgoodsfrom,descriptions,createdby,createddate
		i = 0;
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['idapp'], 'cell' :[row['idapp'],i,row['goods'],row['goodstype'],row['serialnumber'],row['daterequest'],row['datereleased'],
						row['isnew'],row['fk_employee'],row['for_employee'],row['fk_usedemployee'],row['eks_employee'],row['fk_responsibleperson'],
				row['responsible_by'],row['fk_sender'],row['senderby'],row['fk_stock'],row['refgoodsfrom'],row['descriptions'],row['createddate'],row['createdby']]}
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')