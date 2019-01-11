from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive, goods,NASupplier,Employee
from django.core import serializers
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import Data
from NA_DataLayer.common import commonFunct
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
from NA_DataLayer.Transactions.NA_Goods_Receive_BR import NA_BR_Goods_Receive
import math
def NA_Goods_Receive(request):
	assert isinstance(request,HttpRequest)
	#buat nama-name column, key sama 
	populate_combo = []
	populate_combo.append({'label':'RefNO','columnName':'refno','dataType':'varchar'})
	populate_combo.append({'label':'Goods Name','columnName':'goods','dataType':'varchar'})
	populate_combo.append({'label':'Date Received','columnName':'datereceived','dataType':'datetime'})
	populate_combo.append({'label':'Supplier Name','columnName':'suppliername','dataType':'varchar'})
	populate_combo.append({'label':'Received By','columnName':'receivedby','dataType':'varchar'})
	populate_combo.append({'label':'Purchase Request By','columnName':'pr_by','dataType':'varchar'})
	populate_combo.append({'label':'Total Purchased','columnName':'totalpurchase','dataType':'int'})
	populate_combo.append({'label':'Total Received','columnName':'totalreceived','dataType':'int'})
	return render(request,'app/Transactions/NA_F_Goods_Receive.html',{'populateColumn':populate_combo})
def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		#//#column idapp  no refno, goods 	datereceived suppliername FK_ReceivedBy 	receivedby FK_P_R_By pr_by totalpurchase totalreceived,CreatedDate, CreatedBy
		# label idapp', 'NO', 'RefNO', 'goods name', 'Date Received', 'Supplier Name', 'FK_ReceivedBy', 'Received By', 'FK_P_R_By ', 'Purchase Request By', 'Total Purchased', 'Total Received', 'Descriptions', 'Created Date', 'Created By'
		cols.append({'name':'refno','value':'refno','selected':'','dataType':'varchar','text':'RefNO'})
		cols.append({'name':'goods','value':'goods','selected':'True','dataType':'varchar','text':'goods name'})
		cols.append({'name':'datereceived','value':'datereceived','selected':'','dataType':'datetime','text':'Date Received'})
		cols.append({'name':'suppliername','value':'suppliername','selected':'','dataType':'varchar','text':'type of brand'})
		cols.append({'name':'receivedby','value':'receivedby','selected':'','dataType':'varchar','text':'Received By'})
		cols.append({'name':'pr_by','value':'pr_by','selected':'','dataType':'varchar','text':'Purchase Request By'})
		cols.append({'name':'totalpurchase','value':'totalpurchase','selected':'','dataType':'int','text':'Total Purchased'})
		cols.append({'name':'totalreceived','value':'totalreceived','selected':'','dataType':'int','text':'Total Received'})
		cols.append({'name':'createdby','value':'createdby','selected':'','dataType':'varchar','text':'Created By'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

def NA_Goods_Receive_Search(request):
	try:
		IcolumnName = request.GET.get('columnName');
		IvalueKey =  request.GET.get('valueKey')
		IdataType =  request.GET.get('dataType')
		Icriteria =  request.GET.get('criteria')
		Ilimit = request.GET.get('rows', '')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		#if 'supplier' in Isidx:#ganti supplier key column jadi suppliername
		#	#IndexS = Isidx.index['supplier']
		#	#del(Isidx[IndexS])
		#	#Isindx.insert(IndexS,'suppliername')
		#	str(Isidx).replace('supplier','suppliername')
		criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
		dataType = ResolveCriteria.getDataType(str(IdataType))
		if(Isord is not None and str(Isord) != '') or(Isidx is not None and str(Isidx) != ''):
			NAData = NAGoodsReceive.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsReceive.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1]
		dataRows = NAData[0]
		
		rows = []
		#column IDapp 	goods 	datereceived suppliername FK_ReceivedBy 	receivedby FK_P_R_By pr_by totalpurchase totalreceived,CreatedDate, CreatedBy
		i = 0;
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['IDApp'], "cell" :[row['IDApp'],i,row['refno'],row['goods'],row['datereceived'],row['suppliername'],row['FK_ReceivedBy'],row['receivedby'],row['FK_P_R_By'], \
				row['pr_by'],row['totalpurchase'],row['totalreceived'],row['descriptions'],datetime.date(row['CreatedDate']),row['CreatedBy']]}
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
	
