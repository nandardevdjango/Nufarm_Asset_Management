from NA_Models.models import NAGoodsLost, goods, Employee, NAGoodsHistory,\
NAGoodsOutwards, NAGoodsLending, NAMaintenance,NAGoodsReceive
from NA_Models.NASerialize import NAGoodsLostSerializer,NAGoodsOutWordsSerializer,NAGoodLendingSerializer
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, commonFunct, StatusForm
from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from datetime import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import F, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
def NA_Goods_Lost(request):
    return render(request,'app/MasterData/NA_F_GoodsLost.html')

def NA_GoodsLost_GetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    getColumn = commonFunct.retriveColumn(
		table=[NAGoodsLost,goods],resolve=IcolumnName,
		initial_name=['gls','g','empl1','empl2','empl3'],
		custom_fields=[['used_by'],['lost_by'],['resp_person']])
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    accData = NAGoodsLost.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType,Isidx,Isord)
    paginator = Paginator(accData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    totalRecord = len(accData)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i +=1
        datarow = {"id" :row['idapp'], "cell" :[row['idapp'],i,row['goods'],row['itemcode'],row['serialnumber'],row['fromgoods'],row['used_by'],\
            row['lost_by'],row['resp_person'],row['descriptions'],row['createddate'],row['createdby']]}
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def ShowCustomFilter(request):
	if request.is_ajax():
		cols = []
		cols.append({'name':'goodsname','value':'goodsname','selected':'True','dataType':'varchar','text':'Goods Name'})
		cols.append({'name':'brandname','value':'brandname','selected':'','dataType':'varchar','text':'Brand Name'})
		cols.append({'name':'itemcode','value':'itemcode','selected':'','dataType':'varchar','text':'Item code'})
		cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
		cols.append({'name':'used_by','value':'used_by','selected':'','dataType':'varchar','text':'Used by'})
		cols.append({'name':'lost_by','value':'lost_by','selected':'','dataType':'varchar','text':'Lost by'})
		cols.append({'name':'resp_person','value':'resp_person','selected':'','dataType':'varchar','text':'Responsible Person'})
		cols.append({'name':'descriptions','value':'descriptions','selected':'','dataType':'varchar','text':'Descriptions'})
		return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

class NA_GoodsLost_Form(forms.Form):
    fk_goods = forms.IntegerField(required=True,widget=forms.HiddenInput())
    fk_fromgoods = forms.CharField(required=False,widget=forms.HiddenInput())
    goods = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'goods'}))
    itemcode = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control cust-horizontal', 'disabled': 'disabled','placeholder': 'Item code', 'style': 'width:345px'}))
    typeApp = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','disabled':'disabled','placeholder':'Type of goods','style':'width:130px'}))
    serialNumber = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control cust-horizontal', 'placeholder': 'Serial Number', 'style': 'width:98.9%'}))

    nik_used = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control cust-horizontal', 'placeholder': 'Nik', 'style': 'width:130px', 'disabled': 'disabled'}))
    empl_used = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control cust-horizontal', 'placeholder': 'Employee who keeps', 'style': 'width:345px', 'disabled':'disabled'}))
    fk_lostby = forms.IntegerField(required=True,widget=forms.HiddenInput())
    nik_lostby = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Nik','style':'width:130px'}))
    empl_lostby = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Employee who lost goods','disabled':'disabled'}))
    nik_resp = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Nik','style':'width:130px'}))
    empl_resp = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Responsible person','style':'width:345px','disabled':'disabled'}))
    datelost = forms.CharField(required=True,widget=forms.TextInput(attrs={
        'class':'NA-Form-Control cust-horizontal','placeholder':'Date Lost','style':'width:130px'}))
    status_goods = forms.ChoiceField(required=False,widget=forms.Select(attrs={
                    'class':'NA-Form-Control', 'style':'width:130px;display:inline-block;'}),choices=(('L','Lost'),('F','Find')))
    reason = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control','placeholder':'reason .. .', 'style':'width:585px;height:50px;max-width:590px;max-height:125px;'}))
    descriptions = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class':'NA-Form-Control','placeholder':'descriptions .. .', 'style':'width:585px;height:50px;max-width:590px;max-height:125px;'}))
    fk_responsibleperson = forms.IntegerField(required=False, widget=forms.HiddenInput())
    fk_usedby = forms.IntegerField(required=False, widget=forms.HiddenInput())
    fk_goods_outwards = forms.IntegerField(required=False,widget=forms.HiddenInput())
    fk_goods_lending = forms.IntegerField(required=False,widget=forms.HiddenInput())
    fk_maintenance = forms.IntegerField(required=False,widget=forms.HiddenInput())
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)
def getFormData(request, forms, **kwargs):
    clData = forms.cleaned_data
    data = {
        'fk_goods': clData['fk_goods'],'goods': clData['goods'],'typeApp':clData['typeApp'],
        'serialnumber':clData['serialNumber'],'fk_fromgoods':clData['fk_fromgoods'],'fk_goods_outwards': clData['fk_goods_outwards'],
        'fk_goods_lending': clData['fk_goods_lending'], 'fk_maintenance': clData['fk_maintenance'], 'fk_lostby': clData['fk_lostby'],
        'fk_responsibleperson': clData['fk_responsibleperson'], 'fk_usedby': clData['fk_usedby'], 'nik_used': clData['nik_used'], 'nik_resp': clData['nik_resp'],
        'nik_lostby':clData['nik_lostby'],
        'datelost':clData['datelost'],'reason':clData['reason'],'descriptions': clData['descriptions']
        }
    if 'status_form' in kwargs:
        if kwargs['status_form'] == 'Edit' or kwargs['status_form'] == 'Open':
            data['status_goods'] = request.POST['status_goods']
    return data
