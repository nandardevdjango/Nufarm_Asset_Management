import json
from datetime import datetime, date
from django import forms
from django.db import transaction
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import (ResolveCriteria, commonFunct,
                                 StatusForm, Data, decorators)
from NA_Models.models import (NAGaReceive, NAGaVnHistory,
                              goods, Employee, NASuplier)


def NA_Goods_Receive_GA(request):
    return render(request, 'app/Transactions/NA_F_Goods_Receive_GA.html')


def NA_Goods_Receive_GAGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey = request.GET.get('valueKey')
    IdataType = request.GET.get('dataType')
    Icriteria = request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    criteria = ResolveCriteria.getCriteriaSearch(Icriteria)
    dataType = ResolveCriteria.getDataType(IdataType)

    gaData = NAGaReceive.objects.PopulateQuery(
        IcolumnName,
        IvalueKey,
        criteria,
        dataType
    )
    totalRecords = len(gaData)
    paginator = Paginator(gaData, Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i += 1
        datarow = {
            "id": row['idapp'], "cell": [
                row['idapp'], i, row['goodsname'], row['brand'], row['typeapp'], row['received_by'], row['pr_by'],
                row['datereceived'], row['price'], row['supliername'], row['invoice_no'], row['machine_no'],
                row['chassis_no'], row['year_made'], row['colour'], row['model'], row['kind'], row['cylinder'], row['fuel'],
                row['descriptions'], row['createddate'], row['createdby']
            ]
        }
        rows.append(datarow)
    results = {"page": Ipage, "total": paginator.num_pages,
               "records": totalRecords, "rows": rows}
    return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder), content_type='application/json')


def getFormData(form):
    clData = form.cleaned_data
    data = {
        'idapp': clData['idapp'], 'refno': clData['refno'], 'fk_goods': clData['fk_goods'],
        'datereceived': clData['datereceived'], 'fk_suplier': clData['supliercode'],
        'fk_receivedby': clData['received_by'], 'fk_pr_by': clData['pr_by'],
        'invoice_no': clData['invoice_no'], 'typeapp': 'typeapp', 'brand': clData['brand'],
        'machine_no': clData['machine_no'], 'chassis_no': clData['chassis_no'],
        'price': clData['price'], 'descriptions': clData['descriptions']
    }
    return data


class NA_Goods_Receive_GA_Form(forms.Form):
    fk_goods = forms.ModelChoiceField(
        queryset=goods.objects.all(),
        widget=forms.HiddenInput()
    )
    itemcode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'itemcode',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ), required=False)
    goodsname = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'goods name'}
    ), required=False)

    supliercode = forms.ModelChoiceField(
        queryset=NASuplier.objects.all(),
        widget=forms.TextInput(
            attrs={'class': 'NA-Form-Control', 'placeholder': 'suplier code',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ))
    supliername = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'suplier name'}
    ), required=False)

    pr_by = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.HiddenInput()
    )
    pr_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'PR By',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ))
    pr_by_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'Employee Name'}
    ), required=False)

    received_by = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.HiddenInput()
    )
    received_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'Received By',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ))
    received_by_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'Employee Name'}
    ), required=False)

    datereceived = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'date received',
               'style': 'width:120px;display:inline-block;'}))
    brand = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'brand',
               'style': 'width:120px;display:inline-block;'}
    ))
    invoice_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'invoice no',
               'style': 'width:120px;display:inline-block;'}
    ))
    typeapp = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'type',
               'style': 'width:150px;display:inline-block;'}
    ))
    machine_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'machine no',
               'style': 'width:150px;display:inline-block;'}
    ))
    chassis_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'chassis no',
               'style': 'width:373px;display:inline-block;'}))
    year_made = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'year made',
               'style': 'width:120px;display:inline-block;'}))
    colour = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'colour',
               'style': 'width:150px;display:inline-block;'}
    ))
    model = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'model',
               'style': 'width:120px;display:inline-block;'}
    ))
    kind = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'kind',
               'style': 'width:150px;display:inline-block;'}
    ))
    cylinder = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'cylinder',
               'style': 'width:150px;display:inline-block;'}
    ))
    fuel = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'fuel',
               'style': 'width:120px;display:inline-block;'}
    ))
    price = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'price',
               'style': 'width:373px;display:inline-block;'}
    ))
    direct_enter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput()
    )
    # reg_no, fk_app, expired_reg, date_reg, bpkp_expired, remark
    reg_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'registration number',
               'style': 'width:200px;display:inline-block;'}
    ))
    fk_app = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    expired_reg = forms.DateField(widget=forms.HiddenInput())
    date_reg = forms.DateField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'registration date',
               'style': 'width:200px;display:inline-block'}
    ))
    bpkb_expired = forms.DateField(widget=forms.HiddenInput())
    remark = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'remark',
        'style': 'max-width:485px;width:485px;height:50px;max-height:60px;'}
    ))

    descriptions = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'description',
               'style': 'max-width:485px;width:485px;height:50px;max-height:60px;'}))
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    @transaction.atomic
    def save(self, request):
        if self.is_valid():
            receive = NAGaReceive()
            receive.fk_goods = self.cleaned_data.get('fk_goods')
            receive.fk_receivedby = self.cleaned_data.get('received_by')
            receive.fk_p_r_by = self.cleaned_data.get('p_r_by')
            receive.fk_suplier = self.cleaned_data.get('supliercode')
            receive.brand = self.cleaned_data.get('brand')
            receive.datereceived = self.cleaned_data.get('datereceived')
            receive.invoice_no = self.cleaned_data.get('invoice_no')
            receive.typeapp = self.cleaned_data.get('typeapp')
            receive.machine_no = self.cleaned_data.get('machine_no')
            receive.chassis_no = self.cleaned_data.get('chassis_no')
            receive.year_made = self.cleaned_data.get('year_made') + '-1-1'
            receive.colour = self.cleaned_data.get('colour')
            receive.model = self.cleaned_data.get('model')
            receive.kind = self.cleaned_data.get('kind')
            receive.cylinder = self.cleaned_data.get('cylinder')
            receive.fuel = self.cleaned_data.get('fuel')
            receive.price = self.cleaned_data.get('price')
            receive.descriptions = self.cleaned_data.get('descriptions')
            receive.createddate = datetime.now()
            receive.createdby = request.user.username
            receive.save()

            if self.cleaned_data.get('direct_enter'):
                receive_history = NAGaVnHistory()
                receive_history.fk_app = receive
                receive_history.reg_no = self.cleaned_data.get('reg_no')
                receive_history.date_reg = self.cleaned_data.get('date_reg')
                receive_history.expired_reg = self.cleaned_data.get('expired_reg')
                receive_history.bpkp_expired = self.cleaned_data.get('bpkb_expired')
                receive_history.descriptions = self.cleaned_data.get('remark')
                receive_history.createddate = datetime.now()
                receive_history.createdby = request.user.username
                receive_history.save()

            return (Data.Success,)


