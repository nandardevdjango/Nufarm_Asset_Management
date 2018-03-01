﻿from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive, goods,NASuplier,Employee
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
from django.http import HttpResponseRedirect
from distutils.util import strtobool
def NA_Goods_Receive(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'RefNO','columnName':'RefNO','dataType':'varchar'})
	populate_combo.append({'label':'Goods Descriptions','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Date Received','columnName':'datereceived','dataType':'datetime'})
	populate_combo.append({'label':'Suplier Name','columnName':'suplier','dataType':'varchar'})
	populate_combo.append({'label':'Received By','columnName':'receivedby','dataType':'varchar'})
	populate_combo.append({'label':'PR By','columnName':'pr_by','dataType':'varchar'})
	populate_combo.append({'label':'Total Purchased','columnName':'totalpurchase','dataType':'int'})
	populate_combo.append({'label':'Total Received','columnName':'totalreceived','dataType':'int'})
	return render(request,'app/Transactions/NA_F_Goods_Receive.html',{'populateColumn':populate_combo})
def NA_Goods_Receive_Search(request):
	IcolumnName = request.GET.get('columnName');
	IvalueKey =  request.GET.get('valueKey')
	IdataType =  request.GET.get('dataType')
	Icriteria =  request.GET.get('criteria')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	if 'suplier' in Isidx:#ganti suplier key column jadi supliername
		#IndexS = Isidx.index['suplier']
		#del(Isidx[IndexS])
		#Isindx.insert(IndexS,'supliername')
		str(Isidx).replace('suplier','supliername') 
	criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
	dataType = ResolveCriteria.getDataType(str(IdataType))
	if(Isord is not None and str(Isord) != '') or(Isidx is not None and str(Isidx) != ''):
		NAData = NAGoodsReceive.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
	else:
		NAData = NAGoodsReceive.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
	totalRecord = NAData[1][0]
	dataRows = NAData[0]
		
	rows = []
	#column IDapp 	goods 	datereceived supliername FK_ReceivedBy 	receivedby FK_P_R_By pr_by totalpurchase totalreceived,CreatedDate, CreatedBy
	i = 0;
	for row in dataRows:
		datarow = {"id" :row['IDApp'], "cell" :[row['IDApp'],i+1,row['refno'],row['goods'],row['datereceived'],row['supliername'],row['FK_ReceivedBy'],row['receivedby'],row['FK_P_R_By'], \
			row['pr_by'],row['totalpurchase'],row['totalreceived'],row['descriptions'],datetime.date(row['CreatedDate']),row['CreatedBy']]}
		#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
		#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
		rows.append(datarow)
	results = {"page": int(request.GET.get('page', '1')),"total": totalRecord/int( request.GET.get('page', '1')) ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def getRefNO(request):
	if(request.is_ajax()):
		IvalueKey =  request.GET.get('term')
		dataRows = NAGoodsReceive.objects.getRefNO(IvalueKey)
		results = []
		for datarow in dataRows:
			JsonResult = {}
			JsonResult['id'] = datarow['refno']
			JsonResult['label'] = datarow['refno']
			JsonResult['value'] = datarow['refno']
			results.append(JsonResult)
		data = json.dumps(results,cls=DjangoJSONEncoder)
		return HttpResponse(data, content_type='application/json')
	else:
		return HttpResponse(content='',content_type='application/json')	
def getCurrentDataModel(request,form):	#fk_goods, datereceived, fk_suplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
	return {'refno':form.cleaned_data['refno'],'idapp_fk_goods':form.cleaned_data['idapp_fk_goods'],'fk_goods':form.cleaned_data['fk_goods'],'datereceived':form.cleaned_data['datereceived'],'fk_suplier':form.cleaned_data['fk_suplier'],
		 'totalpurchase':form.cleaned_data['totalpurchase'],'totalreceived':form.cleaned_data['totalreceived'],'fk_receivedby':form.cleaned_data['fk_receivedby'],'idapp_fk_p_r_by':form.cleaned_data['idapp_fk_p_r_by'],'hasRefData':form.cleaned_data['hasRefData'],
		 'idapp_fk_receivedby':form.cleaned_data['idapp_fk_receivedby'],'descriptions':form.cleaned_data['descriptions'],'createddate':str(datetime.now().date()),'createdby':request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin' }
def HasExists(request):
	FK_goods = request.POST.get('fk_goods')
	totalpurchase = request.POST.get('totalpurchase')
	datereceived = request.POST.get('datereceived')
	if NAGoodsReceive.objects.hasExists(FK_goods,datereceived,totalpurchase):
		result = 'success'
		statuscode = 200
	return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
@ensure_csrf_cookie
def ShowEntry_Receive(request):
	authentication_classes = []
	status = 'Add'
	initializationForm={}
	statuscode = 200
	data = None
	if request.POST:
		data = request.body
		data = json.loads(data)
		status = data['status']
	else:
		status = 'Add' if request.GET.get('status') == None else request.GET.get('status')	
		#set initilization
	if status == 'Add':		
		if request.POST:
			form = NA_Goods_Receive_Form(data)
			statuscode = 200
			if form.is_valid():
				#save data
				#ALTER TABLE n_a_goods MODIFY IDApp INT AUTO_INCREMENT PRIMARY KEY
				form.clean()					
				data = getCurrentDataModel(request,form)	
				#check if exists the same data to prevent users double input,parameter data to check FK_goods,datereceived,totalpurchase				
				result = NAGoodsReceive.objects.SaveData(data,StatusForm.Input)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
			else: 
				return HttpResponse(json.dumps({'message':'invalid form data'}),status = 400, content_type='application/json')
		else:				
			form = NA_Goods_Receive_Form(initial=initializationForm)
			form.fields['status'].widget.attrs = {'value':status}	
			form.fields['hasRefData'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
	elif status == 'Edit' or status == "Open":	
		hasRefData = NAGoodsReceive.objects.hasReference({idapp:data['idapp'],FK_goods:['idapp_fk_goods'], datereceived:data['datereceived']},False)	
		if request.POST:
			form = NA_Goods_Receive_Form(data)
			if form.is_valid():
				form.clean()
				#save data
				data = getCurrentDataModel(request,form);
				data.update(idapp=data['idapp'])
				data.update(hasRefData=hasRefData)
				result = NAGoodsReceive.objects.SaveData(data,StatusForm.Edit)
				if result != 'success':
					statuscode = 500
				return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				#check itemCode
				#if scorm.objects.filter(Header__id=qp.id).exists()				
				#return HttpResponse('success', 'text/plain')
		else:
			#get data from database
			IDApp = data['idapp']
			#Ndata = goods.objects.getData(IDApp)[0]
			Ndata = NAGoodsReceive.objects.getData(IDApp)[0]	
			#idapp,fk_goods,refno, idapp_fk_goods,datereceived, fk_suplier,supliername, totalpurchase, totalreceived, idapp_fk_received, fk_receivedby,employee_received,idapp_fk_p_r_by, fk_p_r_by,employee_pr, descriptions	
			NAData = {'idapp':idapp,'refno':Ndata.refno,'idapp_fk_goods':Ndata.idapp_fk_goods,'fk_goods':Ndata.fk_goods,'goods_desc':Ndata.goods,'datereceived':Ndata.datereceived,'fk_suplier':Ndata.fk_suplier,'supliername':Ndata.supliername,
					'totalpurchase':Ndata.totalpurchase,'totalreceived':Ndata.totalreceived,'idapp_fk_received':Ndata.idapp_fk_received,'fk_receivedby':Ndata.fk_receivedby,'employee_received':Ndata.employee_received,
					'idapp_fk_p_r_by':Ndata.idapp_fk_p_r_by,'fk_p_r_by':Ndata.idapp_fk_p_r_by,'employee_pr':Ndata.employee_pr,'descriptions':Ndata.descriptions,'descbysystem':Ndata.descbysystem}
			NAData.update(initializeForm=json.dumps(NAData,cls=DjangoJSONEncoder))
			NADetailRows = NAGoodsReceive.objects.getDetailData(IDApp,Ndata.idapp_fk_goods)
			rows = []			
			i = 0;
			#idapp', 'fkapp', 'NO', 'BrandName', 'Price/Unit', 'Type', 'Serial Number', 'warranty', 'End of Warranty', 'CreatedBy', 'CreatedDate', 'ModifiedBy', 'ModifiedDate'
			for row in NADetailRows:
				datarow = {"id" :i+1, "cell" :[row[i]['idapp'],row[i]['fkapp'], i+1,row[i]['brandname'],row[i]['priceperunit'],row[i]['typeapp'],row[i]['serialnumber'],row[i]['warranty'],row[i]['endofwarranty'], \
				row[i]['createdby'],row[i]['createddate'],row[i]['modifiedby'],row[i]['modifieddate'],row[i]['HasRef']]}
				rows.append(datarow)
			dataForGridDetail = {"page": int(request.GET.get('page', '1')),"total": 1 ,"records": rows.count,"rows": rows }
			#return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
			NAData.update(dataForGridDetail=json.dumps(dataForGridDetail,cls=DjangoJSONEncoder))
			form = NA_Goods_Receive_Form(data=NAData)
			form.fields['status'].widget.attrs = {'value':status}
			if hasRefData:
				form.fields['totalreceived'].disabled = True
			form.fields['hasRefData'].widget.attrs = {'value': str2bool(hasRefData)} 
			return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
def HasRefDetail(request):	
	data = request.POST.get('data')
	data = json.loads(data)	
	result = False
	try:
		result = NAGoodsReceive.objects.hasRefDetail({idapp:data['idapp_fk_goods'],
												datereceived:data['datereceived'], 
												typeapp:data['typeapp'],
												serialnumber:data['serialnumber']},False)				
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
	result = NAGoodsReceive.objects.hasReference({idapp:data['idapp'],FK_goods:['idapp_fk_goods'], datereceived:data['datereceived']},False)
def Delete(request):
	result = ''
	try:
		#result=NAGoodsReceive.objects.delete(
		IDApp = request.POST.get('idapp')
		Ndata = NAGoodsReceive.objects.getData(IDApp)[0]
		NAData = {'idapp':IDApp,'idapp_fk_goods':Ndata.idapp_fk_goods,'datereceived':Ndata.datereceived}
		result = NAGoodsReceive.objects.delete(Data)
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def deleteDetail(request):
	Iidapp = Request.POST.get('idapp')
	result = ''
	try:
		result = NAGoodsReceive.objects.deleteDetail(Iidapp)
		return HttpResponse(json.dumps({'message':result}),status = 200, content_type='application/json') 
	except :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getGoods(request):
	"""get goods by itemcode return 'goodsname' + 'brandname' + 'itemcode' as goods criteria = iexact
	"""

	result={};
	try:
		itemcode = request.GET.get('itemcode')
		result = goods.customs.getGoods(itemcode)
		if len(list(result)):
			result = result[0]
			result = {'goods':result.goods}
		else:
			result = {'goods':''}
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getSuplier(request):
	"""get supliername by supliercode return supliername criteria = ixact'
	"""
	result={}
	try:
		supliercode = request.GET.get('supliercode')
		result = NASuplier.customManager.getSuplier(supliercode)
		if len(list(result)):
			result = result[0]
		else :
			result={}
		return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json') 
	except Exception as e:					
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getEmployee(request):
	"""get employee name by nik return employee name criteria = iexact"""
	nik =  request.GET.get('nik')
	result={};
	result = Employee.customManager.getEmployee(nik)
	if len(list(result)):
		result = result[0]
	else :
		result={}
	#if result.count > 0:
	#	result = result[0]	
		#for brandrow in BrandRows:
		#	JsonResult = {}
		#	JsonResult['id'] = brandrow['brandname']
		#	JsonResult['label'] = brandrow['brandname']
		#	JsonResult['value'] = brandrow['brandname']
		#	results.append(JsonResult)
		#data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 500, content_type='application/json')
@ensure_csrf_cookie
def SearchGoodsbyForm(request):
	"""get goods data for grid searching, retusn idapp,itemcode,goods criteria = icontains"""
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	
			
	searchText = request.GET.get('goods_desc')
	Ilimit = request.GET.get('rows', '')
	NAData = None;
	if(Isord is not None and str(Isord) != ''):
		NAData = goods.customs.searchGoodsByForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = goods.customs.searchGoodsByForm(searchText)
	totalRecord = NAData.count()
	paginator = Paginator(NAData, int(Ilimit)) 
	try:
		page = request.GET.get('page', '1')
	except ValueError:
		page = 1
	try:
		dataRows = paginator.page(page)
	except (EmptyPage, InvalidPage):
		dataRows = paginator.page(paginator.num_pages)
		
	rows = []
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],i,row['itemcode'],row['goods']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def SearchSuplierbyForm(request):
	"""get suplier data for grid return suplier code,supliername, criteria = icontains"""
	searchText = request.GET.get('supliername')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	NAData = None;
	if(Isord is not None and str(Isord) != ''):
		NAData = NASuplier.customManager.getSuplierByForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = NASuplier.customManager.getSuplierByForm(searchText)
	totalRecord = NAData.count()
	paginator = Paginator(NAData, int(Ilimit)) 
	try:
		page = request.GET.get('page', '1')
	except ValueError:
		page = 1
	try:
		dataRows = paginator.page(page)
	except (EmptyPage, InvalidPage):
		dataRows = paginator.page(paginator.num_pages)
		
	rows = []
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :row['supliercode'], "cell" :[i,row['supliercode'],row['supliername']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def SearchEmployeebyform(request):
	"""get employee data for grid return idapp,nik, employee_name criteria = icontains"""
	searchText = request.GET.get('employee_name')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	if(Isord is not None and str(Isord) != ''):
		NAData = Employee.customManager.getEmloyeebyForm(searchText).order_by('-' + str(Isidx))
	else:
		NAData = Employee.customManager.getEmloyeebyForm(searchText)
	totalRecord = NAData.count()
	paginator = Paginator(NAData, int(Ilimit)) 
	try:
		page = request.GET.get('page', '1')
	except ValueError:
		page = 1
	try:
		dataRows = paginator.page(page)
	except (EmptyPage, InvalidPage):
		dataRows = paginator.page(paginator.num_pages)
		
	rows = []
	i = 0;#idapp,itemcode,goods
	for row in dataRows.object_list:
		i+=1
		datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['nik'],row['employee_name']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
def getBrandForDetailEntry(request):
	IvalueKey =  request.GET.get('term')
	NAGoodsReceive.objects.getBrandsForDetail(IvalueKey)
	results = []
	for brandrow in BrandRows:
		JsonResult = {}
		JsonResult['id'] = brandrow['brandname']
		JsonResult['label'] = brandrow['brandname']
		JsonResult['value'] = brandrow['brandname']
		results.append(JsonResult)
	data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(data, content_type='application/json')
def getBrandForDetailEntry(request):
	IvalueKey =  request.GET.get('term')
	NAGoodsReceive.objects.getBrandsForDetail(IvalueKey)
	results = []
	for brandrow in BrandRows:
		JsonResult = {}
		JsonResult['id'] = brandrow['brandname']
		JsonResult['label'] = brandrow['brandname']
		JsonResult['value'] = brandrow['brandname']
		results.append(JsonResult)
	data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(data, content_type='application/json')
class NA_Goods_Receive_Form(forms.Form):
	idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	RefNO = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;',
																						 'placeholder': 'RefNO','data-value':'RefNO','tittle':'Ref NO is required'}))
	fk_goods = forms.CharField(widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':1,
                                   'placeholder': 'goods item code','data-value':'goods item code','tittle':'Please enter item code'}),required=True)
	goods_desc = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'goods item code','data-value':'goods item code','tittle':'goods Desc is required'}))
	 
	fk_suplier = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':2,
                                   'placeholder': 'suplier code','data-value':'suplier code','tittle':'Please enter suplier code'}),required=True)
	supliername = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'suplier name','data-value':'suplier name','tittle':'suplier name is required'}))
	datereceived = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:115px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':3,
                                   'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter Date Received','patern':'((((0[13578]|1[02])\/(0[1-9]|1[0-9]|2[0-9]|3[01]))|((0[469]|11)\/(0[1-9]|1[0-9]|2[0-9]|3[0]))|((02)(\/(0[1-9]|1[0-9]|2[0-8]))))\/(19([6-9][0-9])|20([0-9][0-9])))|((02)\/(29)\/(19(6[048]|7[26]|8[048]|9[26])|20(0[048]|1[26]|2[048])))'}))
	totalpurchase = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':4, 'min':1, 'max':9000,'tabindex':4,'style':'width:100px;;display:inline-block;margin-right:5px;','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	totalreceived = forms.IntegerField(max_value=1000,required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':4, 'min':1, 'max':9000,'tabindex':5,'style':'width:80px;;display:inline-block;margin-right:5px;','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	fk_p_r_by = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':6,
                                   'placeholder': 'P R By','data-value':'P R By','tittle':'Employee code(NIK) who PRs'}),required=True)
	employee_pr = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who PRs','data-value':'Employee who PRs','tittle':'Employee who PRs is required'}))
	fk_receivedby = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':7,
                                   'placeholder': 'Who Receives','data-value':'Who Receives','tittle':'Employee code(NIK) who Receives'}),required=True)
	employee_received = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who Receives','data-value':'Employee who Receives','tittle':'Employee who Receives is required'}))
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','tabindex':8,'style':'max-width: 520px;width: 444px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods received (remark)','data-value':'descriptions about goods received (remark)'}),required=False) # models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput())
	idapp_fk_p_r_by = forms.IntegerField(widget=forms.HiddenInput())
	idapp_fk_receivedby = forms.IntegerField(widget=forms.HiddenInput())
	status = forms.CharField(widget=forms.HiddenInput())
		#initializeForm = forms.CharField(widget=forms.HiddenInput(attrs={'value':{'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False}}),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)
	descbysystem = forms.CharField(max_length=250,widget=forms.HiddenInput(),required=False)
	dataForGridDetail = forms.CharField(max_length=2000,widget=forms.HiddenInput(),required=False)
	 #var data = [
  #          { id: "10", Name: "Name 1", PackageCode: "83123a", other: "x", subobject: { x: "a", y: "b", z: [1, 2, 3]} },
  #          { id: "20", Name: "Name 3", PackageCode: "83432a", other: "y", subobject: { x: "c", y: "d", z: [4, 5, 6]} },
  #          { id: "30", Name: "Name 2", PackageCode: "83566a", other: "z", subobject: { x: "e", y: "f", z: [7, 8, 9]} }
  #      ],
	#class Meta:
	#	model = NAGoodsReceive
	#	exclude = ('createdby','createddate','modifiedby','modifieddate')
	def clean(self):#fk_goods, datereceived, fk_suplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
		cleaned_data = super(NA_Goods_Receive_Form,self).clean()
		RefNO =  self.cleaned_data.get('refno')
		fk_goods = self.cleaned_data.get('fk_goods')
		datereceived = self.cleaned_data.get('datereceived')
		fk_suplier = self.cleaned_data.get('fk_suplier')
		totalpurchase = self.cleaned_data.get('totalpurchase')
		totalreceived = self.cleaned_data.get('totalreceived')
		fk_receivedby = self.cleaned_data.get('fk_receivedby')
		fk_p_r_by = self.cleaned_data.get('fk_p_r_by')
		idapp_fk_goods = self.cleaned_data.get('idapp_fk_goods')
		idapp_fk_p_r_by = self.cleaned_data.get('idapp_fk_p_r_by')
		idapp_fk_receivedby = self.cleaned_data.get('idapp_fk_receivedby')
		descriptions = self.cleaned_data.get('descriptions')
		hasRefData = self.cleaned_data.get('hasRefData')
		descbysystem = self.cleaned_data.get('descbysystem')