@ensure_csrf_cookie
def EntryGoods_Lost(request):
    if request.method == 'POST':
        form = NA_GoodsLost_Form(request.POST)
        if form.is_valid():
            statusForm = request.POST['statusForm']
            #fk_responsibleperson: qs('input#id_fk_reponsibleperson').value | |0,
            #fk_lostby: qs('input#id_fk_lostby').value | |0,
            #fk_goods_outwards: qs('input#id_fk_goods_outwards').value | |0,
            #fk_goods_lending: qs('input#id_fk_goods_lending').value | |0,
            #fk_maintenance: qs('input#id_fk_maintenance').value | |0,
            if statusForm == 'Add':
                data = getFormData(request, form)
                createddate = datetime.now()
                createdby = request.user.username
                data.update(fk_responsibleperson=(None if int(
                data['fk_responsibleperson']) == 0 else data['fk_responsibleperson']))
                data.update(fk_lostby=(None if int(
                    data['fk_lostby']) == 0 else data['fk_lostby']))
                data.update(fk_goods_outwards=(None if int(
                            data['fk_goods_outwards']) == 0 else data['fk_goods_outwards']))
                data.update(fk_goods_lending=(None if int(
                            data['fk_goods_lending']) == 0 else data['fk_goods_lending']))
                data.update(fk_maintenance=(None if int(
                                data['fk_maintenance']) == 0 else data['fk_maintenance']))
                data['createddate'] = createddate
                data['createdby'] = createdby
                #chek NIK
                ValidNIK = Employee.objects.existByNIK(data['nik_used'])
                if not ValidNIK:
                    return HttpResponse(json.dumps({'message': 'NIK Used by is not valid '}), status=403, content_type='application/json')
                
                ValidNIK = Employee.objects.existByNIK(data['nik_resp'])
                if not ValidNIK:
                    return HttpResponse(json.dumps({'message': 'NIK responsible person is not valid '}), status=403, content_type='application/json')                
                ValidNIK = Employee.objects.existByNIK(data['nik_lostby'])
                if not ValidNIK:
                    return HttpResponse(json.dumps({'message': 'NIK lost by person is not valid '}), status=403, content_type='application/json')
                ValidSN = NAGoodsReceive.objects.hasExistedSN(data['serialnumber'])
                if not ValidSN:
                    return HttpResponse(json.dumps({'message': 'invalid serial number'}), status=403, content_type='application/json')
                result = NAGoodsLost.objects.SaveData(StatusForm.Input, **data)
                #statusResp = 200
                #if result[0] != 'success':
                #    statusResp = 500
                #return HttpResponse(json.dumps(result), status=statusResp, content_type='application/json')
            elif statusForm == 'Edit':
                data = getFormData(request, form, status_form='Edit')
                data.update(fk_lostby=(None if int(
                            data['fk_responsibleperson']) == 0 else data['fk_responsibleperson']))
                data.update(fk_lostby=(None if int(
                            data['fk_lostby']) == 0 else data['fk_lostby']))
                data.update(fk_goods_outwards=(None if int(
                            data['fk_goods_outwards']) == 0 else data['fk_goods_outwards']))
                data.update(fk_goods_lending=(None if int(
                            data['fk_goods_lending']) == 0 else data['fk_goods_lending']))
                data.update(fk_maintenance=(None if int(
                            data['fk_maintenance']) == 0 else data['fk_maintenance']))
                idapp = request.POST['idapp']
                data['idapp'] = idapp
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = request.user.username
                result = NAGoodsLost.objects.SaveData(StatusForm.Edit, **data)
            statusResp = 200
            if result[0] != 'success':
                statusResp = 500
            return HttpResponse(json.dumps(result), status=statusResp, content_type='application/json')
        elif not form.is_valid():
            return HttpResponse('form not valid',status=403)
    elif request.method == 'GET':
        idapp = request.GET['idapp']
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            result = NAGoodsLost.objects.retriveData(idapp)
            if result[0] == 'success':
                form = NA_GoodsLost_Form(initial=result[1])
                #form.fields['status_goods'] = forms.ChoiceField(required=False,widget=forms.Select(attrs={
                #    'class':'NA-Form-Control', 'style':'width:130px;'}),choices=(('L','Lost'),('F','Find')))
            elif result[0] == 'Lost':
                return HttpResponse('Lost',status=404)
        else:
            form = NA_GoodsLost_Form()
        form.statusForm = statusForm
        return render(request, 'app/MasterData/NA_Entry_GoodsLost.html', {'form': form})

