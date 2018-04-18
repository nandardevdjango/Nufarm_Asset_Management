from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive, goods,NASuplier,Employee,NAGoodsLending
from django.core import serializers
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
#from NA_DataLayer.jqgrid import JqGrid
from django.conf import settings 
from NA_DataLayer.common import decorators
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.utils.safestring import mark_safe
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from distutils.util import strtobool
from decimal import Decimal
import math
def NA_Goods_Lending(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Goods Type','columnName':'typeapp','dataType':'varchar'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'Lent_by','columnName':'lentby','dataType':'varchar'})
	populate_combo.append({'label':'Sent By','columnName':'sentby','dataType':'varchar'})
	populate_combo.append({'label':'Lent Date','columnName':'lentdate','dataType':'datetime'})
	populate_combo.append({'label':'intererest','columnName':'intererests','dataType':'varchar'})
	populate_combo.append({'label':'Responsible By','columnName':'responsibleby','dataType':'datetime'})	
	populate_combo.append({'label':'Goods From','columnName':'refgoodsfrom','dataType':'varchar'})
	populate_combo.append({'label':'IsNew','columnName':'isnew','dataType':'boolean'})
	populate_combo.append({'label':'Status','columnName':'status','dataType':'varchar'})
	populate_combo.append({'label':'Created By','columnName':'createdby','dataType':'varchar'})
	populate_combo.append({'label':'Created Date','columnName':'createddate','dataType':'varchar'})	
	#populate_combo.append({'label':'Modified By','columnName':'modifiedby','dataType':'varchar'})
	#populate_combo.append({'label':'Modified Date','columnName':'modifieddate','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Receive.html',{'populateColumn':populate_combo})
	#Goods Name,Goods Type,Serial Number,Lent By,Sent By,Lent Date,Interest,Goods From,IsNew,Status,Created By,CreatedDate
def NA_Goods_Lending_Search(request):
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
			NAData = NAGoodsLending.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsLending.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1][0]
		dataRows = NAData[0]
		rows = []
		#column idapp,goods,goodstype,serialnumber,lentby,sentby,lentdate,interests,responsibleby,refgoodsfrom,isnew,status,descriptions,createdby,createddate
		i = 0;
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['goodstype'],row['serialnumber'],row['lentby'],row['sentby'],row['lentdate'],row['interests'], \
				row['responsibleby'],row['refgoodsfrom'],row['isnew'],row['status'],row['descriptions'],datetime.date(row['createddate']),row['createdby']]}
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def UpdateStatus(request):
	try:
		idapp = request.GET.get('idapp');
		newVal = request.GET.get('newVal');
		updatedby = request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin'
		result = NAGoodsLending.objects.UpdateStatus(idapp,newVal,updatedby)
		if result != 'success':
			statuscode = 500
		return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def Delete(request):
	result = ''
	try:
		statuscode = 200
		#result=NAGoodsReceive.objects.delete(
		data = request.body
		data = json.loads(data)

		IDApp = data['idapp']
		Ndata = NAGoodsReceive.objects.getData(IDApp)[0]
		NAData = {'idapp':IDApp,'idapp_fk_goods':Ndata['idapp_fk_goods'],'datereceived':Ndata['datereceived'],'deletedby':request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin'}
		#check reference data
		result = NAGoodsReceive.objects.delete(NAData)
		return HttpResponse(json.dumps({'message':result},cls=DjangoJSONEncoder),status = statuscode, content_type='application/json') 
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')