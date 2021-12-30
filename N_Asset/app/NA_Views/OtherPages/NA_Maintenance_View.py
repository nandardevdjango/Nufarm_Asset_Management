from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, CriteriaSearch, commonFunct, StatusForm, Data
from NA_Models.models import NAMaintenance, goods
from django import forms
from datetime import datetime
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def NA_Maintenance(request):
    return render(request, 'app/MasterData/NA_F_Maintenance.html', {'CompanyName': 'Nufarm', 'title': 'Goods Maintenance'})


def ShowCustomFilter(request):
    if request.is_ajax():
        cols = []
        cols.append({'name': 'goods', 'value': 'goods', 'selected': 'True',
                     'dataType': 'varchar', 'text': 'Goods name'})
        cols.append({'name': 'goodstype', 'value': 'typeapp',
                     'selected': '', 'dataType': 'varchar', 'text': 'Goods type'})
        cols.append({'name': 'serialnumber', 'value': 'serialnumber',
                     'selected': '', 'dataType': 'varchar', 'text': 'Serial Number'})
        cols.append({'name': 'requestdate', 'value': 'requestdate',
                     'selected': '', 'dataType': 'datetime', 'text': 'Date Requested'})
        cols.append({'name': 'startdate', 'value': 'startdate',
                     'selected': '', 'dataType': 'datetime', 'text': 'Start Date'})
        cols.append({'name': 'enddate', 'value': 'enddate',
                     'selected': '', 'dataType': 'datetime', 'text': 'End Date'})
        cols.append({'name': 'isstillguarante', 'value': 'isstillguarante',
                     'selected': '', 'dataType': 'boolean', 'text': 'Still Has Warranty'})
        cols.append({'name': 'maintenanceby', 'value': 'maintenanceby',
                     'selected': '', 'dataType': 'varchar', 'text': 'Maintenance By'})
        cols.append({'name': 'personalname', 'value': 'personalname',
                     'selected': '', 'dataType': 'varchar', 'text': 'Person Name'})
        cols.append({'name': 'isfinished', 'value': 'isfinished',
                     'selected': '', 'dataType': 'boolean', 'text': 'Is Finished'})
        cols.append({'name': 'issucced', 'value': 'issucced',
                     'selected': '', 'dataType': 'boolean', 'text': 'Is Succed'})
        cols.append({'name': 'expense', 'value': 'expense',
                     'selected': '', 'dataType': 'decimal', 'text': 'Cost Expense'})
        cols.append({'name': 'descriptions', 'value': 'descriptions',
                     'selected': '', 'dataType': 'varchar', 'text': 'descriptions/Remark'})
        cols.append({'name': 'createdby', 'value': 'createdby',
                     'selected': '', 'dataType': 'varchar', 'text': 'Created By'})
        cols.append({'name': 'createddate', 'value': 'createddate',
                     'selected': '', 'dataType': 'datetime', 'text': 'Created Date'})
        return render(request, 'app/UserControl/customFilter.html', {'cols': cols, 'CompanyName': 'Nufarm', 'title': 'Maintenance'})


