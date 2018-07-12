from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NADisposal
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
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

def NA_Goods_Disposal(request):
	populate_combo = []
	#jieun heula query
	#column idapp,NO,goods,goodstype,serialnumber,    <-->
	#idapp,goods,type,serialnumber,bookvalue,datedisposal,afterrepair,lastrepairFrom,issold,sellingprice,proposedby,acknowledgeby,approvedby,descriptions,createdby,createddate					
	# colnames datagrid
	#colNames: ['idapp', 'NO', 'Goods Name', 'Type', 'Serial Number', 'Date Removal', 'Has Repaired', 'Last Repaired From', 'Is Sold','Selling Price',
	#'Proposed By', 'Acknowledged By', 'Approved By','Descriptions', 'Created Date', 'Created By'],
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Goods Type','columnName':'typeapp','dataType':'varchar'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'Book Value','columnName':'bookvalue','dataType':'decimal'})
	populate_combo.append({'label':'Date Disposal/Removal','columnName':'datedisposal','dataType':'datetime'})
	populate_combo.append({'label':'afterrepair','columnName':'afterrepair','dataType':'boolean'})
	populate_combo.append({'label':'Last Repaired From','columnName':'lastrepairFrom','dataType':'varchar'})
	populate_combo.append({'label':'IsSold','columnName':'issold','dataType':'boolean'})
	populate_combo.append({'label':'Selling Price ','columnName':'sellingprice','dataType':'decimal'})
	populate_combo.append({'label':'Proposed By','columnName':'proposedby','dataType':'varchar'})
	populate_combo.append({'label':'Acknowledged By','columnName':'acknowledgeby','dataType':'varchar'})	
	populate_combo.append({'label':'Approved By','columnName':'approvedby','dataType':'varchar'})
	populate_combo.append({'label':'Created By','columnName':'createdby','dataType':'varchar'})
	populate_combo.append({'label':'Created Date','columnName':'createddate','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Disposal.html',{'populateColumn':populate_combo})

def NA_Goods_Disposal_Search(request):
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
			NAData = NADisposal.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NADisposal.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		#column idapp,goods,type,serialnumber,bookvalue,datedisposal,afterrepair,lastrepairfrom,issold,sellingprice,proposedby,acknowledgeby,approvedby,descriptions,createdby,createddate	
		i = 0;
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['idapp'], 'cell' :[row['idapp'],i,row['goods'],row['goodstype'],row['serialnumber'],row['bookvalue'],row['datedisposal'],
						row['afterrepair'],row['lastrepairfrom'],row['issold'],row['sellingprice'],row['proposedby'],row['acknowledgeby'],
				row['approvedby'],row['descriptions'],row['createdby'],row['createddate']]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')