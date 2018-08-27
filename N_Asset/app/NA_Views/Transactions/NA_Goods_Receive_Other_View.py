from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator,EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import ResolveCriteria,commonFunct,StatusForm, Data,decorators
from NA_Models.models import NAGoodsReceive_other,goods,NASupplier
from .NA_Goods_Receive_View import NA_Goods_Receive_Form
from datetime import datetime
from django import forms

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
        custom_fields=[['receivedby'],['pr_by'],['suppliername']]
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
				row['IDApp'],i,row['refno'],row['goods'],row['datereceived'],row['suppliername'],
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
        'datereceived':clData['datereceived'],'fk_supplier':clData['fk_supplier'],
        'totalpurchase':clData['totalpurchase'],'totalreceived':clData['totalreceived'],
		'fk_receivedby':clData['idapp_fk_receivedby'],'fk_p_r_by':clData['idapp_fk_p_r_by'],
        'descriptions':clData['descriptions']
		 }
	return data


class NA_Goods_Receive_other_Form(NA_Goods_Receive_Form):
	typeApp = forms.CharField(widget=forms.HiddenInput())


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
			data,result = NAGoodsReceive_other.objects.retrieveData(idapp)
			if data == Data.Success:
				if isinstance(result['datereceived'],datetime):
					result['datereceived'] = result['datereceived'].strftime('%d/%m/%Y')
				form = NA_Goods_Receive_other_Form(initial=result)
			elif data == Data.Lost:
				return commonFunct.response_default((data,result))
		else:
			form = NA_Goods_Receive_other_Form()
		return render(request,'app/Transactions/NA_Entry_Goods_Receive_other.html',{'form':form})

@decorators.ajax_required
@decorators.detail_request_method('POST')
def Delete_data(request):
    idapp = request.POST['idapp']
    result = NAGoodsReceive_other.objects.DeleteData(idapp)
    return commonFunct.response_default(result)

@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
	cols = []
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