def ExistSerialNO(request):
	authentication_classes = []
	statuscode = 200
	data = request.body
	data = json.loads(data)
	SN = data['SN']
	result = ''
	try:
		result = NAGoodsReceive.objects.hasEsitsSN(SN)
		result = str2bool(str(result))
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
	return HttpResponse(json.dumps({'message':result}),status = 200, content_type='application/json')

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
def getCurrentDataModel(request,form):	#fk_goods, datereceived, fk_supplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
	return {'idapp':form.cleaned_data['idapp'],'refno':form.cleaned_data['refno'],'idapp_fk_goods':form.cleaned_data['idapp_fk_goods'],'fk_goods':form.cleaned_data['fk_goods'],'datereceived':form.cleaned_data['datereceived'],'fk_supplier':form.cleaned_data['fk_supplier'],
		 'totalpurchase':form.cleaned_data['totalpurchase'],'totalreceived':form.cleaned_data['totalreceived'],'fk_receivedby':form.cleaned_data['fk_receivedby'],'idapp_fk_receivedby':form.cleaned_data['idapp_fk_receivedby'],'fk_p_r_by':form.cleaned_data['fk_p_r_by'],
		 'idapp_fk_p_r_by':form.cleaned_data['idapp_fk_p_r_by'],'descriptions':form.cleaned_data['descriptions'],'hasRefData':form.cleaned_data['hasRefData'],
		 'createddate':str(datetime.now().date()),'createdby':request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin','dataForGridDetail':{} }
@ensure_csrf_cookie
def HasExists(request):
	try:#check if exists the same data to prevent users double input,parameter data to check FK_goods,datereceived,totalpurchase
		authentication_classes = []
		data = request.body
		data = json.loads(data)
		idapp_fk_goods = data['idapp_fk_goods']
		totalpurchase = data['totalpurchase']
		datereceived = data['datereceived']
		refno = data['refno']
		statuscode = 200;
		if NAGoodsReceive.objects.hasExists(idapp_fk_goods,datereceived,totalpurchase):
			statuscode = 200
			return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
		elif NAGoodsReceive.objects.hasExistsRefNo('refno'):
			return HttpResponse(json.dumps({'message':'ref no exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
		return HttpResponse(json.dumps({'message':'OK'}),status = statuscode, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
@ensure_csrf_cookie
def ShowEntry_Receive(request):
	authentication_classes = []
	status = 'Add'
	initializationForm={}
	statuscode = 200
	data = None
	hasRefData = False
	try:
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
					dataDetail = list(json.loads(data.get('dataForGridDetail')));	
					data = getCurrentDataModel(request,form)
					dataForGridDetail = json.loads(form.cleaned_data['dataForGridDetail'], parse_float=Decimal)
					totalReceived = data['totalreceived'];	
					desc = '('				
					#dataDetail = object_list
					if len(dataDetail) > 0:
						detCount = len(dataDetail)
						#build descriptions
						for i in range(detCount):
							desc += dataDetail[i]['brandname'] + ', Type : ' + dataDetail[i]['typeapp'] + ', SN : ' + dataDetail[i]['serialnumber']
							if i <detCount -1:
								desc += ', '
							dataForGridDetail[i].update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					desc += ')'
					data['dataForGridDetail'] = dataForGridDetail
					data.update(descbysystem=desc)
					if len(dataDetail) != totalReceived:
						totalReceived = len(dataDetail)
					data.update(totalreceived=totalReceived)
					result = NAGoodsReceive.objects.SaveData(data,StatusForm.Input)
				if result != 'success':
					statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				return HttpResponse(json.dumps({'message':result}),status = 400, content_type='application/json')
			else:				
				form = NA_Goods_Receive_Form(initial=initializationForm)
				form.fields['status'].widget.attrs = {'value':status}	
				form.fields['hasRefData'].widget.attrs = {'value': False}
				return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
		elif status == 'Edit' or status == "Open":					
			if request.POST:
				hasRefData = NAGoodsReceive.objects.hasReference({'idapp':data['idapp'],'idapp_fk_goods':data['idapp_fk_goods'], 'datereceived':data['datereceived']},None)
				ChangedHeader = data['hasChangedHeader']
				ChangedDetail = data['hasChangedDetail']	
				form = NA_Goods_Receive_Form(data=data)
				if form.is_valid():
					form.clean()
					#save data
					data = getCurrentDataModel(request,form);
					data.update(idapp=data['idapp'])
					data.update(hasRefData=hasRefData)
					data.update(hasChangedHeader=ChangedHeader)
					data.update(hasChangedDetail=ChangedDetail)
					
					dataForGridDetail = json.loads(form.cleaned_data['dataForGridDetail'], parse_float=Decimal)
					dataDetail = list(dataForGridDetail)	
					desc = '('				
					#dataDetail = object_list
					if len(dataDetail) > 0:
						detCount = len(dataDetail)
						#build descriptions
						for i in range(detCount):
							desc += dataDetail[i]['brandname'] + ', Type : ' + dataDetail[i]['typeapp'] + ', SN : ' + dataDetail[i]['serialnumber']
							if i <detCount -1:
								desc += ', '
							dataForGridDetail[i].update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					desc += ')'
					data['dataForGridDetail'] = dataForGridDetail
					data.update(descbysystem=desc)
					totalReceived = data['totalreceived']
					if len(dataDetail) != totalReceived:
						totalReceived = len(dataDetail)
					data.update(totalreceived=totalReceived)
					result = NAGoodsReceive.objects.SaveData(data,StatusForm.Edit)
					if result != 'success':
						statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
					#check itemCode
					#if scorm.objects.filter(Header__id=qp.id).exists()				
					#return HttpResponse('success', 'text/plain')
			else:
				#get data from database
				IDApp = request.GET.get('idapp')

				#Ndata = goods.objects.getData(IDApp)[0]
				Ndata = NAGoodsReceive.objects.getData(IDApp)
				Ndata = Ndata[0]
				hasRefData = NAGoodsReceive.objects.hasReference({'idapp':Ndata['idapp'],'idapp_fk_goods':Ndata['idapp_fk_goods'], 'datereceived':Ndata['datereceived']},None)
				#idapp,fk_goods,refno, idapp_fk_goods,datereceived, fk_supplier,suppliername, totalpurchase, totalreceived, idapp_fk_received, fk_receivedby,employee_received,idapp_fk_p_r_by, fk_p_r_by,employee_pr, descriptions
				NAData = {'idapp':Ndata['idapp'],'refno':Ndata['refno'],'idapp_fk_goods':Ndata['idapp_fk_goods'],'fk_goods':Ndata['fk_goods'],'goods_desc':Ndata['goods_desc'],'datereceived':Ndata['datereceived'],'fk_supplier':Ndata['fk_supplier'],'suppliername':Ndata['suppliername'],
						'totalpurchase':Ndata['totalpurchase'],'totalreceived':Ndata['totalreceived'],'idapp_fk_receivedby':Ndata['idapp_fk_receivedby'],'fk_receivedby':Ndata['fk_receivedby'],'employee_received':Ndata['employee_received'],
						'idapp_fk_p_r_by':Ndata['idapp_fk_p_r_by'],'fk_p_r_by':Ndata['fk_p_r_by'],'employee_pr':Ndata['employee_pr'],'descriptions':Ndata['descriptions'],'descbysystem':Ndata['descbysystem'],'economiclife':Ndata['economiclife']}
				NAData.update(initializeForm=json.dumps(NAData,cls=DjangoJSONEncoder))
				NADetailRows =  NAGoodsReceive.objects.getDetailData(IDApp,Ndata['idapp_fk_goods'])
				#NADetailRows = NA_BR_Goods_Receive.
				rows = []			
				i = 0;
				#idapp', 'fkapp', 'NO', 'BrandName', 'Price/Unit', 'Type', 'Serial Number', 'warranty', 'End of Warranty', 'CreatedBy', 'CreatedDate', 'ModifiedBy', 'ModifiedDate'
				#var rowData = { 'idapp': '', 'fkapp': '', 'no': i + 1, 'brandname': '', 'priceperunit': '', 'typeapp': '', 'serialnumber': '', 'warranty': '', 'endofwarranty': '', 'createdby': '', 'createddate': new Date(), 'modifiedby': '', 'modifieddate': '','HasRef':false }
		  #  	DummyData.push(rowData);
				for row in NADetailRows:
					i = i+1
					datarow = {'idapp':row['IDApp'],'fkapp':row['FK_App'], 'no':i,'brandname':row['BrandName'],'priceperunit':row['PricePerUnit'], \
						'typeapp':row['TypeApp'],'serialnumber':row['SerialNumber'],'warranty':row['Warranty'],'endofwarranty':row['EndOfWarranty'], \
						'createdby':row['CreatedBy'],'createddate':row['CreatedDate'],'modifiedby':row['ModifiedBy'],'modifieddate':row['ModifiedDate'],'HasRef':str2bool(str(row['HasRef'])),'isnew':'0','isdeleted':'0','isdirty':'0'}
					rows.append(datarow)					
				dataForGridDetail = rows #{"page": int(request.GET.get('page', '1')),"total": 1 ,"records": rows.count,"rows": rows }
				#return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
				NAData.update(dataForGridDetail=json.dumps(dataForGridDetail,cls=DjangoJSONEncoder))
				NAData.update(status=status)
				NAData.update(hasRefData=hasRefData)
				form = NA_Goods_Receive_Form(data=NAData)
				#form.fields['status'].widget.attrs = {'value':status}
				if hasRefData:
					form.fields['totalreceived'].disabled = True
				#form.fields['hasRefData'].widget.attrs = {'value':hasRefData}
				return render(request, 'app/Transactions/Goods_Receive.html', {'form' : form})
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
	
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
	result = NAGoodsReceive.objects.hasReference({'idapp':data['idapp'],'idapp_fk_goods':data['idapp_fk_goods'], 'datereceived':data['datereceived']},None)
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
def deleteDetail(request):
	statuscode = 200
	#result=NAGoodsReceive.objects.delete(
	data = request.body
	data = json.loads(data)
	Iidapp = data['idapp']
	result = ''
	try:
		#get data
		NAData = {'idapp':Iidapp,'deletedby':request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin'}
		result = NAGoodsReceive.objects.deleteDetail(NAData)
		return HttpResponse(json.dumps({'message':result}),status = 200, content_type='application/json') 
	except Exception as e:
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
def getSupplier(request):
	"""get suppliername by suppliercode return suppliername criteria = ixact'
	"""
	result={}
	try:
		suppliercode = request.GET.get('suppliercode')
		result = NASupplier.customManager.getSupplier(suppliercode)
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
	return HttpResponse(json.dumps(result,cls=DjangoJSONEncoder),status = 200, content_type='application/json')
@ensure_csrf_cookie
def SearchGoodsbyForm(request):
	"""get goods data for grid searching, retusn idapp,itemcode,goods criteria = icontains"""
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	
			
	searchText = request.GET.get('goods_desc')
	Ilimit = request.GET.get('rows', '')
	NAData = None;
	if (Isord is not None and Isord != '') and (Isidx is not None and Isidx != ''):
		NAData = goods.customs.searchGoodsByForm(searchText)
		if NAData != Data.Empty:
			NAData = commonFunct.multi_sort_queryset(NAData,Isidx,Isord)
	else:
		NAData = goods.customs.searchGoodsByForm(searchText)

	#if NAData == Data.Empty:
	#	NAData = goods.objects.none()
	totalRecord = NAData.count()#if (NAData != Data.Empty) else 0
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
	return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder),content_type='application/json')
def SearchSupplierbyForm(request):
	"""get supplier data for grid return supplier code,suppliername, criteria = icontains"""
	searchText = request.GET.get('suppliername')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	NAData = None;
	if (Isord is not None and Isord != '') and (Isidx is not None and Isidx != ''):
		NAData = NASupplier.customManager.getSupplierByForm(searchText)# NASuplier.customManager.getSuplierByForm(searchText)
		if len(NAData):
			NAData.order_by('-' + str(Isidx))
			NAData = commonFunct.multi_sort_queryset(NAData,Isidx,Isord)
	else:
		NAData = NASupplier.customManager.getSupplierByForm(searchText)
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
		datarow = {"id" :row['suppliercode'], "cell" :[i,row['suppliercode'],row['suppliername']]}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder),content_type='application/json')
def SearchEmployeebyform(request):
	"""get employee data for grid return idapp,nik, employee_name criteria = icontains"""
	searchText = request.GET.get('employee_name')
	Ilimit = request.GET.get('rows', '')
	Isidx = request.GET.get('sidx', '')
	Isord = request.GET.get('sord', '')
	if (Isord is not None and Isord != '') and (Isidx is not None and Isidx != ''):
		NAData = Employee.customManager.getEmloyeebyForm(searchText)
		if len(NAData):
			NAData = commonFunct.multi_sort_queryset(NAData,Isidx,Isord)				
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
	return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder),content_type='application/json')
