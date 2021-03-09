from django.shortcuts import render,render_to_response
from datetime import datetime
from django.template import RequestContext
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsOutwards
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
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from NA_Report.NA_R_Goods_Outwards import NA_GO_PDF
from django.conf import settings
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
	return render(request, 'app/Transactions/NA_F_Goods_Outwards.html', {'populateColumn': populate_combo, 'CompanyName': 'Nufarm', 'title': 'Goods Outwards'})
def ShowCustomFilter(request):
	#goods,goodstype,serialnumber,daterequest,datereleased,isnew,for_employee,eks_employee,
	#fk_responsibleperson,responsible_by,fk_sender,senderby,fk_stock,refgoodsfrom,descriptions,createdby,createddate
	cols = []
	cols.append({'name':'goods','value':'goods','selected':'True','dataType':'varchar','text':'Goods name'})
	cols.append({'name':'goodstype','value':'goodstype','selected':'','dataType':'varchar','text':'Goods type'})
	cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
	cols.append({'name':'daterequest','value':'daterequest','selected':'','dataType':'datetime','text':'Date Requested'})
	cols.append({'name':'datereleased','value':'datereleased','selected':'','dataType':'datetime','text':'Date Released'})
	#cols.append({'name':'for_employee','value':'for_employee','selected':'','dataType':'varchar','text':'For Employee'})
	cols.append({'name':'responsibleby','value':'responsibleby','selected':'','dataType':'varchar','text':'Responsible by'})
	cols.append({'name':'sentby','value':'sentby','selected':'','dataType':'varchar','text':'Sent  By'})
	cols.append({'name':'isnew','value':'isnew','selected':'','dataType':'boolean','text':'Is New'})
	cols.append({'name':'refgoodsfrom','value':'refgoodsfrom','selected':'','dataType':'varchar','text':'Reference goods from'})
	cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'descriptions/Remark'})
	cols.append({'name':'createdby','value':'createdby','selected':'','dataType':'varchar','text':'Created By'})
	cols.append({'name':'createddate','value':'createddate','selected':'','dataType':'datetime','text':'Created Date'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols, 'CompanyName': 'Nufarm', 'title': 'Goods Outwards'})
