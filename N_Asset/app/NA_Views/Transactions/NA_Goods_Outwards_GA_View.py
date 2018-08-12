import json
from datetime import datetime, date
from django import forms
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import (ResolveCriteria, commonFunct,
                                 StatusForm, Data, decorators)
from NA_Models.models import NAGaOutwards, goods, NASuplier, NAGoodsEquipment


def NA_Goods_Outwards_GA(request):
    return render(request, 'app/Transactions/NA_F_Goods_Outwards_GA.html')


def NA_Goods_Outwards_GAGetData(request):
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

    gaData = NAGaOutwards.objects.populate_query(
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
    results = {
        "page": Ipage,
        "total": paginator.num_pages,
        "records": totalRecords,
        "rows": rows
    }
    return HttpResponse(json.dumps(results, cls=DjangoJSONEncoder), content_type='application/json')


def getFormData(form):
    clData = form.cleaned_data
    data = {
        'idapp': clData['idapp'], 'refno': clData['refno'], 'fk_goods': clData['fk_goods'],
        'datereceived': clData['datereceived'], 'fk_suplier': clData['supliercode'],
        'fk_receivedby': clData['received_by'], 'fk_pr_by': clData['pr_by'],
        'invoice_no': clData['invoice_no'], 'typeapp': 'typeapp', 'brand': clData['brand'],
        'machine_no': clData['machine_no'], 'chassis_no': clData['chassis_no'],
        'descriptions': clData['descriptions']
    }
    return data

# idapp, fk_goods, fk_employee, typeapp, isnew, daterequest, daterealesed,
# fk_usedemployee, fk_frommaintenance, fk_responsibleperson, fk_sender, fk_stock,
# fk_lending, fk_return, fk_receive, descriptions


class NAGaOutwardsForm(forms.Form):
    fk_goods = forms.CharField(widget=forms.HiddenInput())

    itemcode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'itemcode',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ), required=False)

    goodsname = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'goods name'}
    ), required=False)

    employee = forms.CharField(widget=forms.HiddenInput())

    employee_nik = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'employee',
            'style': 'width:120px;display:inline-block;margin-right: 5px;'
        }
    ), required=False)

    employee_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'employee name'}
    ), required=False)

    used_by = forms.CharField(widget=forms.HiddenInput())

    used_by_nik = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'used by'}
    ), required=False)

    used_by_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'employee name'}
    ), required=False)

    resp_employee = forms.CharField(widget=forms.HiddenInput())

    resp_employee_nik = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'responsible person',
            'style': 'width:120px;display:inline-block;margin-right: 5px;'
        }
    ), required=False)

    resp_employee_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'employee name'}
    ), required=False)

    sender = forms.CharField(widget=forms.HiddenInput())

    sender_nik = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'sender',
            'style': 'width:120px;display:inline-block;margin-right: 5px;'
        }
    ), required=False)

    sender_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'employee name'
        }
    ), required=False)

    isnew = forms.BooleanField(widget=forms.CheckboxInput())

    daterequest = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control',
            'placeholder': 'date request',
            'style': 'display:inline-block;width:150px'
        }
    ))

    datereleased = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control',
            'placeholder': 'date released',
            'style': 'display:inline-block;width:150px'
        }
    ))

    typeapp = forms.CharField(widget=forms.HiddenInput())
    equipment = forms.CharField(widget=forms.HiddenInput())

    add_equipment = forms.CharField(widget=forms.HiddenInput())

    descriptions = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'description',
               'style': 'max-width:485px;width:485px;height:50px;max-height:60px;'}))
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    def save(self, request):
        outwards = NAGaOutwards()


def Entry_Goods_Outwards_GA(request):
    if request.method == 'POST':
        form = NAGaOutwardsForm(request.POST)
        statusForm = request.POST['statusForm']
        if form.is_valid():
            data = form.cleaned_data
            if statusForm == 'Add':
                data['createddate'] = datetime.now()
                data['createdby'] = request.user.username
                result = NAGaOutwards.objects.SaveData(
                    StatusForm.Input, **data)
            elif statusForm == 'Edit':
                data['modifieddate'] = datetime.now()
                data['modifiedby'] = request.user.username
                result = NAGaOutwards.objects.SaveData(StatusForm.Edit, **data)
            return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)

    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data, result = NAGaOutwards.objects.retrieveData(idapp)
            if data == Data.Success:
                result = [i for i in result][0]
                if isinstance(result['datereceived'], datetime):
                    result['datereceived'] = result['datereceived'].strftime(
                        '%d/%m/%Y')

                if isinstance(result['year_made'], date):
                    result['year_made'] = result['year_made'].strftime('%Y')
                form = NAGaOutwardsForm(initial=result)
            elif data == Data.Lost:
                return commonFunct.response_default((data, result))
        else:
            form = NAGaOutwardsForm()
        return render(
            request,
            'app/Transactions/NA_Entry_Goods_Outwards_GA.html',
            {
                'form': form,
                'equipments': NAGoodsEquipment.get_equipment(request)
            }
        )


@decorators.ajax_required
@decorators.detail_request_method('POST')
def Delete_data(request):
    idapp = request.POST['idapp']
    result = NAGaOutwards.objects.DeleteData(idapp)
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


def search_ga_by_form(request):
    q = request.GET.get('q', '')
    data = NAGaOutwards.objects.search_ga_by_form(q)
    return commonFunct.search_data_by_form(
        request,
        data,
        fields=['idapp, goods, reg_no, expired_reg, bpkb_expired, is_new, descriptions']
    )
