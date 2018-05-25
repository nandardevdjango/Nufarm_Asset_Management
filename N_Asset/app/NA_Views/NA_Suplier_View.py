from django.shortcuts import render
from NA_Models.models import NASuplier, LogEvent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import datetime
from NA_DataLayer.common import (CriteriaSearch, StatusForm, ResolveCriteria, Data, 
								 Message, commonFunct,decorators)
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import forms

#@login_required
def NA_Suplier(request):
    return render(request, 'app/MasterData/NA_F_Suplier.html')

@decorators.ajax_required
@decorators.detail_request_method('GET')
def NA_SuplierGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    if(',' in Isidx):
        Isidx = Isidx.split(',')

    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    if(Isord is not None and str(Isord) != ''):
        suplData = NASuplier.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
    else:
        suplData = NASuplier.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)

    totalRecord = suplData.count()
    paginator = Paginator(suplData, int(Ilimit))
    try:
        page = request.GET.get('page', '1')
    except ValueError:
        page = 1
    try:
        dataRows = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dataRows = paginator.page(paginator.num_pages)

    rows = []
    i = 0
    for row in dataRows.object_list:
        i += 1
        datarow = {"id" :row['supliercode'], "cell" :[i,row['supliercode'],row['supliername'],row['address'],row['telp'],row['hp'],row['contactperson'], \
		    row['inactive'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')


class NA_Suplier_form(forms.Form):
    supliercode = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Enter Suplier Code','style':'width:200px'}))
    supliername = forms.CharField(max_length=40, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Enter Suplier Name','style':'width:220px'}))
    address = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control', 'placeholder':'Address of Suplier','cols':'100','rows':'2', 
        'style':'height: 50px;max-height:70px;width:430px;max-width:430px'}))
    telp = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Telp','style':'width:200px'}))
    hp = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Phone Number','style':'width:220px'}))
    contactperson = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class':'NA-Form-Control', 'placeholder':'Contact Person','style':'width:200px'}))
    inactive = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    window_status = forms.CharField(widget=forms.HiddenInput(), required=False)
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def getCurrentUser(request):
    return str(request.user.username)

def getData(request, form):
    clData = form.cleaned_data
    data = {'supliercode': clData['supliercode'],'supliername': clData['supliername'],'address': clData['address'],
        'telp':clData['telp'],'hp':clData['hp'],'contactperson':clData['contactperson'],'inactive':clData['inactive']
        }
    return data

def EntrySuplier(request):
    if request.method == 'POST':
        form = NA_Suplier_form(request.POST)
        if form.is_valid():
            mode = request.POST['mode']
            data = getData(request, form)
            result = None
            if mode == 'Add':
                data['createddate'] = datetime.datetime.now()
                data['createdby'] = getCurrentUser(request)
                result = NASuplier.objects.SaveData(StatusForm.Input,**data)
            elif mode == 'Edit':
                data['modifieddate'] = datetime.datetime.now()
                data['modifiedby'] = getCurrentUser(request)
                result = NASuplier.objects.SaveData(StatusForm.Edit,**data)
            elif mode == 'Open':
                if request.POST['supliername']:
                    return HttpResponse(json.dumps({'message':'Cannot Edit Data with inspect element .. .'}),status=403,content_type='application/json')
            return commonFunct.response_default(result)
    elif request.method == 'GET':
        getSupCode = request.GET['supliercode']
        mode = request.GET['mode']
        if mode == 'Edit' or mode == 'Open':
            result = NASuplier.objects.retriveData(getSupCode) #return tuple
            if result[0] == Data.Success:
                form = NA_Suplier_form(initial=result[1][0])
                form.fields['supliercode'].widget.attrs['disabled'] = 'disabled'
                return render(request, 'app/MasterData/NA_Entry_Suplier.html', {'form':form})
            elif result[0] == Data.Lost:
                return HttpResponse(json.dumps({'message':Message.get_lost_info(pk=getSupCode,table='suplier')}),status=404,content_type='application/json')
        else:
            form = NA_Suplier_form()
            return render(request, 'app/MasterData/NA_Entry_Suplier.html', {'form':form})

@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
	cols = []
	cols.append({'name':'supliercode','value':'supliercode','selected':'','dataType':'varchar','text':'Suplier Code'})
	cols.append({'name':'supliername','value':'supliername','selected':'True','dataType':'varchar','text':'Suplier Name'})
	cols.append({'name':'address','value':'address','selected':'','dataType':'varchar','text':'Address'})
	cols.append({'name':'telp','value':'telp','selected':'','dataType':'varchar','text':'Telp'})
	cols.append({'name':'hp','value':'hp','selected':'','dataType':'varchar','text':'Hp'})
	cols.append({'name':'contactperson','value':'contactperson','selected':'','dataType':'varchar','text':'Contact Person'})
	cols.append({'name':'inactive','value':'inactive','selected':'','dataType':'boolean','text':'InActive'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

@decorators.ajax_required
@decorators.detail_request_method('POST')
def NA_Suplier_delete(request):
    if request.user.is_authenticated():
        get_supcode = request.POST.get('supliercode')
        deleteObj = NASuplier.objects.delete_suplier(supliercode=get_supcode,NA_User=request.user.username)
        return commonFunct.response_default(deleteObj)

def SearchSuplierbyForm(request):
	"""get suplier data for grid return suplier code,supliername, criteria = icontains"""
	searchText = request.GET.get('supliername')
	Ilimit = request.GET.get('rows')
	Isidx = request.GET.get('sidx')
	Isord = request.GET.get('sord')
	NAData = NASuplier.objects.getSuplierByForm(searchText)
	if NAData == Data.Empty:
		results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
		return HttpResponse(
			json.dumps(results, indent=4,cls=DjangoJSONEncoder),
			content_type='application/json'
		)
	print(Isidx)
	print(Isidx == None)
	if (Isord is not None and Isord != '') and (Isidx is not None and Isidx != ''):
		#if ',' in Isidx:
		#	multi_sort = []
		#	Isidx = Isidx.split(',')
		#	for i in Isidx:
		#		multi_sort.append({'column':})
		#		if len(i.split(' ')) > 1:

		sort = str(Isidx)
		if Isord == 'desc':
			sort = '-' + sort
		NAData = NAData.order_by(sort)
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
		datarow = {
			"id" :row['supliercode'], "cell" :[
				i,row['supliercode'],row['supliername'],row['address']
				]
			}
		rows.append(datarow)
	results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
	return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')