def Entry_Goods_Receive_GA(request):
    if request.method == 'POST':
        form = NA_Goods_Receive_GA_Form(request.POST)
        statusForm = request.POST['statusForm']
        if form.is_valid():
            data = form.cleaned_data
            if statusForm == 'Add':
                data['createddate'] = datetime.now()
                data['createdby'] = request.user.username
                result = form.save(request=request)
            elif statusForm == 'Edit':
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = request.user.username
                result = NAGaReceive.objects.SaveData(StatusForm.Edit, **data)
            return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)

    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data, result = NAGaReceive.objects.retrieveData(idapp)
            if data == Data.Success:
                result = [i for i in result][0]
                if isinstance(result['datereceived'], datetime):
                    result['datereceived'] = result['datereceived'].strftime(
                        '%d/%m/%Y')

                if isinstance(result['year_made'], date):
                    result['year_made'] = result['year_made'].strftime('%Y')
                form = NA_Goods_Receive_GA_Form(initial=result)
            elif data == Data.Lost:
                return commonFunct.response_default((data, result))
        else:
            form = NA_Goods_Receive_GA_Form()
        return render(request, 'app/Transactions/NA_Entry_Goods_Receive_GA.html', {'form': form})


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
    cols.append({'name': 'refno', 'value': 'refno', 'selected': '',
                 'dataType': 'varchar', 'text': 'RefNO'})
    cols.append({'name': 'goods', 'value': 'goods', 'selected': 'True',
                 'dataType': 'varchar', 'text': 'goods name'})
    cols.append({'name': 'datereceived', 'value': 'datereceived',
                 'selected': '', 'dataType': 'datetime', 'text': 'Date Received'})
    cols.append({'name': 'supliername', 'value': 'supliername',
                 'selected': '', 'dataType': 'varchar', 'text': 'type of brand'})
    cols.append({'name': 'receivedby', 'value': 'receivedby',
                 'selected': '', 'dataType': 'varchar', 'text': 'Received By'})
    cols.append({'name': 'pr_by', 'value': 'pr_by', 'selected': '',
                 'dataType': 'varchar', 'text': 'Purchase Request By'})
    cols.append({'name': 'totalpurchase', 'value': 'totalpurchase',
                 'selected': '', 'dataType': 'int', 'text': 'Total Purchased'})
    cols.append({'name': 'totalreceived', 'value': 'totalreceived',
                 'selected': '', 'dataType': 'int', 'text': 'Total Received'})
    cols.append({'name': 'createdby', 'value': 'createdby',
                 'selected': '', 'dataType': 'varchar', 'text': 'Created By'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols})