def NA_MaintenanceGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey = request.GET.get('valueKey')
    IdataType = request.GET.get('dataType')
    Icriteria = request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    NAData = []
    if(Isord is not None and str(Isord) != '') or (Isidx is not None and str(Isidx) != ''):
        NAData = NAMaintenance.objects.PopulateQuery(str(Isidx), Isord, Ilimit, request.GET.get(
            'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
    else:
        NAData = NAMaintenance.objects.PopulateQuery('', 'DESC', Ilimit, request.GET.get(
            'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
    totalRecord = NAData[1]
    dataRows = NAData[0]

    # totalRecords = len(maintenanceData)
    # paginator = Paginator(maintenanceData,Ilimit)
    # try:
    #     dataRows = paginator.page(Ipage)
    # except EmptyPage:
    #     dataRows = paginator.page(paginator.num_pages)
    # rows = []
    # i = 0
    if NAData == []:
        results = {"page": "1", "total": 0, "records": 0, "rows": []}
    else:
        totalRecord = NAData[1]
        dataRows = NAData[0]
    rows = []
    i = 0
    for row in dataRows:
        i += 1
        datarow = {"id": row['idapp'], "cell": [row['idapp'], i, row['goods'], row['itemcode'], row['serialnumber'], row['requestdate'],
                                                row['startdate'], row['isstillguarantee'], row['expense'], row['maintenanceby'], row[
            'personalname'], row['enddate'], row['isfinished'], row['issucced'],
            row['descriptions'], row['createddate'], row['createdby']]}
        rows.append(datarow)
    TotalPage = 1 if totalRecord < int(Ilimit) else (
        math.ceil(float(totalRecord/int(Ilimit))))  # round up to next number
    results = {"page": int(request.GET.get('page', '1')),
               "total": TotalPage, "records": totalRecord, "rows": rows}
    return HttpResponse(json.dumps(results, indent=4, cls=DjangoJSONEncoder), content_type='application/json')


def getFormData(request, form):
    clData = form.cleaned_data
    data = {'fk_goods': clData['fk_goods'], 'typeApp': clData['typeApp'], 'serialNum': clData['serialNum'], 'itemcode': clData['itemcode'], 'goods': clData['goods'],
            'requestdate': clData['requestdate'], 'startdate': clData['startdate'], 'isstillguarantee': clData['isstillguarantee'], 'expense': clData['expense'],
            'maintenanceby': clData['maintenanceby'], 'personalname': clData['personalname'], 'isfinished': clData['isfinished'], 'issucced': clData['issucced'], 'enddate': clData['enddate'],
            'descriptions': clData['descriptions']}
    return data


class NA_Maintenance_Form(forms.Form):
    idapp  = forms.IntegerField(widget=forms.HiddenInput(),required=False)
    fk_goods = forms.CharField(required=True, widget=forms.HiddenInput())
    itemcode = forms.CharField(required=True, label='Search goods', widget=forms.TextInput(attrs={
        'disabled': 'disabled', 'class': 'NA-Form-Control', 'placeholder': 'Item code', 'style': 'width:110px;'}))
    goods = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'disabled': 'disabled', 'placeholder': 'Goods'}))
    typeApp = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'disabled': 'disabled', 'placeholder': 'type of goods', 'style': 'width:110px;'}))
    serialNum = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'serial number', 'autocomplete': 'off', 'style': 'width:225px;'}))
    minus = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'disabled': 'disabled', 'placeholder': 'minus', 'autocomplete': 'off', 'style': 'width:225px;'}))
    requestdate = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Request Date', 'autocomplete': 'off', 'style': 'width:110px;'}))
    startdate = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Start Date', 'autocomplete': 'off', 'style': 'width:110px;'}))
    isstillguarantee = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'disabled': 'disabled', 'style': 'float: left;margin-bottom: 20px;margin-right: 5px;'}))
    expense = forms.DecimalField(required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': '0.00', 'autocomplete': 'off', 'style': 'width:180px;', 'patern': '^[0-9]+([\.,][0-9]+)?$', 'step': 'any', 'tittle': 'Please enter valid value'}))
    maintenanceby = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Maintenance By', 'style': 'width:225px;'}))
    personalname = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Personal Name', 'style': 'width:320px;'}))
    issucced = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'style': 'margin-right:5px;float:left', }))
    isfinished = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'style': 'margin-right:5px;float:left', }))
    enddate = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'End Date', 'autocomplete': 'off', 'style': 'width:110px;'}))
    descriptions = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Descriptions', 'style': 'width:550px;height:45px;max-width:550px'}))
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)
    hasRefData = forms.BooleanField(widget=forms.HiddenInput(), required=False)


def EntryMaintenance(request):
    getUser = str(request.user.username)
    if request.method == 'POST':
        data = request.body
        data = json.loads(data)
        idapp:int=data['idapp']
        statusForm = data['statusForm']
        form = NA_Maintenance_Form(data)
        if form.is_valid():
            data = getFormData(request, form)
            result = None
            if statusForm == 'Add':
                data['createddate'] = datetime.now()
                data['createdby'] = getUser
                result = NAMaintenance.objects.SaveData(
                    StatusForm.Input, **data)
            elif statusForm == 'Edit':
                data.update(idapp=idapp)
                #data['idapp'] = idapp
                #idapp = request.POST['idapp']
                #data['issucced'] = 1 if data['issucced'] == 'true' else 0
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = getUser
                result = NAMaintenance.objects.SaveData(
                    StatusForm.Edit, **data)
            return commonFunct.response_default(result)
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data = NAMaintenance.objects.retriveData(idapp)  # tuple data
            if len(data[1]) <= 0:
                return HttpResponse('please enter good return first', status=404)
            statusResp = 200
            if data[0] == Data.Lost:
                statusResp = 404
                return HttpResponse('Lost', status=statusResp)
            if statusResp == 200:
                data[1][0].update(idapp=idapp)
                data[1][0]['hasRefData'] = True if data[1][0]['hasRefData'] == 'True' else False
                data[1][0]['isstillguarantee'] = True if data[1][0]['isstillguarantee'] == 1 else False
                data[1][0]['isfinished'] = True if data[1][0]['isfinished'] == 1 else False
                data[1][0]['issucced'] = True if data[1][0]['issucced'] == 1 else False
                data[1][0]['requestdate'] = data[1][0]['requestdate'].strftime(
                    '%d/%m/%Y')
                data[1][0]['startdate'] = data[1][0]['startdate'].strftime(
                    '%d/%m/%Y')
                data[1][0]['enddate'] = data[1][0]['enddate'].strftime(
                    '%d/%m/%Y')
                form = NA_Maintenance_Form(initial=data[1][0])
                return render(request, 'app/MasterData/NA_Entry_Maintenance.html', {'form': form})
        else:
            form = NA_Maintenance_Form()
        return render(request, 'app/MasterData/NA_Entry_Maintenance.html', {'form': form})


