from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator,EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import ResolveCriteria,commonFunct,StatusForm, Data,decorators
from NA_Models.models import NAGaReceive,goods,NASuplier
from .NA_Goods_Receive_View import NA_Goods_Receive_Form
from datetime import datetime
from django import forms

def NA_Goods_Receive_GA(request):
    return render(request,'app/Transactions/NA_F_Goods_Receive_GA.html')

def NA_Goods_Receive_GAGetData(request):
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
   
    gaData = NAGaReceive.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)
    totalRecords = len(gaData)
    paginator = Paginator(gaData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i+=1
        datarow = {
			"id" :row['idapp'], "cell" :[
				row['idapp'],i,row['goodsname'], row['brand'],row['typeapp'],row['received_by'],row['pr_by'],
				row['datereceived'],row['price'],row['supliername'],row['invoice_no'], row['machine_no'],
				row['chassis_no'],row['year_made'],row['colour'], row['model'], row['kind'], row['cylinder'], row['fuel'],
                row['descriptions'], row['createddate'], row['createdby']
				]
			}
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')

def getFormData(form):
	clData = form.cleaned_data
	data = {
		'idapp':clData['idapp'],'refno':clData['refno'],'fk_goods':clData['fk_goods'],
		'datereceived':clData['datereceived'],'fk_suplier':clData['supliercode'],
		'fk_receivedby':clData['received_by'],'fk_pr_by':clData['pr_by'],
		'invoice_no':clData['invoice_no'],'typeapp':'typeapp','brand':clData['brand'],
		'machine_no':clData['machine_no'],'chassis_no':clData['chassis_no'],
        'descriptions':clData['descriptions']
	}
	return data

#brand, invoice_no, fk_app, typeapp, machine_no, chasis_no, year_made, colour, model, kind, cylinder, fuel, description

class NA_Goods_Receive_GA_Form(forms.Form):
    fk_goods = forms.CharField(widget=forms.HiddenInput())
    itemcode = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'itemcode',
               'style':'width:120px;display:inline-block;margin-right: 5px;'}
        ),required=False)
    goodsname = forms.CharField(disabled=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'goods name'}
		),required=False)

    supliercode = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'suplier code',
               'style':'width:120px;display:inline-block;margin-right: 5px;'}
        ))
    supliername = forms.CharField(disabled=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'suplier name'}
		),required=False)

    pr_by = forms.CharField(widget=forms.HiddenInput())
    pr_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'PR By',
               'style':'width:120px;display:inline-block;margin-right: 5px;'}
        ))
    pr_by_name = forms.CharField(disabled=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'Employee Name'}
		),required=False)

    received_by = forms.CharField(widget=forms.HiddenInput())
    received_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'Received By',
               'style':'width:120px;display:inline-block;margin-right: 5px;'}
        ))
    received_by_name = forms.CharField(disabled=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'Employee Name'}
		),required=False)

    datereceived = forms.DateField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'date received',
               'style':'width:120px;display:inline-block;'}))
    brand = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'brand',
               'style':'width:120px;display:inline-block;'}
        ))
    invoice_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'invoice no',
               'style':'width:120px;display:inline-block;'}
        ))
    typeapp = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'type',
               'style':'width:150px;display:inline-block;'}
        ))
    machine_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'machine no',
               'style':'width:150px;display:inline-block;'}
        ))
    chassis_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'chassis no',
               'style':'width:205px;display:inline-block;'}))
    year_made = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'year made',
               'style':'width:120px;display:inline-block;'}))
    colour = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'colour',
               'style':'width:150px;display:inline-block;'}
        ))
    model = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'model',
               'style':'width:120px;display:inline-block;'}
        ))
    kind = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'kind',
               'style':'width:150px;display:inline-block;'}
        ))
    cylinder = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'cylinder',
               'style':'width:150px;display:inline-block;'}
        ))
    fuel = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'fuel',
               'style':'width:120px;display:inline-block;'}
        ))
    descriptions = forms.CharField(widget=forms.Textarea(
        attrs={'class':'NA-Form-Control', 'placeholder':'description',
               'style':'max-width:485px;width:485px;height:50px;max-height:60px;'}))
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def Entry_Goods_Receive_GA(request):
	if request.method == 'POST':
		form = NA_Goods_Receive_GA_Form(request.POST)
		statusForm = request.POST['statusForm']
		if form.is_valid():
			data = form.cleaned_data
			if statusForm == 'Add':
				data['createddate'] = datetime.now()
				data['createdby'] = request.user.username
			elif statusForm == 'Edit':
				data['modifieddate'] = datetime.now()
				data['modifiedby'] = request.user.username
			result = NAGaReceive.objects.SaveData(StatusForm.Input,**data)
			return commonFunct.response_default(result)
		else:
			raise forms.ValidationError(form.errors)

	elif request.method == 'GET':
		statusForm = request.GET['statusForm']
		if statusForm == 'Edit' or statusForm == 'Open':
			idapp = request.GET['idapp']
			data,result = NAGaReceive.objects.retrieveData(idapp)
			if data == Data.Success:
				if isinstance(result['datereceived'],datetime):
					result['datereceived'] = result['datereceived'].strftime('%d/%m/%Y')
				form = NA_Goods_Receive_GA_Form(initial=result)
			elif data == Data.Lost:
				return commonFunct.response_default((data,result))
		else:
			form = NA_Goods_Receive_GA_Form()
		return render(request,'app/Transactions/NA_Entry_Goods_Receive_GA.html',{'form':form})

@decorators.ajax_required
@decorators.detail_request_method('POST')
def Delete_data(request):
    idapp = request.POST['idapp']
    result = NAGaReceive.objects.DeleteData(idapp)
    return commonFunct.response_default(result)

@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
	cols = []
	cols.append({'name':'refno','value':'refno','selected':'','dataType':'varchar','text':'RefNO'})
	cols.append({'name':'goods','value':'goods','selected':'True','dataType':'varchar','text':'goods name'})
	cols.append({'name':'datereceived','value':'datereceived','selected':'','dataType':'datetime','text':'Date Received'})
	cols.append({'name':'supliername','value':'supliername','selected':'','dataType':'varchar','text':'type of brand'})
	cols.append({'name':'receivedby','value':'receivedby','selected':'','dataType':'varchar','text':'Received By'})
	cols.append({'name':'pr_by','value':'pr_by','selected':'','dataType':'varchar','text':'Purchase Request By'})
	cols.append({'name':'totalpurchase','value':'totalpurchase','selected':'','dataType':'int','text':'Total Purchased'})
	cols.append({'name':'totalreceived','value':'totalreceived','selected':'','dataType':'int','text':'Total Received'})
	cols.append({'name':'createdby','value':'createdby','selected':'','dataType':'varchar','text':'Created By'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols})