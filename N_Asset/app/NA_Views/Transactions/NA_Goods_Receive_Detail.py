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
def entrybatchdetail(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'RefNO','columnName':'refno','dataType':'varchar'})
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'BrandName','columnName':'brandname','dataType':'varchar'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'Warranty','columnName':'warranty','dataType':'decimal'})
	populate_combo.append({'label':'End Of Warranty','columnName':'endofwarranty','dataType':'datetime'})
	populate_combo.append({'label':'Price','columnName':'price','dataType':'decimal'})
	return render(request,'app/Transactions/NA_F_Goods_Receive_Batch_Detail.html',{'populateColumn':populate_combo})

def getData(request):
	statuscode = 200
	try:
		refno = request.GET.get('refno')
		#get header data
		NAData = NA_GoodsReceive_detail.objects.getHeaderData(refno)
		#"""
		#return idapp,idapp_fk_goods,goods_desc,datereceived,supliername,employee_receieved,employee_pr,totalpurchase,totalreceived
		#"""
		if len(NAData) <= 0:
			raise Exception('can not find such reference number')
		NAData = NAData[0]
		NAData.update(dataForGridDetail={})
		FKApp = NAData['idapp']
		idapp_fk_goods = NAData['idapp_fk_goods']
		NADataDetail = NA_GoodsReceive_detail.objects.getDetailData(FKApp,idapp_fk_goods)
		NAData.update(dataForGridDetail=json.dumps(NADataDetail,cls=DjangoJSONEncoder))
		Result = json.dumps(NAData,cls=DjangoJSONEncoder)
		return HttpResponse(Result,status = statuscode, content_type='application/json') 
	except Exception as e :
		return HttpResponse(json.dumps({'message': repr(e)}),status = 500, content_type='application/json')