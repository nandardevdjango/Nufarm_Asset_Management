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
				row['datereceived'],row['price'],row['supliername'],row['invoice_no'],row['chasis_no'],
                row['year_made'],row['colour'], row['model'], row['kind'], row['cylinder'], row['fuel'],
                row['descriptions'], row['createddate'], row['createdby']
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

#brand, invoice_no, fk_app, typeapp, machine_no, chasis_no, year_made, colour, model, kind, cylinder, fuel, description

class NA_Goods_Receive_GA_Form(forms.Form):
    fk_goods = forms.CharField(widget=forms.HiddenInput())
    goodsname = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'goods name'}))
    supliercode = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'suplier code'}))
    supliername = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'suplier name'}))
    pr_by = forms.CharField(widget=forms.HiddenInput())
    pr_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'PR By'}))
    pr_by_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'Employee Name'}))
    received_by = forms.CharField(widget=forms.HiddenInput())
    received_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'Received By'}))
    received_by_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'Employee Name'}))
    brand = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'brand'}))
    invoice_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'invoice no'}))
    typeapp = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'type'}))
    machine_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'machine no'}))
    chasis_no = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'chasis no'}))
    year_made = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'year made'}))
    colour = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'colour'}))
    model = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'model'}))
    kind = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'kind'}))
    cylinder = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder': 'cylinder'}))
    fuel = forms.CharField(widget=forms.TextInput(
        attrs={'class':'NA-Form-Control', 'placeholder':'fuel'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class':'NA-Form-Control', 'placeholder':'description'}))


def Entry_Goods_Receive_GA(request):
	if request.method == 'POST':
		form = NA_Goods_Receive_GA_Form(request.POST)
		statusForm = request.POST['statusForm']
		if form.is_valid():
			data = getFormData(form)
			if statusForm == 'Add':
				data['createddate'] = datetime.now()
				data['createdby'] = request.user.username
			elif statusForm == 'Edit':
				data['modifieddate'] = datetime.now()
				data['modifiedby'] = request.user.username
			result = NAGaReceive.objects.SaveData(StatusForm.Input,**data)
			return commonFunct.response_default(result)

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