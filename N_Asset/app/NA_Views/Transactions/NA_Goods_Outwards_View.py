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
@ensure_csrf_cookie
def ShowEntry_Outwards(request):
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
			result = ''
			if form.is_valid():
				form.clean()
				data.update(isnew=strtobool(str(data['isnew'])))
				data.update(fk_frommaintenance=(None if int(data['fk_frommaintenance']) == 0 else data['fk_frommaintenance']))
				data.update(fk_usedemployee=(None if int(data['fk_usedemployee']) == 0 else data['fk_usedemployee']))
				data.update(fk_return=(None if int(data['fk_return']) == 0 else data['fk_return']))
				data.update(fk_lending=(None if int(data['fk_lending']) == 0 else  data['fk_lending']))
				data.update(fk_receive=(None if int(data['fk_receive']) == 0 else data['fk_receive']))
				if status == 'Add':	
					data.update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					result = NAGoodsOutwards.objects.SaveData(data,StatusForm.Input)
				elif status == 'Edit':
					data.update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					#if NAGoodsLending.objects.HasReference(data['idapp']):
					#	result = NAGoodsLending.objects.SaveData(data,StatusForm.Edit)
					#	return  HttpResponse(json.dumps({'message':'Can not edit data data\Data has child-referenced'}),status = statuscode, content_type='application/json')                       
				
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				if result != 'success':
					statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
		if status == 'Add':
			form = NA_Goods_Outwards_Form(initial=initializationForm)
			form.fields['hasRefData'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/NA_Entry_Goods_Outwards.html', {'form' : form})
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
@ensure_csrf_cookie
def hasExists(request):
	try:#check if exists the same data to prevent users double input,parameter data to check FK_goods,datereceived,totalpurchase
		authentication_classes = []
		data = request.body
		data = json.loads(data)
		idapp_fk_goods = data['idapp_fk_goods']
		serialnumber = data['serialnumber']
		datereq = data['daterequest']
		daterel = data['datereleased']
		statuscode = 200;
		if NAGoodsOutwards.objects.HasExists(idapp_fk_goods,serialnumber,datereq,daterel):
			statuscode = 200
			return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
		return HttpResponse(json.dumps({'message':'OK'}),status = statuscode, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getLastTransGoods(request):
	serialNO = request.GET.get('serialno')
	try:
		result = NAGoodsOutwards.objects.getLastTrans(serialNO)
		#return(idapp,itemcode,goodsname,brandname,typeapp,fk_usedemployee,usedemployee,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance)
		return HttpResponse(json.dumps({'idapp':result[0],'fk_goods':result[1],'goodsname':result[2],'brandname':result[3],'type':result[4],
								  'fk_usedemployee':result[5],'usedemployee':result[6],'lastinfo':result[7],'fk_receive':result[8],'fk_return':result[9],
                                  'fk_lending':result[10],'fk_outwards':[11],'fk_maintenance':result[12],
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
		NAData = NAGoodsOutwards.objects.getBrandForOutwards(searchText,str(Isidx),Isord,PageSize,PageIndex, request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		i = 0;#idapp,itemcode,goods
		for row in dataRows:
			i+=1
			#idapp,NO,fk_goods,goodsname,brandName,type,serialnumber,fk_usedemployee,usedemployee,lastinfo,fk_receive,fk_outwards,fk_lending,fk_return,fk_maintenance,
			datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['fk_goods'],row['goodsname'],row['brandname'],row['type'],
							row['serialnumber'],row['fk_usedemployee'],row['usedemployee'],row['lastinfo'],row['fk_receive'],row['fk_outwards'],row['fk_lending'],row['fk_return'],row['fk_maintenance'],]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(PageSize) else (math.ceil(float(totalRecord/int(PageSize)))) # round up to next number
		results = {"page": int(PageIndex),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e:
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
	serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':2,
									'placeholder': 'Serial Number','data-value':'Serial Number','tittle':'Please enter Serial Number if exists'}),required=True)   
	brandvalue = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

	fk_frommaintenance = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_return = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_lending = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_receive = forms.IntegerField(widget=forms.HiddenInput(),required=False)  
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)

	def clean(self):
		cleaned_data = super(NA_Goods_Outwards_Form,self).clean()
		cleaned_data = super(NA_Goods_Outwards_Form,self).clean()
		fk_employee = self.cleaned_data['fk_employee']
		daterequest = self.cleaned_data['daterequest']
		datereleased = self.clean_data['datereleased']
		fk_responsibleperson = self.cleaned_data['fk_responsibleperson']
		fk_sender = self.cleaned_data['fk_sender']
		serialnumber = self.cleaned_data['serialnumber']
	def __init__(self,*args,**kwargs):
		super(NA_Goods_Outwards_Form,self).__init__(*args, **kwargs)
		self.initial['goods'] = ''
		self.initial['brandvalue'] = ''
		self.initial['typeapp'] = ''
		self.initial['hasRefData'] = False
		self.initial['isnew'] = False
		self.initial['fk_usedemployee'] = ''
		self.initial['usedemployee'] = ''