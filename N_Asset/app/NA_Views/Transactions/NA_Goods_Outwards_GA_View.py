import json
from datetime import datetime, date
from django import forms
from django.db import transaction
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import (ResolveCriteria, commonFunct,
                                 StatusForm, Data, decorators)
from NA_Models.models import (NAGaOutwards, goods, NASupplier, NAGaReceive,
                              NAGoodsEquipment, Employee, NAGaVnHistory)


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

    column = commonFunct.retriveColumn(
        table=[goods, NAGaReceive, NAGaVnHistory, NAGaOutwards],
        custom_fields=[
            ['employee'],
            ['used_employee'],
            ['resp_employee'],
            ['sender']
        ],
        resolve=IcolumnName,
        initial_name=['g', 'ngr', 'ngh', 'ngo',
                      'emp1', 'emp2', 'emp3', 'emp4'],
        exclude=['g.typeapp']
    )

    gaData = NAGaOutwards.objects.populate_query(
        column,
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
                row['idapp'], i, row['goodsname'], row['brand'], row['typeapp'],
                row['invoice_no'], row['reg_no'], row['isnew'], row['daterequest'],
                row['datereleased'], row['employee_name'], row['sender'],
                row['resp_employee'], row['equipment'], row['add_equipment'],
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
        'datereceived': clData['datereceived'], 'fk_supplier': clData['suppliercode'],
        'fk_receivedby': clData['received_by'], 'fk_pr_by': clData['pr_by'],
        'invoice_no': clData['invoice_no'], 'typeapp': 'typeapp', 'brand': clData['brand'],
        'machine_no': clData['machine_no'], 'chassis_no': clData['chassis_no'],
        'descriptions': clData['descriptions']
    }
    return data


