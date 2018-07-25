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

#goods,goodstype,serialnumber,islost,sellingprice,bookvalue,datedisposal,refgoodsfrom
#issold,proposedby,acknowledgeby,approvedby,createdby,createddate
def ShowCustomFilter(request):
	cols = []
	cols.append({'name':'goods','value':'goods','selected':'True','dataType':'varchar','text':'Goods name'})
	cols.append({'name':'goodstype','value':'goodstype','selected':'','dataType':'varchar','text':'Goods type'})
	cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
	cols.append({'name':'datedisposal','value':'datedisposal','selected':'','dataType':'datetime','text':'Date Requested'})
	cols.append({'name':'sellingprice','value':'sellingprice','selected':'','dataType':'decimal','text':'Selling Price'})
	



	cols.append({'name':'responsibleby','value':'responsibleby','selected':'','dataType':'varchar','text':'Responsible by'})
	cols.append({'name':'sentby','value':'sentby','selected':'','dataType':'varchar','text':'Sent  By'})
	cols.append({'name':'islost','value':'islost','selected':'','dataType':'boolean','text':'Is New'})
	cols.append({'name':'refgoodsfrom','value':'refgoodsfrom','selected':'','dataType':'varchar','text':'Reference goods from'})
	cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'descriptions/Remark'})
	cols.append({'name':'createdby','value':'createdby','selected':'','dataType':'varchar','text':'Created By'})
	cols.append({'name':'createddate','value':'createddate','selected':'','dataType':'datetime','text':'Created Date'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols})
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
			datarow = {"id" :row['idapp'], 'cell' :[row['idapp'],i,row['goods'],row['goodstype'],row['serialnumber'],row['bookvalue'],row['datedisposal'],row['islost'],
						row['refgoodsfrom'],row['issold'],row['sellingprice'],row['proposedby'],row['acknowledgeby'],
				row['approvedby'],row['descriptions'],row['createdby'],row['createddate']]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
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
		NAData = NADisposal.objects.getBrandForDisposal(searchText,str(Isidx),Isord,PageSize,PageIndex, request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
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

def getLastTransGoods(request):
	serialNO = request.GET.get('serialno')
	try:
		result = NADisposal.objects.getLastTrans(serialNO)
		#return(idapp_fk_goods,itemcode,goodsname,brandname,typeapp,islost,fk_usedemployee, usedemployee,fk_acc_fa,bookvalue,lastInfo,fkmaintenance,fkreturn,fklending,fkoutwards)
		return HttpResponse(json.dumps({'idapp':result[0],'fk_goods':result[1],'goodsname':result[2],'brandname':result[3],'type':result[4],
								  'islost':result[5],'fk_usedemployee':result[6],'usedemployee':result[7],'fk_acc_fa':result[8],'bookvalue':result[9],
								  'lastinfo':result[10],'fk_maintenance':result[11],'fk_return':result[12],
                                  'fk_lending':result[13],'fk_outwards':result[14],
								  }),status = 200, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')

def getBookValue(request):
	statuscode = 200
	data = request.body
	data = json.loads(data)
	serialNO = data['serialno']
	idappFKGoods = data['idapp_fk_goods']
	dateDisposal = datetime.date.today() if data['datedisposal'] is None else data['datedisposal']
	try:
		result = NADisposal.objects.getBookValue(None,idapp= idappFKGoods,SerialNo=serialNO,DateDisposal=dateDisposal)
		if result is None :
			statuscode = 500
			return HttpResponse(json.dumps({'message':'unknown book value'}),status = statuscode, content_type='application/json')
		return json.dumps({'fk_acc_fa':result[0],'bookvalue':result[1]},cls=DjangoJSONEncoder,status = 200, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
@ensure_csrf_cookie
def ShowEntry_Disposal(request):
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
			form = NA_Goods_Outwards_Form(data)
			result = ''
			if form.is_valid():
				form.clean()
				data.update(fk_maintenance=(None if int(data['fk_maintenance']) == 0 else data['fk_maintenance']))
				data.update(idapp_fk_usedemployee=(None if int(data['idapp_fk_usedemployee']) == 0 else data['idapp_fk_usedemployee']))
				data.update(fk_return=(None if int(data['fk_return']) == 0 else data['fk_return']))
				data.update(fk_lending=(None if int(data['fk_lending']) == 0 else  data['fk_lending']))
				data.update(fk_outwards=(None if int(data['fk_outwards']) == 0 else data['fk_outwards']))
				if status == 'Add':	
					data.update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					#result = NAGoodsOutwards.objects.SaveData(data,StatusForm.Input)
				elif status == 'Edit':
					data.update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					#if NAGoodsOutwards.objects.HasReference(data['idapp']):					
					#	return  HttpResponse(json.dumps({'message':'Can not edit data data\Data has child-referenced'}),status = statuscode, content_type='application/json')                       
					#result = NAGoodsOutwards.objects.SaveData(data,StatusForm.Edit)
				if result != 'success':
					statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
		if status == 'Add':
			form = NA_Goods_Disposal_Form(initial=initializationForm)
			form.fields['hasrefdata'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/NA_Entry_Goods_Disposal.html', {'form' : form})
		elif status == 'Edit' or status == 'Open':
			IDApp = request.GET.get('idapp')
			#Ndata = NAGoodsOutwards.objects.getData(IDApp)
			Ndata = Ndata[0]
			Ndata.update(idapp=IDApp)
			Ndata.update(hasRefData=commonFunct.str2bool(str(Ndata['hasrefdata'])))
			Ndata.update(initializeForm=json.dumps(Ndata,cls=DjangoJSONEncoder))
			#form = NA_Goods_Outwards_Form(data=Ndata)
			return render(request, 'app/Transactions/NA_Entry_Goods_Disposal.html', {'form' : form})    
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')

class NA_Goods_Disposal_Form(forms.Form):
	#idapp,fk_goods,goods,idapp_fk_goods,typeapp,serialnumber,brandvalue,bookvalue,fk_usedemployee,fk_usedemployee_employee,datedisposal,issold,
	#sellingprice,fk_proposedby,fk_proposedby_employee,idapp_fk_proposedby,fk_Acknowledge1,fk_Acknowledge1_employee,idapp_fk_acknowledge1,fk_Acknowledge2,
	#fk_Acknowledge2_employee,idapp_fk_acknowledge2,
	#descriptions,islost,fk_stock,fk_acc_fa,fk_usedemployee,fk_usedemployee_employee,idapp_fk_usedemployee,
	#fk_approvedby,fk_approvedby_employee,idapp_fk_approvedby,fk_maintenance,fk_return,fk_lending,fk_outwards,hasRefData,initializeForm,

	idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)	
	
	goods = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																						'placeholder': 'goods name','data-value':'goods name','tittle':'goods name is required'}))
	fk_goods = forms.CharField(widget=forms.HiddenInput(),required=False)
	idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput(),required=False)	
	
	typeapp = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False)
	serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':1,
									'placeholder': 'Serial Number','data-value':'Serial Number','tittle':'Please enter Serial Number if exists'}),required=True)   
	brandvalue = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)
	bookvalue = forms.DecimalField(max_digits=30,decimal_places=2,widget=forms.HiddenInput,required=False)
	datedisposal = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':2,
								'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter date lent','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	issold = forms.BooleanField(widget=forms.CheckboxInput(attrs={'tabindex':3,'style':'vertical-align: text-bottom;'},),required=False,)
	sellingprice = forms.DecimalField(max_digits=30,decimal_places=2,widget=forms.TextInput(attrs={
									'class':'NA-Form-Control','style':'width:112px;display:inline-block;','placeholder':'selling price','data-value':'selling price','patern':'^[0-9]+([\.,][0-9]+)?$','step':'any','tittle':'Please enter valid value','tabindex':3,'disabled':True,}),required=False)
	#proposedby
	fk_proposedby = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':4,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	fk_proposedby_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	idapp_fk_proposedby = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	#fk_acknowledge1
	fk_acknowledge1 = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':5,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	fk_acknowledge1_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	idapp_fk_acknowledge1 = forms.IntegerField(widget=forms.HiddenInput(),required=False)


	#fk_Acknowledge2
	fk_acknowledge2 = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':6,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	fk_acknowledge2_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	idapp_fk_acknowledge2 = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	#fk_approvedby
	fk_approvedby = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'width:120px;display:inline-block;margin-right:5px;margin-bottom:2px;','tabindex':7,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	fk_approvedby_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	idapp_fk_approvedby = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about lending goods',
  																		'data-value':'descriptions about disposal/deletetion of goods','title':'Remark any other text to describe transactions','tabindex':8}),required=False)
	
	islost = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False,initial=False)#di isi 1 / 0 kalau ada value di form, lainya 0
	fk_stock = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_acc_fa = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	#info
	fk_usedemployee = forms.CharField(max_length=50,widget=forms.HiddenInput(),required=False)
	fk_usedemployee_employee = forms.CharField(max_length=100, widget=forms.HiddenInput(),required=False)
	idapp_fk_usedemployee = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	
	#availability = forms.CharField(widget=forms.HiddenInput(),required=False)#value ini di peroleh secara hard code dari query jika status = edit/open
	
	fk_maintenance = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_return = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_lending = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_outwards = forms.IntegerField(widget=forms.HiddenInput(),required=False) 
	hasrefdata = forms.BooleanField(widget=forms.HiddenInput(),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

	def clean(self):
		cleaned_data = super(NA_Goods_Disposal_Form,self).clean()
		serialnumber = self.cleaned_data['serialnumber']
		fk_proposedby = self.cleaned_data['fk_proposedby']
		datereleased = self.cleaned_data['datereleased']
		fk_acknowledge1 = self.cleaned_data['fk_acknowledge1']
		fk_approvedby = self.cleaned_data['fk_approvedby']
				
	def __init__(self,*args,**kwargs):
		super(NA_Goods_Disposal_Form,self).__init__(*args, **kwargs)
		self.initial['goods'] = ''
		self.initial['brandvalue'] = ''
		self.initial['typeapp'] = ''
		self.initial['hasrefdata'] = False
		self.initial['issold'] = False
		self.initial['fk_usedemployee'] = ''
		self.initial['usedemployee'] = ''
		self.initial['sellingprice'] = 0
		self.initial['bookvalue'] = 0