def Delete_M_data(request):
    if request.user.is_authenticated() and request.method == 'POST':
        idapp = request.POST['idapp']
        result = NAMaintenance.objects.DeleteData(idapp)
        return commonFunct.response_default(result)


def SearchGoodsbyForm(request):
    PageSize = request.GET.get('rows', '')
    PageIndex = request.GET.get('page', '1')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    includeNotYetUsed = request.GET.get('includeNotYetUsed')

    NAData = NAMaintenance.objects.search_M_ByForm(goodsFilter, str(
        Isidx), Isord, PageSize, PageIndex, request.user.username, commonFunct.str2bool(includeNotYetUsed))
    if NAData == []:
        results = {"page": "1", "total": 0, "records": 0, "rows": []}
    else:
        totalRecord = len(NAData)
        paginator = Paginator(NAData, int(PageSize))
        try:
            page = request.GET.get('page', '1')
        except ValueError:
            page = 1
        try:
            dataRows = paginator.page(page)
        except (EmptyPage, InvalidPage):
            dataRows = paginator.page(paginator.num_pages)

        rows = []
        i = 0  # idapp,itemcode,goods
        for row in dataRows.object_list:
            i += 1
            datarow = {"id": i, "cell": [i, row['idapp'], row['ItemCode'], row['goods'], row['typeapp'], row['conditions'],
                                         row['still_guarantee'], row['SerialNumber'], row['minusdesc'], row['lastUsedInfo']]}
            rows.append(datarow)
        results = {"page": page, "total": paginator.num_pages,
                   "records": totalRecord, "rows": rows}
    return HttpResponse(json.dumps(results, indent=4, cls=DjangoJSONEncoder), content_type='application/json')


def get_GoodsData(request):
    if request.method == 'GET':
        idapp = request.GET['idapp']
        serialnumber = request.GET['serialnumber']
        result = NAMaintenance.objects.getGoods_data(idapp, serialnumber)
        return commonFunct.response_default(result)


def getPersonalName(request):
    IvalueKey = request.GET.get('term')
    dataRows = NAMaintenance.objects.getPersonalName(IvalueKey)
    results = []
    for datarow in dataRows:
        JsonResult = {}
        JsonResult['id'] = datarow['personalname']
        JsonResult['label'] = datarow['personalname']
        JsonResult['value'] = datarow['personalname']
        results.append(JsonResult)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')


def getMaintenanceBy(request):
    IvalueKey = request.GET.get('term')
    dataRows = NAMaintenance.objects.getMaintenanceBy(IvalueKey)
    results = []
    for datarow in dataRows:
        JsonResult = {}
        JsonResult['id'] = datarow['maintenanceby']
        JsonResult['label'] = datarow['maintenanceby']
        JsonResult['value'] = datarow['maintenanceby']
        results.append(JsonResult)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')


def getLastTransGoods(request):
    serialNO = request.GET.get('serialno')
    try:
        result = NAMaintenance.objects.getLastTrans(serialNO)
    # return(idapp, itemcode, goodsname+brandname+typeapp, typeapp, nik_usedemployee+usedemployee, still_guarantee, minusdesc)
        return HttpResponse(json.dumps({'idapp': result[0], 'itemcode': result[1], 'goods': result[2], 'type': result[3],
                                        'lastUsedInfo': result[4], 'still_guarantee': result[5], 'minusdesc': result[6], }), status=200, content_type='application/json')
    except Exception as e:
        result = repr(e)
        return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')
