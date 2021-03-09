from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import json
from NA_DataLayer.common import ResolveCriteria, CriteriaSearch, commonFunct, StatusForm, Data,Message, decorators
from NA_Models.models import NAGoodsReturn,goods
from django import forms
from datetime import datetime
import math
def NA_Goods_Return(request):
    return render(request,'app/Transactions/NA_F_Goods_Return.html',{'CompanyName': 'Nufarm', 'title': 'Goods Return'})
def NA_Goods_ReturnGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    # getColumn = commonFunct.retriveColumn(
    #     table=[NAGoodsReturn,goods],
    #     resolve=IcolumnName,
    #     initial_name=['ngr','g','emp1','emp2'],
    #     custom_fields=[['fromemployee'],['usedemployee']]
    # )
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    NAData = []
    if(Isord is not None and str(Isord) != '') or (Isidx is not None and str(Isidx) != ''):
    	NAData = NAGoodsReturn.objects.PopulateQuery(str(Isidx),Isord,Ilimit, request.GET.get('page', '1'),request.user.username,IcolumnName,IvalueKey,criteria,dataType)#return tuples
    else:
    	NAData = NAGoodsReturn.objects.PopulateQuery('','DESC',Ilimit, request.GET.get('page', '1'),request.user.username,IcolumnName,IvalueKey,criteria,dataType)#return tuples
    totalRecord = NAData[1]
    dataRows = NAData[0]

    # returnData = NAGoodsReturn.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType)
    # # returnData = commonFunct.multi_sort_queryset(returnData,)
    # totalRecords = len(returnData)
    # paginator = Paginator(returnData,Ilimit)
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
    for row in dataRows:#.object_list:
        i+=1
        datarow = {
            "id" :row['idapp'], "cell" :[
                row['idapp'],i,row['goods'],row['serialnumber'],row['fromemployee'],row['usedemployee'],row['datereturn'],
                row['conditions'],row['minusDesc'],row['iscompleted'],row['isaccepted'],row['descriptions'],row['createddate'],row['createdby']
                ]
            }
        rows.append(datarow)
    # results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    # return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')
    TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
    results = {"page": int(request.GET.get('page', '1')),"total": TotalPage ,"records": totalRecord,"rows": rows}
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')
#def getLastTransGoods(request):

def getFormData(request,form):
    clData = form.cleaned_data
    data = {
        'fk_goods':clData['fk_goods'],'serialNumber':clData['serialNumber'],'conditions':clData['conditions'],
        'minus':clData['minus'],'datereturn':clData['datereturn'],'iscompleted':clData['iscompleted'],
        'idapp_fromemployee': clData['idapp_fromemployee'], 'idapp_usedemployee': clData['idapp_usedemployee'],
        'isaccepted':clData['isaccepted'],
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
    typeApp = forms.CharField(widget=forms.HiddenInput(),required=False)
    #itemcode = forms.CharField(required=True,label='Search goods',widget=forms.TextInput(
    #    attrs={'class':'NA-Form-Control inline-field','placeholder':'Item code','style':'width:180px;'})
    itemcode = forms.CharField(required=False,widget=forms.HiddenInput())
    goods = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'Goods'}))
    serialNumber = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'serial number','autocomplete':'off','style':'width:180px;'}))
    fromemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'from employee'}))
    nik_fromemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'nik','style':'width:180px;'}))
    usedemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control','disabled':'disabled','placeholder':'used employee','style':'width:100%;margin-right:auto'}))
    nik_usedemployee = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','disabled':'disabled','placeholder':'nik','style':'width:180px;'}))
    datereturn = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'Date Return','style':'width:180px;'}))
    conditions = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'NA-Form-Control select inline-field','style':'width:180px;margin-left:auto;'}),
                                    choices=(
                                        ('1', 'Good'),
                                        ('2', 'Less Good'),
                                        ('3', 'Broken'),
                                        ('4','Other/Undetermined'),
                                        )
                                    )
    minus = forms.CharField(required=True,widget=forms.TextInput(
        attrs={'class':'NA-Form-Control inline-field','placeholder':'minus','style':'width:479px;max-width:500px;'}))
    iscompleted = forms.BooleanField(required=False,widget=forms.CheckboxInput(
        attrs={'style':'margin-left:15px;position:absolute','checked':False}))
    descriptions = forms.CharField(required=True,widget=forms.Textarea(
        attrs={'class':'NA-Form-Control','placeholder':'Descriptions','style':'width:479px;height:45px;max-width:480px;max-height:90px;'}))
    idapp_fromemployee = forms.CharField(widget=forms.HiddenInput(),required=True)
    idapp_usedemployee = forms.CharField(widget=forms.HiddenInput(),required=True)
    idapp_fk_goods_outwards = forms.CharField(widget=forms.HiddenInput(),required=False)
    idapp_fk_goods_lend = forms.CharField(widget=forms.HiddenInput(), required=False)
    isaccepted = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'style': 'margin-left:15px;position:absolute','checked':False}))
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
            isaccepted = data['isaccepted']
            if isaccepted == 1:
                data['isaccepted'] = True
            else:
                data['isaccepted'] = False
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
        try:
            result = NAGoodsReturn.objects.DeleteData(idapp,request.user.username)
        except Exception as e:
            return HttpResponse(e)
        if isinstance(result,tuple):
            return HttpResponse(result[0])
        else:
            return HasReference(result)

