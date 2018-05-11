from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsLending
from django.core import serializers
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
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
	populate_combo.append({'label':'Responsible By','columnName':'responsibleby','dataType':'varchar'})	
	populate_combo.append({'label':'Goods From','columnName':'refgoodsfrom','dataType':'varchar'})
	populate_combo.append({'label':'IsNew','columnName':'isnew','dataType':'boolean'})
	populate_combo.append({'label':'Status','columnName':'status','dataType':'varchar'})
	populate_combo.append({'label':'Created By','columnName':'createdby','dataType':'varchar'})
	populate_combo.append({'label':'Created Date','columnName':'createddate','dataType':'datetime'})
	populate_combo.append({'label':'Date Returned','columnName':'datereturn','dataType':'datetime'})		
	#populate_combo.append({'label':'Modified By','columnName':'modifiedby','dataType':'varchar'})
	#populate_combo.append({'label':'Modified Date','columnName':'modifieddate','dataType':'datetime'})
	return render(request,'app/Transactions/NA_F_Goods_Lending.html',{'populateColumn':populate_combo})
	#Goods Name,Goods Type,Serial Number,Lent By,Sent By,Lent Date,Interest,Goods From,IsNew,Status,Created By,CreatedDate
def ShowCustomFilter(request):
	#idapp,no,goods,goodstype,serialnumber,lentby,sentby,lentdate,interests,responsibleby,refgoodsfrom,isnew,status,descriptions,createdby,createddate
	cols = []
	cols.append({'name':'goods','value':'goods','selected':'True','dataType':'varchar','text':'Goods name'})
	cols.append({'name':'goodstype','value':'goodstype','selected':'','dataType':'varchar','text':'Goods type'})
	cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
	cols.append({'name':'lentby','value':'lentby','selected':'','dataType':'varchar','text':'Lent By'})
	cols.append({'name':'sentby','value':'sentby','selected':'','dataType':'varchar','text':'Sent  By'})
	cols.append({'name':'lentdate','value':'lentdate','selected':'','dataType':'datetime','text':'Date Lent'})
	cols.append({'name':'datereturn','value':'datereturn','selected':'','dataType':'datetime','text':'Date Returned'})
	cols.append({'name':'interests','value':'interests','selected':'','dataType':'varchar','text':'Interest of Lending'})
	cols.append({'name':'responsibleby','value':'responsibleby','selected':'','dataType':'varchar','text':'Responsible by'})

	cols.append({'name':'refgoodsfrom','value':'refgoodsfrom','selected':'','dataType':'varchar','text':'Reference goods from'})
	cols.append({'name':'isnew','value':'isnew','selected':'','dataType':'boolean','text':'Is New'})
	cols.append({'name':'refgoodsfrom','value':'refgoodsfrom','selected':'','dataType':'varchar','text':'Reference goods from'})
	cols.append({'name':'status','value':'status','selected':'','dataType':'int','text':'Status Lent'})
	cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'descriptions/Remark'})
	cols.append({'name':'createdby','value':'createdby','selected':'','dataType':'varchar','text':'Created By'})
	cols.append({'name':'createddate','value':'createddate','selected':'','dataType':'datetime','text':'Created Date'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols})
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
			NAData = NAGoodsLending.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsLending.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		#column idapp,goods,goodstype,serialnumber,lentby,sentby,lentdate,interests,responsibleby,refgoodsfrom,isnew,status,descriptions,createdby,createddate
		i = 0;
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['goodstype'],row['serialnumber'],row['lentby'],row['sentby'],row['lentdate'],row['datereturn'],row['interests'], \
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
		statuscode = 200
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
	
		#check reference data
		result = NAGoodsLending.objects.Delete(IDApp,request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
		return HttpResponse(json.dumps({'message':result},cls=DjangoJSONEncoder),status = statuscode, content_type='application/json') 
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getInterest(request):
	if(request.is_ajax()):
		IvalueKey =  request.GET.get('term')
		dataRows = NAGoodsLending.objects.getInterest(IvalueKey)
		results = []
		for datarow in dataRows:
			JsonResult = {}
			JsonResult['id'] = datarow['interests']
			JsonResult['label'] = datarow['interests']
			JsonResult['value'] = datarow['interests']
			results.append(JsonResult)
		data = json.dumps(results,cls=DjangoJSONEncoder)
		return HttpResponse(data, content_type='application/json')
	else:
		return HttpResponse(content='',content_type='application/json')
#def getCurrentDataModel(request,form):
#	return{
@ensure_csrf_cookie
def ShowEntry_Lending(request):
	authentication_classes = []
	status = 'Add'
	initializationForm={}
	statuscode = 200
	data = None
	hasRefData = False
	try:
		status = 'Add' if request.GET.get('status') == None else request.GET.get('status')	
		if request.POST:
			data = request.body
			data = json.loads(data)
			
			status = data['status']
			form = NA_Goods_Lending_Form(data)
			resul = ''
			if form.is_valid():
				form.clean()
				data.update(isnew=strtobool(str(data['isnew'])))
				data.update(fk_maintenance=(None if int(data['fk_maintenance']) == 0 else data['fk_maintenance']))
				data.update(fk_return=(None if int(data['fk_return']) == 0 else data['fk_return']))
				data.update(fk_currentapp=(None if int(data['fk_currentapp']) == 0 else  data['fk_currentapp']))
				data.update(fk_receive=(None if int(data['fk_receive']) == 0 else data['fk_receive']))
				if status == 'Add':	
					data.update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					result = NAGoodsLending.objects.SaveData(data,StatusForm.Input)
				elif status == 'Edit':
					data.update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					if NAGoodsLending.objects.HasReference(data['idapp']):
						result = NAGoodsLending.objects.SaveData(data,StatusForm.Edit)
						return  HttpResponse(json.dumps({'message':'Can not edit data data\Data has child-referenced'}),status = statuscode, content_type='application/json')                       
				
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				if result != 'success':
					statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
		if status == 'Add':
			form = NA_Goods_Lending_Form(initial=initializationForm)
			form.fields['hasRefData'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/NA_Entry_Goods_Lending.html', {'form' : form})
		elif status == 'Edit' or status == 'Open':
			IDApp = request.GET.get('idapp')
			Ndata = NAGoodsLending.objects.getData(IDApp)
			Ndata = Ndata[0]
			Ndata.update(idapp=IDApp)
			Ndata.update(hasRefData=commonFunct.str2bool(str(Ndata['hasRefData'])))
			Ndata.update(initializeForm=json.dumps(Ndata,cls=DjangoJSONEncoder))
			form = NA_Goods_Lending_Form(data=Ndata)
			return render(request, 'app/Transactions/NA_Entry_Goods_Lending.html', {'form' : form})
			#get data
			#/idapp, fk_goods, isnew, goods, idapp_fk_goods, fk_employee, idapp_fk_employee, fk_employee_employee
		 #   //datelending, fk_stock, fk_responsibleperson, idapp_fk_responsibleperson, fk_responsibleperson_employee,
   #         //interests, fk_sender, idapp_fk_sender, fk_sender_employee, statuslent, descriptions, typeapp, serialnumber,
		 #   //brandvalue, fk_maintenance, fk_return, fk_currentapp, fk_receive,  lastinfo, initializeForm, hasRefData
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
@ensure_csrf_cookie
def	HasExists(request):
	try:#check if exists the same data to prevent users double input,parameter data to check FK_goods,datereceived,totalpurchase
		authentication_classes = []
		data = request.body
		data = json.loads(data)
		idapp_fk_goods = data['idapp_fk_goods']
		serialnumber = data['serialnumber']
		datelent = data['datelent']
		statuscode = 200;

		if NAGoodsLending.objects.hasExists(idapp_fk_goods,serialnumber,datelent):
			statuscode = 200
			return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
		return HttpResponse(json.dumps({'message':'OK'}),status = statuscode, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getLastTransGoods(request):
	serialNO = request.GET.get('serialno')
	try:
		result = NAGoodsLending.objects.getLastTrans(serialNO)
		#idapp,itemcode,goodsname,brandname,typeapp,lastInfo,fkreturn,fklending,fkoutwards,fkmaintenance,fkdisposal,fklost
		return HttpResponse(json.dumps({'idapp':result[0],'fk_goods':result[1],'goodsname':result[2],'brandname':result[3],'type':result[4],
								  'lastinfo':result[5],'fk_receive':result[6],'fk_return':result[7],'fk_lending':result[8],'fk_outwards':[9],'fk_maintenance':result[10],
								  }),status = 200, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getGoodsWithHistory(request):
	try:
		searchText = request.GET.get('searchData')
		PageSize = request.GET.get('rows', '')
		PageIndex = request.GET.get('page', '1')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		NAData = NAGoodsLending.objects.getBrandForLending(searchText,str(Isidx),Isord,PageSize,PageIndex, request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		i = 0;#idapp,itemcode,goods
		for row in dataRows:
			i+=1
			#idapp,NO,fk_goods,goodsname,brandName,type,serialnumber,lastinfo,fk_receive,fk_outwards,fk_lending,fk_return,fk_maintenance,
			datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['fk_goods'],row['goodsname'],row['brandname'],row['type'],
							row['serialnumber'],row['lastinfo'],row['fk_receive'],row['fk_outwards'],row['fk_lending'],row['fk_return'],row['fk_maintenance'],]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(PageSize) else (math.ceil(float(totalRecord/int(PageSize)))) # round up to next number
		results = {"page": int(PageIndex),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
class NA_Goods_Lending_Form(forms.Form):
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
																						 'placeholder': 'employee who lends','data-value':'employee who lends','tittle':'employee who lends is required'}))
	
	datelending = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':6,
                                   'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter date lent','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	#datereturn = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':6,
 #                                  'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter date lent','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	fk_stock = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_responsibleperson = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
                                   'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':4,
                                   'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	idapp_fk_responsibleperson = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	fk_responsibleperson_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																						 'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	interests = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:355px;display:inline-block;','tabindex':5,
																						 'placeholder': 'Interest Of','data-value':'Interest Of','tittle':'Interest is required'}))
	fk_sender = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
                                   'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':3,
                                   'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	idapp_fk_sender = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_sender_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																			 'placeholder': 'employee who sends','data-value':'employee who sends','tittle':'employee who sends is required'}))
	statuslent = forms.ChoiceField(widget=forms.Select(attrs={
                                   'class': 'NA-Form-Control','style':'width:90px;display:inline-block'}),choices=(('L', 'Lent'),('R','Returned')),required=False)
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about lending goods',
																			'data-value':'descriptions about lending goods','title':'Remark any other text to describe transactions','tabindex':7}),required=False)
	typeapp = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False)
	serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':2,
                                   'placeholder': 'Serial Number','data-value':'Serial Number','tittle':'Please enter Serial Number if exists'}),required=True)
	brandvalue = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)
	fk_maintenance = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_return = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_currentapp = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_receive = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	#fk_disposal = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	#fk_lost = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	lastinfo = forms.CharField(widget=forms.HiddenInput(),required=False)#value ini di peroleh secara hard code dari query jika status = edit/open
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)
	def clean(self):
		cleaned_data = super(NA_Goods_Lending_Form,self).clean()
		fk_employee = self.cleaned_data['fk_employee']
		datelending = self.cleaned_data['datelending']
		fk_responsibleperson = self.cleaned_data['fk_responsibleperson']
		interests = self.cleaned_data['interests']
		fk_sender = self.cleaned_data['fk_sender']
		serialnumber = self.cleaned_data['serialnumber']
	def __init__(self,*args,**kwargs):
		super(NA_Goods_Lending_Form,self).__init__(*args, **kwargs)
		self.initial['statuslent'] = 'L'
		self.initial['goods'] = ''
		self.initial['brandvalue'] = ''
		self.initial['typeapp'] = ''
		self.initial['hasRefData'] = False
		self.initial['isnew'] = False