#def getBrandForDetailEntry(request):
#	IvalueKey =  request.GET.get('term')
#	NAGoodsReceive.objects.getBrandsForDetail(IvalueKey)
#	results = []
#	for brandrow in BrandRows:
#		JsonResult = {}
#		JsonResult['id'] = brandrow['brandname']
#		JsonResult['label'] = brandrow['brandname']
#		JsonResult['value'] = brandrow['brandname']
#		results.append(JsonResult)
#	data = json.dumps(results,cls=DjangoJSONEncoder)
#	return HttpResponse(data, content_type='application/json')
def getBrandForDetailEntry(request):
	IvalueKey =  request.GET.get('term')
	idappFKGoods = request.GET.get('fk_goods')
	BrandRows = {}
	try:
		if idappFKGoods == '' or idappFKGoods is None:
			BrandRows = NAGoodsReceive.objects.getBrandsForDetail(None,IvalueKey)
		else:
			BrandRows = NAGoodsReceive.objects.getBrandsForDetail(idappFKGoods,IvalueKey)
	except Exception as e :
		return repr(e)
	
	results = []
	for brandrow in BrandRows:
		JsonResult = {}
		JsonResult['id'] = brandrow['BrandName']
		JsonResult['label'] = brandrow['BrandName']
		JsonResult['value'] = brandrow['BrandName']
		results.append(JsonResult)
	data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(data, content_type='application/json')