#@api_view(['GET'])
def GetGoodsBySN(request,SN=''):
    sn = SN
    if not sn:
        sn = request.GET.get('serialno')
    HasTrans = NAGoodsHistory.objects.filter(serialnumber__iexact=sn).exists()
    resp = {}  
    if HasTrans:
        data = NAGoodsHistory.objects.filter(Q(serialnumber__iexact=sn) \
                & Q(fk_return__isnull=True) & Q(fk_disposal__isnull=True) \
                & Q(fk_lost__isnull=True)) \
                .filter(Q(fk_maintenance__isnull=False) \
                    | Q(fk_lending__isnull=False) \
                    | Q(fk_outwards__isnull=False)) \
                .values('fk_outwards', 'fk_lending', 'fk_maintenance')
        if data:
            #idapp,fk_goods,itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods=
            # tbl_name = GO/GL/GM,fk_employee=empl_used,nik_employee,fk_resp, nik_resp
            if data[0]['fk_outwards']:
                #get data from goods outwards
               resp = NAGoodsOutwards.objects.getDatabySN(sn)
               #ambil data
               #idapp = resp["idapp"]
               #serializer = NAGoodsOutWordsSerializer(instance=resp,many=True)
            elif data[0]['fk_lending']:
                resp = NAGoodsLending.objects.getDatabySN(sn)
                #serializer =NAGoodLendingSerializer(instance=resp)
            elif data[0]['fk_maintenance']:
                resp = NAMaintenance.objects.getDatabySN(sn)
                #serializer = 
            #serializer = NAGoodsLostSerializer(instance=resp,many=True)
            #return Response(serializer.data)
            return HttpResponse(json.dumps(resp[0],cls=DjangoJSONEncoder),content_type='application/json')
        else:
            return HttpResponse(json.dumps(resp[0],cls=DjangoJSONEncoder),content_type='application/json')

def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '') 
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    tabs_section = request.GET.get('tab_section')
    Ilimit = request.GET.get('rows', '')
    NAData = NAGoodsLost.objects.searchGoods_byForm({'goods_filter':goodsFilter,'tab_section':tabs_section})
    if NAData[1] == []:
        results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
    else:
        totalRecord = len(NAData[1])
        paginator = Paginator(NAData[1], int(Ilimit)) 
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
        if NAData[0] == 'g_maintenance':
            for row in dataRows.object_list:
                i+=1
                datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],row['fk_goods'],i,row['itemcode'],row['goods'],\
                    row['serialnumber'],row['tbl_name']]}
                rows.append(datarow)
        else:
            for row in dataRows.object_list:
                i+=1
                datarow = {"id" :str(row['idapp']) +'_fk_goods', "cell" :[row['idapp'],row['fk_goods'],i,row['itemcode'],row['goods'],\
                    row['serialnumber'],row['tbl_name'],row['fk_employee'],row['nik_employee'],row['used_employee'],row['fk_resp'],row['nik_resp'],row['employee_responsible']]}
                rows.append(datarow)
        results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
