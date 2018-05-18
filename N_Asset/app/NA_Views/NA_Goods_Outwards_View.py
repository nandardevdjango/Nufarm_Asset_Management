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
class NA_Goods_Outwards_Form(forms.Form):
    idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_goods = forms.CharField(widget=forms.HiddenInput(),required=False)
    isnew = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False,initial=False)
    goods = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																					    'placeholder': 'goods name','data-value':'goods name','tittle':'goods name is required'}))
    idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_employee = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
                                    'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':2,
                                    'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
    idapp_fk_employee = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_employee_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																						    'placeholder': 'employee who uses goods','data-value':'employee who uses goods','tittle':'employee who uses goods is required'}))
    daterequest = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':6,
                                    'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter date request','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
    datereleased = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':6,
                                'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter date lent','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
  

    fk_responsibleperson = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
                                    'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':4,
                                    'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
    idapp_fk_responsibleperson = forms.IntegerField(widget=forms.HiddenInput(),required=False)

    fk_responsibleperson_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																						    'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
    fk_sender = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
                                    'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':3,
                                    'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
    idapp_fk_sender = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_sender_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																			    'placeholder': 'employee who sends','data-value':'employee who sends','tittle':'employee who sends is required'}))
    descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about lending goods',
  																	    'data-value':'descriptions about lending goods','title':'Remark any other text to describe transactions','tabindex':7}),required=False)
    fk_stock = forms.IntegerField(widget=forms.HiddenInput(),required=False)

    #info
    fk_usedemployee = forms.CharField(max_length=50,widget=forms.HiddenInput(),required=False)
    idapp_fk_usedemployee = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_usedemployee_employee = forms.CharField(max_length=100, widget=forms.HiddenInput(),required=False)
    lastinfo = forms.CharField(widget=forms.HiddenInput(),required=False)#value ini di peroleh secara hard code dari query jika status = edit/open
    typeapp = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False)
    serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':2,
                                    'placeholder': 'Serial Number','data-value':'Serial Number','tittle':'Please enter Serial Number if exists'}),required=True)   
    brandvalue = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

    fk_frommaintenance = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_return = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_lending = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_receive = forms.IntegerField(widget=forms.HiddenInput(),required=False)
  
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
    hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)