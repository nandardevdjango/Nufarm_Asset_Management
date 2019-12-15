from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NA_GoodsReceive_detail, goods,NASupplier,Employee
from django.core import serializers
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import Data
from NA_DataLayer import common
#from NA_DataLayer.jqgrid import JqGrid
from django.conf import settings 
from NA_DataLayer.common import decorators
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from distutils.util import strtobool
from decimal import Decimal
import math
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from NA_Models.models import NAGoodsReceive
from NA_DataLayer.Transactions import NA_Goods_Receive_BR
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1","True","Yes")

@ensure_csrf_cookie #send csrf token to page in the cookie to protect whenever user post request
def entrybatchdetail(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	#populate_combo.append({'label':'RefNO','columnName':'refno','dataType':'varchar'})
	#populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'BrandName','columnName':'brandname','dataType':'varchar'})
	populate_combo.append({'label':'Price','columnName':'priceperunit','dataType':'decimal'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'Warranty','columnName':'warranty','dataType':'decimal'})
	populate_combo.append({'label':'End Of Warranty','columnName':'endofwarranty','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Receive_Batch_Detail.html',{'populateColumn':populate_combo})

def getData(request):
	statuscode = 200
	try:
		refno = request.GET.get('refno')
		#get header data
		NAData = NA_GoodsReceive_detail.objects.getHeaderData(refno)
		#"""
		#return 'idapp', 'idapp_fk_goods', 'refno', 'fk_goods', 'Goods Name', 'economiclife', 'Date Received', 'fk_supplier', 'Suplier Name', 'idapp_fk_receivedby', 'fk_receivedby',
						#'Received By', 'idapp_fk_pr_by','fk_pr_by','Purchase Request By', 'Total Purchase', 'Total Receieved','descriptions'
		#"""
		if len(NAData) <= 0:
			raise Exception('can not find such reference number')
		NAData = NAData[0]
		NAData.update(dataForGridDetail={})
		FKApp = NAData['idapp']
		idapp_fk_goods = NAData['idapp_fk_goods']
		NADataDetail = NA_GoodsReceive_detail.objects.getDetailData(FKApp,idapp_fk_goods)
		rows = []			
		i = 0
		for row in NADataDetail:
			i = i+1
			datarow = {'idapp':row['IDApp'],'fkapp':row['FK_App'], 'no':i,'brandname':row['BrandName'],'priceperunit':row['PricePerUnit'], \
				'typeapp':row['TypeApp'],'serialnumber':row['SerialNumber'],'warranty':row['Warranty'],'endofwarranty':row['EndOfWarranty'], \
				'createdby':row['CreatedBy'],'createddate':row['CreatedDate'],'modifiedby':row['ModifiedBy'],'modifieddate':row['ModifiedDate'],'HasRef':str2bool(str(row['HasRef'])),'isnew':'0','isdeleted':'0','isdirty':'0'}
			rows.append(datarow)					
		dataForGridDetail = rows
		NAData.update(dataForGridDetail=json.dumps(rows,cls=DjangoJSONEncoder))
		Result = json.dumps(NAData,cls=DjangoJSONEncoder)
		return HttpResponse(Result,status = statuscode, content_type='application/json') 
	except Exception as e :
		return HttpResponse(json.dumps({'message': repr(e)}),status = 500, content_type='application/json')

@ensure_csrf_cookie
def saveData(request):
	authentication_classes = []
	data = request.body
	#import ipdb
	
	Odata = json.loads(data, parse_float=Decimal)
	data = Odata['headerData'][0]
	
	ChangedHeader = str2bool(str(Odata['hasChangedHeader']))
	ChangedDetail = str2bool(str(Odata['hasChangedDetail']))
	dataDetail = Odata['dataForGridDetail']
	#ipdb.set_trace()
	totalReceived = data['totalreceived'];	
	desc = '('		
			
	#dataDetail = object_list
	if len(dataDetail) > 0:
		detCount = len(dataDetail)
		#build descriptions
		for i in range(detCount):
			brandname = dataDetail[i]['brandname']
			if brandname == '':
				continue
			desc += brandname + ', Type : ' + dataDetail[i]['typeapp'] + ', SN : ' + dataDetail[i]['serialnumber']
			if i <detCount -1:
				desc += ', '
			dataDetail[i].update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
			dataDetail[i].update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
	desc += ')'
	data.update(dataForGridDetail=dataDetail)
	#data['dataForGridDetail'] = dataForGridDetail
	data.update(descbysystem=desc)
	data.update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
	data.update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
	if len(dataDetail) != totalReceived:
		totalReceived = len(dataDetail)
	data.update(totalreceived=totalReceived)
	hasRefData = NAGoodsReceive.objects.hasReference({'idapp':data['idapp'],'idapp_fk_goods':data['idapp_fk_goods'], 'datereceived':data['datereceived']},None)
	data.update(hasRefData=hasRefData)
	data.update(hasChangedHeader=ChangedHeader)
	data.update(hasChangedDetail=ChangedDetail)
	Oresult = (Data.Success,)
	try:
		result = NAGoodsReceive.objects.SaveData(data,StatusForm.Edit)
		if result != 'success':
			Oresult = (None,'Unhandled error')
	except NAError as e:
		Oresult = NAErrorHandler.handle(err=e)
	return common.commonFunct.response_default(Oresult)
	