class NAGaOutwardsForm(forms.Form):
    idapp = forms.IntegerField(required=False, widget=forms.HiddenInput())
    fk_app = forms.ModelChoiceField(
        queryset=NAGaVnHistory.objects.active(),
        widget=forms.HiddenInput()
    )

    fk_goods = forms.ModelChoiceField(
        queryset=goods.objects.filter(inactive=False),
        widget=forms.HiddenInput()
    )

    fk_receive = forms.ModelChoiceField(
        queryset=NAGaReceive.objects.all(),
        widget=forms.HiddenInput()
    )

    itemcode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'itemcode',
               'style': 'width:120px;display:inline-block;margin-right: 5px;'}
    ), required=False)

    goodsname = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'goods name'}
    ), required=False)

    typeapp = forms.CharField(widget=forms.HiddenInput(), required=False)
    colour = forms.CharField(widget=forms.HiddenInput(), required=False)
    invoice_no = forms.CharField(widget=forms.HiddenInput(), required=False)
    year_made = forms.CharField(widget=forms.HiddenInput(), required=False)

    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(inactive=False),
        widget=forms.HiddenInput()
    )

    employee_nik = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'employee',
            'style': 'width:120px;display:inline-block;margin-right: 5px;'
        }
    ), required=False)

    employee_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'employee name'}
    ), required=False)

    used_by = forms.ModelChoiceField(
        queryset=Employee.objects.filter(inactive=False),
        widget=forms.HiddenInput(),
        required=False
    )

    used_by_nik = forms.CharField(widget=forms.HiddenInput(), required=False)

    used_by_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    resp_employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(inactive=False),
        widget=forms.HiddenInput()
    )

    resp_employee_nik = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'responsible person',
            'style': 'width:120px;display:inline-block;margin-right: 5px;'
        }
    ), required=False)

    resp_employee_name = forms.CharField(disabled=True, widget=forms.TextInput(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'employee name'}
    ), required=False)

    sender = forms.ModelChoiceField(
        queryset=Employee.objects.filter(inactive=False),
        widget=forms.HiddenInput()
    )

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

    isnew = forms.BooleanField(widget=forms.HiddenInput())

    daterequest = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'NA-Form-Control',
            'placeholder': 'date request',
            'style': 'display:inline-block;width:150px'
        },
        format='%d/%m/%Y'
    ), input_formats=settings.DATE_INPUT_FORMATS)

    datereleased = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'NA-Form-Control',
            'placeholder': 'date released',
            'style': 'display:inline-block;width:150px'
        },
        format='%d/%m/%Y'
    ), input_formats=settings.DATE_INPUT_FORMATS)

    equipment = forms.ModelMultipleChoiceField(
        queryset=NAGoodsEquipment.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    add_equipment = forms.ModelMultipleChoiceField(
        queryset=NAGoodsEquipment.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )

    descriptions = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'NA-Form-Control', 'placeholder': 'description',
               'style': 'max-width:485px;width:485px;height:50px;max-height:60px;'}))
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    statusForm = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        if self.cleaned_data.get('statusForm') == 'Edit':
            if not self.cleaned_data.get('idapp'):
                raise forms.ValidationError({
                    'idapp': 'This field is required'
                })
        return super(NAGaOutwardsForm, self).clean()

    @transaction.atomic
    def save(self, user):
        status_form = self.cleaned_data.get('statusForm')
        outwards = NAGaOutwards()
        if status_form == 'Edit':
            outwards = NAGaOutwards.objects.get(
                idapp=self.cleaned_data.get('idapp')
            )
        outwards.fk_goods = self.cleaned_data.get('fk_goods')
        outwards.fk_app = self.cleaned_data.get('fk_app')
        outwards.fk_receive = self.cleaned_data.get('fk_receive')
        outwards.fk_employee = self.cleaned_data.get('employee')
        outwards.fk_usedemployee = self.cleaned_data.get('used_by')
        outwards.fk_responsibleperson = self.cleaned_data.get('resp_employee')
        outwards.fk_sender = self.cleaned_data.get('sender')
        outwards.isnew = self.cleaned_data.get('isnew')
        outwards.typeapp = self.cleaned_data.get('fk_goods').typeapp
        outwards.daterequest = self.cleaned_data.get('daterequest')
        outwards.datereleased = self.cleaned_data.get('daterequest')
        outwards.descriptions = self.cleaned_data.get('descriptions')
        equipment = self.cleaned_data.get('equipment')
        add_equipment = self.cleaned_data.get('add_equipment')
        if status_form == 'Add':
            outwards.createdby = user
            outwards.createddate = datetime.now()

            outwards.save()
            if equipment:
                outwards.equipment.add(*equipment)

            if add_equipment:
                outwards.add_equipment.add(*add_equipment)

        elif status_form == 'Edit':
            outwards.modifiedby = user
            outwards.modifieddate = datetime.now()

            outwards.equipment.remove(*equipment)
            if equipment:
                outwards.equipment.add(*equipment)

            outwards.add_equipment.remove(*add_equipment)
            if add_equipment:
                outwards.add_equipment.add(*add_equipment)
            outwards.save()

        return (Data.Success.value, )


def Entry_Goods_Outwards_GA(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['equipment'] = data.getlist('equipment[]')
        data['add_equipment'] = data.getlist('add_equipment[]')
        form = NAGaOutwardsForm(data)
        statusForm = request.POST['statusForm']
        if form.is_valid():
            data = form.cleaned_data
            result = form.save(user=request.user.username)
            return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)

    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data, result = NAGaOutwards.objects.retrieve_data(idapp)
            if data == Data.Success:
                result.update({
                    'daterequest': result.get('daterequest').strftime(
                        '%d/%m/%Y'
                    ),
                    'datereleased': result.get('datereleased').strftime(
                        '%d/%m/%Y'
                    )
                })

                if isinstance(result['year_made'], date):
                    result.update({
                        'year_made': result.get('year_made').strftime('%Y')
                    })
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
    cols.append({'name': 'suppliername', 'value': 'suppliername',
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
    return commonFunct.search_data_by_form(
        request=request,
        data=NAGaOutwards.objects.search_ga_by_form(q),
        fields=[
            'idapp',
            'itemcode',
            'goods',
            'reg_no',
            'expired_reg',
            'bpkb_expired',
            'info_is_new',
            'descriptions',
            'fk_receive',
            'fk_app',
            'typeapp',
            'invoice_no',
            'year_made',
            'colour'
        ]
    )
