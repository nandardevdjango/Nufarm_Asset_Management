from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, CriteriaSearch, commonFunct, StatusForm, Data, decorators
from NA_Models.models import NAGoodsReturn,goods
from django import forms
from datetime import datetime

def NA_Goods_Return(request):
    return render(request,'app/Transactions/NA_F_Goods_Return.html')
def NA_Goods_ReturnGetData(request):
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
        table=[NAGoodsReturn,goods],
        resolve=IcolumnName,
        initial_name=['ngr','g','emp1','emp2'],
        custom_fields=[['fromemployee'],['usedemployee']]
    )
    maintenanceData = NAGoodsReturn.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType)
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
            "id" :row['idapp'], "cell" :[
                row['idapp'],i,row['goods'],row['serialnumber'],row['fromemployee'],row['usedemployee'],row['datereturn'],
                row['conditions'],row['minusDesc'],row['iscompleted'],row['descriptions'],row['createddate'],row['createdby']
                ]
            }
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')

def getFormData(request,form):
    clData = form.cleaned_data
    data = {
        'fk_goods':clData['fk_goods'],'serialNumber':clData['serialNumber'],'conditions':clData['conditions'],
        'minus':clData['minus'],'datereturn':clData['datereturn'],'iscompleted':clData['iscompleted'],
        'idapp_fromemployee':clData['idapp_fromemployee'],'idapp_usedemployee':clData['idapp_usedemployee'],
        'typeApp':clData['typeApp'],'descriptions':clData['descriptions']
        }
    fk_goods_outwards = clData.get('idapp_fk_goods_outwards')
    if fk_goods_outwards == '' or fk_goods_outwards is None:
        fk_goods_outwards = 'NULL'
    fk_goods_lend = clData.get('idapp_fk_goods_lend')
    if fk_goods_lend == '' or fk_goods_lend is None:
        fk_goods_lend = 'NULL'
    data['fk_goods_outwards'] = fk_goods_outwards
    data['fk_goods_lend'] = fk_goods_lend
    return data

class NA_Goods_Return_Form(forms.Form):
    fk_goods = forms.CharField(required=True,widget=forms.HiddenInput())
    typeApp = forms.CharField(widget=forms.HiddenInput(),required=True)
    itemcode = forms.CharField(required=True,label='Search goods',widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'Item code','style':'width:110px;'}))
    goods = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'Goods'}))
    serialNumber = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','disabled':'disabled','placeholder':'serial number','style':'width:325px;'}))
    fromemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'from employee'}))
    nik_fromemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'nik','style':'width:110px;'}))
    usedemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'used employee','style':'width:210px;'}))
    nik_usedemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','disabled':'disabled','placeholder':'nik','style':'width:110px;'}))
    datereturn = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'Date Return','style':'width:110px;'}))
    conditions = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'NA-Form-Control select inline-field','style':'width:110px;margin-left:auto;'}),
                                  choices=(
                                      ('1', 'Condition 1'),
                                      ('2', 'Condition 2'),
                                      ('3', 'Condition 3')
                                      )
                                  )
    minus = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'minus','style':'width:325px;'}))
    iscompleted = forms.BooleanField(required=False,widget=forms.CheckboxInput(
        attrs={'style':'margin-left:15px;position:absolute'}))
    descriptions = forms.CharField(required=True,widget=forms.Textarea(
        attrs={'class':'NA-Form-Control','placeholder':'Descriptions','style':'width:426px;height:45px;max-width:426px;max-height:90px;'}))
    idapp_fromemployee = forms.CharField(widget=forms.HiddenInput(),required=True)
    idapp_usedemployee = forms.CharField(widget=forms.HiddenInput(),required=True)
    idapp_fk_goods_outwards = forms.CharField(widget=forms.HiddenInput(),required=False)
    idapp_fk_goods_lend = forms.CharField(widget=forms.HiddenInput(),required=False)
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

def Entry_GoodsReturn(request):
    getUser = str(request.user.username)
    if request.method == 'POST':
        form = NA_Goods_Return_Form(request.POST)
        if form.is_valid():
            data = getFormData(request,form)
            statusForm = request.POST['statusForm']
            result = None
            if statusForm == 'Add':
                data['createddate'] = datetime.now()
                data['createdby'] = getUser
                result = NAGoodsReturn.objects.SaveData(StatusForm.Input,**data)
            elif statusForm == 'Edit':
                idapp = request.POST['idapp']
                data['idapp'] = idapp
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = getUser
                result = NAGoodsReturn.objects.SaveData(StatusForm.Edit,**data)
            return commonFunct.response_default(result)
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data = NAGoodsReturn.objects.retrieveData(idapp) #tuple data
            iscompleted = data['iscompleted']
            if iscompleted == 1:
                data['iscompleted'] = True
            else:
                data['iscompleted'] = False
            data['datereturn'] = data['datereturn'].strftime('%d/%m/%Y')
            form = NA_Goods_Return_Form(initial=data)
            return render(request,'app/Transactions/NA_Entry_Goods_Return.html',{'form':form})
        else:
            form = NA_Goods_Return_Form()
        return render(request,'app/Transactions/NA_Entry_Goods_Return.html',{'form':form})

@decorators.ajax_required
@decorators.detail_request_method('POST')
def Delete_data(request):
    if request.user.is_authenticated():
        idapp = request.POST['idapp']
        result = NAGoodsReturn.objects.DeleteData(idapp)
        return HttpResponse('success')

@decorators.ajax_required
@decorators.detail_request_method('GET')
def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    Ilimit = request.GET.get('rows', '')
    NAData = NAGoodsReturn.objects.SearchGoods_byForm(goodsFilter)
    if NAData == []:
        results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
    else:
        totalRecord = len(NAData)
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
                "id" :str(row['idapp']) +'_fk_goods', "cell" :[
                    row['idapp'],i,row['itemcode'],row['goods'],row['serialnumber'],row['fromgoods'],row['fk_goods'],row['typeapp']
                    ]
                }
            rows.append(datarow)
        results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

@decorators.ajax_required
@decorators.detail_request_method('GET')
def get_GoodsData(request):
    idapp = request.GET['idapp']
    fromgoods = request.GET['fromgoods']
    result = NAGoodsReturn.objects.getGoods_data(idapp,fromgoods)
    return commonFunct.response_default(result)