def NA_Goods_Outwards_Search(request):
	try:
		IcolumnName = request.GET.get('columnName')
		IvalueKey = request.GET.get('valueKey')
		IdataType = request.GET.get('dataType')
		Icriteria = request.GET.get('criteria')
		Ilimit = request.GET.get('rows', '')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
		dataType = ResolveCriteria.getDataType(str(IdataType))
		NAData =[]
		if(Isord is not None and str(Isord) != '') or (Isidx is not None and str(Isidx) != ''):
			NAData = NAGoodsOutwards.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username,IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsOutwards.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username,IcolumnName,IvalueKey,criteria,dataType)#return tuples
		totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		#column idapp,goods,goodstype,serialnumber,daterequest,datereleased,isnew,fk_employee,for_employee,fk_usedemployee,eks_employee,
		#fk_responsibleperson,responsible_by,fk_sender,senderby,fk_stock,refgoodsfrom,descriptions,createdby,createddate
		i = 0
		for row in dataRows:
			i = i+1
			datarow = {"id" :row['idapp'], 'cell' :[row['idapp'],i,row['territory'],row['goods'],row['goodstype'],row['serialnumber'],row['daterequest'],row['datereleased'],
						row['isnew'],row['fk_employee'],row['for_employee'],row['mobile'],row['fk_usedemployee'],row['eks_employee'],row['fk_responsibleperson'],
				row['responsible_by'],row['fk_sender'],row['senderby'],row['fk_stock'],row['refgoodsfrom'],row['equipment_desc'],row['descriptions'],row['createddate'],row['createdby']]}
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows}
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
@ensure_csrf_cookie
def ShowEntry_Outwards(request):
	authentication_classes = []
	status = 'Add'
	initializationForm = {}
	statuscode = 200
	data = None
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
				data.update(isnew=strtobool(str(data['isnew'])))
				data.update(fk_frommaintenance=(None if int(data['fk_frommaintenance']) == 0 else data['fk_frommaintenance']))
				data.update(idapp_fk_usedemployee=(None if int(data['idapp_fk_usedemployee']) == 0 else data['idapp_fk_usedemployee']))
				data.update(fk_return=(None if int(data['fk_return']) == 0 else data['fk_return']))
				data.update(fk_lending=(None if int(data['fk_lending']) == 0 else data['fk_lending']))
				data.update(fk_receive=(None if int(data['fk_receive']) == 0 else data['fk_receive']))
				if status == 'Add':
					data.update(createdby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					result = NAGoodsOutwards.objects.SaveData(data,StatusForm.Input)
				elif status == 'Edit':
					data.update(modifiedby=request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
					if NAGoodsOutwards.objects.HasReference(data['idapp']):
						return HttpResponse(json.dumps({'message':'Can not edit data data\nData has child-referenced'}),status = statuscode, content_type='application/json')
					result = NAGoodsOutwards.objects.SaveData(data,StatusForm.Edit)
				if result == 'success':
					return HttpResponse(json.dumps({'message': result}), status=statuscode, content_type='application/json')
				elif int(result) > 0:
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
				else:
					statuscode = 500
					return HttpResponse(json.dumps({'message':result}),status = statuscode, content_type='application/json')
		if status == 'Add':
			form = NA_Goods_Outwards_Form(initial=initializationForm)
			form.fields['hasRefData'].widget.attrs = {'value': False}
			return render(request, 'app/Transactions/NA_Entry_Goods_Outwards.html', {'form' : form})
		elif status == 'Edit' or status == 'Open':
			IDApp = request.GET.get('idapp')
			Ndata = NAGoodsOutwards.objects.getData(IDApp)
			Ndata = Ndata[0]
			Ndata.update(idapp=IDApp)
			Ndata.update(hasRefData=commonFunct.str2bool(str(Ndata['hasRefData'])))
			Ndata.update(initializeForm=json.dumps(Ndata,cls=DjangoJSONEncoder))
			form = NA_Goods_Outwards_Form(data=Ndata)
			return render(request, 'app/Transactions/NA_Entry_Goods_Outwards.html', {'form' : form})
			#idapp, fk_goods, isnew, goods, idapp_fk_goods, fk_employee, idapp_fk_employee, fk_employee_employee
			#daterequest,datereleased, fk_stock, fk_responsibleperson, idapp_fk_responsibleperson, fk_responsibleperson_employee,
			# fk_sender, idapp_fk_sender, fk_sender_employee,  descriptions,fk_usedemployee,idapp_fk_usedemployee,fk_usedemployee_employee, typeapp, serialnumber,
			#brandvalue, fk_frommaintenance, fk_return, fk_lending, fk_receive,  lastinfo, initializeForm, hasRefData
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
		fk_employee = data['fk_employee']
		statuscode = 200
		if NAGoodsOutwards.objects.HasExists(idapp_fk_goods,serialnumber,datereq,daterel,fk_employee):
			statuscode = 200
			return HttpResponse(json.dumps({'message':'Data has exists\nAre you sure you want to add the same data ?'}),status = statuscode, content_type='application/json')
		return HttpResponse(json.dumps({'message':'OK'}),status = statuscode, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getLastDateTrans(request):
	fromtrans = request.GET.get('fromtrans')
	pkkey = request.GET.get('pkkey')
	try:
		result = NAGoodsOutwards.objects.getLastDateTrans(pkkey,fromtrans)
		return HttpResponse(json.dumps({'message':result}),status = 200, content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def getLastTransGoods(request):
	serialNO = request.GET.get('serialno')
	try:
		result = NAGoodsOutwards.objects.getLastTrans(serialNO)
		#return(idapp,itemcode,goodsname,brandname,typeapp,fk_usedemployee,nik_usedemployee,usedemployee,lastInfo,fkreceive,fkreturn,fklending,fkoutwards,fkmaintenance)
		return HttpResponse(json.dumps({'idapp':result[0],'fk_goods':result[1],'goodsname':result[2],'brandname':result[3],'type':result[4],
			'fk_usedemployee':result[5],'nik_usedemployee':result[6],'usedemployee':result[7],'lastinfo':result[8],'fk_receive':result[9],'fk_return':result[10],
			'fk_lending':result[11],'fk_outwards':[12],'fk_maintenance':result[13],}),status = 200, content_type='application/json')
	except Exception as e :
		result = repr(e)
		return HttpResponse(json.dumps({'message':result}),status = 500, content_type='application/json')
def export_to_excels(request):
	#get qryset
	NAData = []
	#tentukan column
	colNames= ['idapp', 'NO','Territory', 'Goods Name', 'Type', 'Serial Number', 'Date Request', 'Date Released', 'Is New', 'fk_employee', 'For Employee','mobile',
		'fk_usedemployee', 'Eks Employee', 'fk_responsibleperson', 'Responsible By', 'fk_sender', 'Employee Sender', 'fk_stock', 'Ref Goods From', 'Equipment', 'Descriptions', 'Created Date', 'Created By']
	try:
		IcolumnName = request.GET.get('columnName')
		IvalueKey = request.GET.get('valueKey')
		IdataType = request.GET.get('dataType')
		Icriteria = request.GET.get('criteria')
		Ilimit = request.GET.get('rows', '')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
		dataType = ResolveCriteria.getDataType(str(IdataType))
		if(Isord is not None and str(Isord) != '') or(Isidx is not None and str(Isidx) != ''):
			NAData = NAGoodsOutwards.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		else:
			NAData = NAGoodsOutwards.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin',IcolumnName,IvalueKey,criteria,dataType)#return tuples
		#totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
		#column IDapp 	goods 	datereceived suppliername FK_ReceivedBy 	receivedby FK_P_R_By pr_by totalpurchase totalreceived,CreatedDate, CreatedBy
		i = 0
		for row in dataRows:
			i = i + 1
			datarow = tuple([row['idapp'], i,row['territory'], row['goods'], row['goodstype'], row['serialnumber'], datetime.strftime(row['daterequest'], "%m/%d/%Y"), datetime.strftime(row['datereleased'], "%m/%d/%Y"),
						row['isnew'],row['fk_employee'],row['for_employee'],row['mobile'],row['fk_usedemployee'],row['eks_employee'],row['fk_responsibleperson'],
				row['responsible_by'], row['fk_sender'], row['senderby'], row['fk_stock'], row['refgoodsfrom'], row['equipment_desc'], row['descriptions'], datetime.strftime(row['createddate'],"%m/%d/%Y"), row['createdby']])
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		dataRows = list(dict(zip(colNames, row)) for row in rows)
		column_hidden = ['idapp', 'fk_employee', 'fk_usedemployee','fk_responsibleperson', 'fk_sender', 'fk_stock']
		response = commonFunct.create_excel(
			colNames, column_hidden, dataRows, 'Goods_Outwards_' + datetime.strftime(datetime.now(),"%Y_%m_%d"),'Goods_Outwards')
		return response
	except Exception as e:
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
		i = 0 #idapp,itemcode,goods
		for row in dataRows:
			i+=1
			#idapp,NO,fk_goods,goodsname,brandName,type,serialnumber,fk_usedemployee,usedemployee,lastinfo,fk_receive,fk_outwards,fk_lending,fk_return,fk_maintenance,
			datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['fk_goods'],row['goodsname'],row['brandname'],row['type'],
							row['serialnumber'],row['fk_usedemployee'],row['nik_usedemployee'],row['usedemployee'],row['lastinfo'],row['fk_receive'],row['fk_outwards'],row['fk_lending'],row['fk_return'],row['fk_maintenance'],]}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(PageSize) else (math.ceil(float(totalRecord/int(PageSize)))) # round up to next number
		results = {"page": int(PageIndex),"total": TotalPage ,"records": totalRecord,"rows": rows}
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
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
		if NAGoodsOutwards.objects.HasReference(IDApp):
			return HttpResponse(json.dumps({'message':'Can not delete data\nData has child-referenced'},cls=DjangoJSONEncoder),status = 203, content_type='application/json')
		result = NAGoodsOutwards.objects.Delete(IDApp,request.user.username if (request.user.username is not None and request.user.username != '') else 'Admin')
		return HttpResponse(json.dumps({'message':result},cls=DjangoJSONEncoder),status = statuscode, content_type='application/json')
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')
def getReportAdHoc(request):
	"""main_display_add_hoc = ['GoodsName', 'BrandName', 'SerialNumber', 'Type',
	'DateReleased', 'ToEmployee', 'Equipment', 'Descriptions', 'Conditions', 'Eks_Employee', 'Sender']"""
	try:
		data = request.body
		data = json.loads(data)
		idapp = data['idapp']
		data = NAGoodsOutwards.objects.getReportAdHoc(idapp)[0]
		goods_name = data['GoodsName']

		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = """inline; filename="Goods_Outwards_{goodsName}.pdf""".format(goodsName=goods_name)
		pdfReport = NA_GO_PDF("Goods_Outwards_{goodsName}".format(goodsName=goods_name))
		outputPDF = pdfReport.buildAddHocPDF(data)
		response.write(outputPDF)
		#return render_to_response('app/Transactions/NA_R_Goods_Outwards.html',
		#'result': outputPDF}, context_instance=RequestContext(request))
		return response
	except NAError as e:
		result = NAErrorHandler.handle(err=e)
		return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')
class NA_Goods_Outwards_Form(forms.Form):
	idapp = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_goods = forms.CharField(widget=forms.HiddenInput(),required=False)
	isnew = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False,initial=False)
	goods = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																						'placeholder': 'goods name','data-value':'goods name','tittle':'goods name is required'}))
	idapp_fk_goods = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_employee = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'inline-flex;flex:1;margin-right:5px;margin-bottom:2px;','tabindex':2,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	idapp_fk_employee = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_employee_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who uses goods','data-value':'employee who uses goods','tittle':'employee who uses goods is required'}))
	daterequest = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-flex;margin-right:auto;padding-left:5px','tabindex':5,
									'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','autocomplete':'off','tittle':'Please enter date request','patern':'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'}))
	datereleased = forms.DateField(required=True,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'width:105px;display:inline-flex;margin-right:auto;padding-left:5px','tabindex':6,
								'placeholder': 'dd/mm/yyyy','data-value':'dd/mm/yyyy','autocomplete':'off','tittle':'Please enter date lent','patern':'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$'}))
	fk_responsibleperson = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'flex:1;display:inline-flex;margin-right:5px;margin-bottom:2px;','tabindex':4,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	idapp_fk_responsibleperson = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	fk_responsibleperson_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																							'placeholder': 'employee who is responsible','data-value':'employee who is responsible','tittle':'employee who is responsible is required'}))
	fk_sender = forms.CharField(widget=forms.TextInput(attrs={#Employee Code
									'class': 'NA-Form-Control','style':'display:inline-flex;flex:1;margin-right:5px;margin-bottom:2px;','tabindex':3,
									'placeholder': 'NIK','data-value':'NIK','tittle':'Please enter NIK if exists'}),required=True)
	idapp_fk_sender = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_sender_employee = forms.CharField(max_length=120,required=False,widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'border-bottom-right-radius:0;border-top-right-radius:0;','disabled':True,
																				'placeholder': 'employee who sends','data-value':'employee who sends','tittle':'employee who sends is required'}))
	equipment_desc = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'please fill with equipment',
		'data-value':'please fill with equipment','title':'this is filled with what goods to be equiped','tabindex':8}),required=False)
	descriptions = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'cols':'100','rows':'2','style':'max-width: 520px;height: 45px;','class':'NA-Form-Control','placeholder':'descriptions about goods outwards',
		'data-value':'descriptions about goods outwards','title':'Remark any other text to describe transactions','tabindex':7}),required=False)
	fk_stock = forms.IntegerField(widget=forms.HiddenInput(),required=False)

	#info
	fk_usedemployee = forms.CharField(max_length=50,widget=forms.HiddenInput(),required=False)
	idapp_fk_usedemployee = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_usedemployee_employee = forms.CharField(max_length=100, widget=forms.HiddenInput(),required=False)
	lastinfo = forms.CharField(widget=forms.HiddenInput(),required=False)#value ini di peroleh secara hard code dari query jika status = edit/open
	typeapp = forms.CharField(max_length=32,widget=forms.HiddenInput(),required=False)
	serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'NA-Form-Control','style':'display:inline-flex;flex:1;margin-right:5px;margin-bottom:2px;','tabindex':1,
									'placeholder': 'Serial Number','data-value':'Serial Number','autocomplete':'off','tittle':'Please enter Serial Number if exists'}),required=True)
	brandvalue = forms.CharField(max_length=100,widget=forms.HiddenInput(),required=False)

	fk_frommaintenance = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_return = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_lending = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	fk_receive = forms.IntegerField(widget=forms.HiddenInput(),required=False)
	initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
	hasRefData = forms.BooleanField(widget=forms.HiddenInput(),required=False)

	def clean(self):
		cleaned_data = super(NA_Goods_Outwards_Form,self).clean()
		fk_employee = self.cleaned_data['fk_employee']
		daterequest = self.cleaned_data['daterequest']
		datereleased = self.cleaned_data['datereleased']
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
