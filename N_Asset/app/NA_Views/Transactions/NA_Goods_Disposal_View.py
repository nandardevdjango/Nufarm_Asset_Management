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
	#idapp,goods,type,serialnumber,ishasvalue,bookvalue,datedisposal,afterrepair,lastrepairFrom,issold,sellingprice,proposedby,acknowledgeby,approvedby,descriptions,createdby,createddate					
	# colnames datagrid
	#colNames: ['idapp', 'NO', 'Goods Name', 'Type', 'Serial Number', 'Date Removal', 'Has Repaired', 'Last Repaired From', 'Is Sold','Selling Price',
	#'Proposed By', 'Acknowledged By', 'Approved By','Descriptions', 'Created Date', 'Created By'],
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Goods Type','columnName':'typeapp','dataType':'varchar'})
	populate_combo.append({'label':'Serial Number','columnName':'serialnumber','dataType':'varchar'})
	populate_combo.append({'label':'Date Disposal/Removal','columnName':'datedisposal','dataType':'datetime'})
	populate_combo.append({'label':'afterrepair','columnName':'afterrepair','dataType':'boolean'})
	populate_combo.append({'label':'Last Repaired From','columnName':'lastrepairFrom','dataType':'varchar'})
	populate_combo.append({'label':'IsSold','columnName':'issold','dataType':'boolean'})
	populate_combo.append({'label':'Selling Price ','columnName':'sellingprice','dataType':'decimal'})
	populate_combo.append({'label':'Proposed By','columnName':'proposedby','dataType':'varchar'})
	populate_combo.append({'label':'Acknowledged By','columnName':'acknowledgeby','dataType':'varchar'})	
	populate_combo.append({'label':'Approved By','columnName':'approvedby','dataType':'varchar'})
	populate_combo.append({'label':'IsNew','columnName':'isnew','dataType':'boolean'})
	populate_combo.append({'label':'Created By','columnName':'createdby','dataType':'varchar'})
	populate_combo.append({'label':'Created Date','columnName':'createddate','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Disposal.html',{'populateColumn':populate_combo})