@decorators.ajax_required
@decorators.detail_request_method('GET')
def SearchGoodsbyForm(request):
	Isidx = request.GET.get('sidx', 'goods')
	Isord = request.GET.get('sord', 'asc')
	goodsFilter = request.GET.get('goods_filter')
	PageIndex = request.GET.get('page', '1')
	Ilimit = request.GET.get('rows', '0')
	NAData = NAGoodsReturn.objects.SearchGoods_byForm(goodsFilter,str(Isidx),Isord,Ilimit,PageIndex, request.user.username)
	if NAData == []:
		results = {"page": "1","total": 0 ,"records": 0,"rows": [] }
	else:
		totalRecord = NAData[1]
		dataRows = NAData[0]
		#rows = []
		#totalRecord = len(NAData)
		#paginator = Paginator(NAData, int(Ilimit))
		#try:
		#	page = request.GET.get('page', '1')
		#except ValueError:
		#	page = 1
		#try:
		#	dataRows = paginator.page(page)
		#except (EmptyPage, InvalidPage):
		#	dataRows = paginator.page(paginator.num_pages)
		rows = []
		i = 0
		for row in dataRows:
			i+=1
			datarow = {
				"id" :str(row['idapp']) +'_fk_goods', "cell" :[
					row['idapp'],i,row['itemcode'],row['goods'],row['serialnumber'],row['fromgoods'],row['fk_goods'],row['employee_name'],row['typeapp']
					]
				}
			rows.append(datarow)
		TotalPage = 1 if totalRecord < int(Ilimit) else (math.ceil(float(totalRecord/int(Ilimit)))) # round up to next number
		results = {"page": int(PageIndex),"total": TotalPage ,"records": totalRecord,"rows": rows }
		#results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
		return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

@decorators.ajax_required
@decorators.detail_request_method('GET')
def get_GoodsData(request):
    idapp = request.GET['idapp']
    fromgoods = request.GET['fromgoods']
    result = NAGoodsReturn.objects.getGoods_data(idapp,fromgoods)
    return commonFunct.response_default(result)
@decorators.ajax_required
@decorators.detail_request_method('GET')
def getLastTrans(request):
	serialnumber = request.GET['serialnumber']
	result = ''
	try:
		result = NAGoodsReturn.objects.getLastTrans(serialnumber)
		if len(result) > 0:
			return commonFunct.response_default(result)
		else:
			return commonFunct.response_default((Data.Empty,))
	except Exception as e:
		return commonFunct.response_default((Data.Empty,e))

@decorators.ajax_required
def ShowCustomFilter(request):
    cols = []
    cols.append({'name':'goodsname','value':'goodsname','selected':'True','dataType':'varchar','text':'Goods Name'})
    cols.append({'name':'brandname','value':'brandname','selected':'','dataType':'varchar','text':'Brand Name'})
    cols.append({'name':'serialnumber','value':'serialnumber','selected':'','dataType':'varchar','text':'Serial Number'})
    cols.append({'name':'fromemployee','value':'fromemployee','selected':'','dataType':'varchar','text':'Return By'})
    cols.append({'name':'usedemployee','value':'usedemployee','selected':'','dataType':'varchar','text':'Used By'})
    cols.append({'name':'datereturn','value':'datereturn','selected':'','dataType':'varchar','text':'Date Return'})
    cols.append({'name':'conditions','value':'conditions','selected':'','dataType':'varchar','text':'Conditions'})
    cols.append({'name':'minusDesc','value':'minusDesc','selected':'','dataType':'varchar','text':'Minus'})

    return render(request, 'app/UserControl/customFilter.html', {'cols': cols})