def getTypeApps(request):
	IvalueKey =  request.GET.get('term')
	idappFKGoods = request.GET.get('fk_goods')
	TypeAppRows = {}
	try:
		TypeAppRows = NAGoodsReceive.objects.getTypesApp(idappFKGoods,IvalueKey)
	except Exception as e :
		return repr(e)
	
	results = []
	for typeAppRow in TypeAppRows:
		JsonResult = {}
		JsonResult['id'] = typeAppRow['TypeApp']
		JsonResult['label'] = typeAppRow['TypeApp']
		JsonResult['value'] = typeAppRow['TypeApp']
		results.append(JsonResult)
	data = json.dumps(results,cls=DjangoJSONEncoder)
	return HttpResponse(data, content_type='application/json')
class NA_Goods_Receive_Form(forms.Form):
	idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	refno = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:100px;display:inline-block;','tabindex':1,
																						 'placeholder': 'RefNO','data-value':'refno','tittle':'Ref NO is required'}))
	datereceived = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-block;margin-right:auto;padding-left:5px','tabindex':2,
                                   'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','tittle':'Please enter Date Received','patern':'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'}))
	fk_goods = forms.CharField(widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':3,
                                   'placeholder': 'goods item code','data-value':'goods item code','tittle':'Please enter item code'}),required=True)
	goods_desc = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'goods item code','data-value':'goods item code','tittle':'goods Desc is required'}))
	 
	fk_supplier = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':4,
                                   'placeholder': 'supplier code','data-value':'supplier code','tittle':'Please enter supplier code'}),required=True)
	suppliername = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'supplier name','data-value':'supplier name','tittle':'supplier name is required'}))

	totalpurchase = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':3, 'min':1,'tabindex':5,'style':'width:100px;;display:inline-block;margin-right:5px;','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	totalreceived = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={'class': 'NA-Form-Control','maxlength':3, 'min':1,'tabindex':6,'style':'width:85px;;display:inline-block;margin-right:5px;','tittle':'Total purchased is required','patern':'[1-9]\d{1,9}','step':'any'}))
	fk_p_r_by = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':7,
                                   'placeholder': 'P R By','data-value':'P R By','tittle':'Employee code(NIK) who PRs'}),required=True)
	employee_pr = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who PRs','data-value':'Employee who PRs','tittle':'Employee who PRs is required'}))
	fk_receivedby = forms.CharField(max_length=30,widget=forms.TextInput(attrs={
                                   'class': 'NA-Form-Control','style':'width:100px;display:inline-block;margin-right:5px;','tabindex':8,
                                   'placeholder': 'Who Receives','data-value':'Who Receives','tittle':'Employee code(NIK) who Receives'}),required=True)
	employee_received = forms.CharField(max_length=150,required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','readonly':True,
																						 'placeholder': 'Employee who Receives','data-value':'Employee who Receives','tittle':'Employee who Receives is required'}))
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','tabindex':9,'style':'max-width: 800px;width: 444px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods received (remark)','data-value':'descriptions about goods received (remark)'}),required=False) # models.CharField(db_column='Descriptions', max_length=150, blank=True, null=True)  # Field name made lowercase.
	idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput(),required=True)
	idapp_fk_p_r_by = forms.IntegerField(widget=forms.HiddenInput(),required=True)
	idapp_fk_receivedby = forms.IntegerField(widget=forms.HiddenInput(),required=True)
	status = forms.CharField(widget=forms.HiddenInput(),required=False)
	economiclife = forms.CharField(widget=forms.HiddenInput(),required=False)
		#initializeForm = forms.CharField(widget=forms.HiddenInput(attrs={'value':{'depreciationmethod':'SL','economiclife':5.00,'placement':'Gudang IT','inactive':False}}),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)
	descbysystem = forms.CharField(widget=forms.HiddenInput(),required=False)
	dataForGridDetail = forms.CharField(widget=forms.HiddenInput(),required=False)
	 #var data = [
  #          { id: "10", Name: "Name 1", PackageCode: "83123a", other: "x", subobject: { x: "a", y: "b", z: [1, 2, 3]} },
  #          { id: "20", Name: "Name 3", PackageCode: "83432a", other: "y", subobject: { x: "c", y: "d", z: [4, 5, 6]} },
  #          { id: "30", Name: "Name 2", PackageCode: "83566a", other: "z", subobject: { x: "e", y: "f", z: [7, 8, 9]} }
  #      ],
	#class Meta:
	#	model = NAGoodsReceive
	#	exclude = ('createdby','createddate','modifiedby','modifieddate')
	def clean(self):#fk_goods, datereceived, fk_supplier, totalpurchase, totalreceived,  fk_receivedby fk_p_r_by, idapp_fk_goods, idapp_fk_p_r_by, idapp_fk_receivedby,descriptions
		cleaned_data = super(NA_Goods_Receive_Form,self).clean()
		refno =  self.cleaned_data.get('refno')
		fk_goods = self.cleaned_data.get('fk_goods')
		datereceived = self.cleaned_data.get('datereceived')
		fk_supplier = self.cleaned_data.get('fk_supplier')
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
		dataForGridDetail = self.cleaned_data.get('dataForGridDetail')