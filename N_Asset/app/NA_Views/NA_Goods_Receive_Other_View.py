from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator,EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import ResolveCriteria,commonFunct,StatusForm
from NA_Models.models import NAGoodsReceive_other,goods,NASuplier
from .NA_Goods_Receive_View import NA_Goods_Receive_Form
from datetime import datetime

def NA_Goods_Receive_other(request):
    return render(request,'app/Transactions/NA_F_Goods_Receive_other.html')

def NA_Goods_Receive_otherGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    criteria = ResolveCriteria.getCriteriaSearch(Icriteria)
    dataType = ResolveCriteria.getDataType(IdataType)
    getColumn = commonFunct.retriveColumn(
        table=[NAGoodsReceive_other,goods],
        resolve=IcolumnName,
        initial_name=['ngr','g','emp1','emp2','sp'],
        custom_fields=[['receivedby'],['pr_by'],['supliername']]
    )
    maintenanceData = NAGoodsReceive_other.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType)
    totalRecords = len(maintenanceData)
    paginator = Paginator(maintenanceData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i+=1
        datarow = {
			"id" :row['IDApp'], "cell" :[
				row['IDApp'],i,row['refno'],row['goods'],row['datereceived'],row['supliername'],
				row['receivedby'],row['pr_by'],row['totalpurchase'],
				row['totalreceived'],row['descriptions'],datetime.date(row['CreatedDate']),row['CreatedBy']
				]
			}
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')

def getFormData(form):
	clData = form.cleaned_data
	data = {
		'idapp':clData['idapp'],'refno':clData['refno'],'fk_goods':clData['idapp_fk_goods'],
		'fk_goods':clData['fk_goods'],'datereceived':clData['datereceived'],'fk_suplier':clData['fk_suplier'],
        'totalpurchase':clData['totalpurchase'],'totalreceived':clData['totalreceived'],
		'fk_receivedby':clData['idapp_fk_receivedby'],'fk_p_r_by':clData['idapp_fk_p_r_by'],
        'descriptions':clData['descriptions']
		 }
	return data

class NA_Goods_Receive_other_Form(NA_Goods_Receive_Form):
	pass

def Entry_Goods_Receive_other(request):
	if request.method == 'POST':
		form = NA_Goods_Receive_other_Form(request.POST)
		statusForm = request.POST['statusForm']
		if form.is_valid():
			data = getFormData(form)
			if statusForm == 'Add':
				data['createddate'] = datetime.now()
				data['createdby'] = request.user.username
			elif statusForm == 'Edit':
				data['modifieddate'] = datetime.now()
				data['modifiedby'] = request.user.username
			result = NAGoodsReceive_other.objects.SaveData(StatusForm.Input,**data)
			return commonFunct.response_default(result)

	elif request.method == 'GET':
		statusForm = request.GET['statusForm']
		if statusForm == 'Edit' or statusForm == 'Open':
			idapp = request.GET['idapp']
			data = NAGoodsReceive_other.objects.retrieveData(idapp)
			form = NA_Goods_Receive_other_Form(initial=data)
		else:
			form = NA_Goods_Receive_other_Form()
		return render(request,'app/Transactions/NA_Entry_Goods_Receive_other.html',{'form':form})