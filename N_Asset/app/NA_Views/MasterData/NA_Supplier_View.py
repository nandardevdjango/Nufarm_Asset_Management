import datetime
import json

from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render

from NA_DataLayer.common import (
    ResolveCriteria,
    Data,
    Message,
    commonFunct,
    decorators
)
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from NA_DataLayer.logging import LogActivity
from NA_Models.models import NASupplier


@decorators.ensure_authorization
def NA_Supplier(request):
    return render(request, 'app/MasterData/NA_F_Supplier.html')


@decorators.ajax_required
@decorators.detail_request_method('GET')
def NA_SupplierGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey = request.GET.get('valueKey')
    IdataType = request.GET.get('dataType')
    Icriteria = request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    if(',' in Isidx):
        Isidx = Isidx.split(',')

    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    if(Isord is not None and str(Isord) != ''):
        suplData = NASupplier.objects.PopulateQuery(
            IcolumnName,
            IvalueKey,
            criteria,
            dataType
        ).order_by('-' + str(Isidx))
    else:
        suplData = NASupplier.objects.PopulateQuery(
            IcolumnName,
            IvalueKey,
            criteria, dataType
        )

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
        datarow = {
            "id": row['suppliercode'], "cell": [
                i,
                row['suppliercode'],
                row['suppliername'],
                row['address'],
                row['telp'],
                row['hp'], row['contactperson'],
                row['inactive'],
                row['createddate'],
                row['createdby']
            ]
        }
        rows.append(datarow)
    results = {
        "page": page,
        "total": paginator.num_pages,
        "records": totalRecord,
        "rows": rows
    }
    return HttpResponse(
        json.dumps(results, indent=4, cls=DjangoJSONEncoder),
        content_type='application/json'
    )


class NA_Supplier_form(forms.Form):
    suppliercode = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Enter Supplier Code',
                'style': 'width:200px'
            }
        ))
    suppliername = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Enter Supplier Name',
                'style': 'width:220px'
            }
        ))
    address = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Address of Supplier',
                'cols': '100',
                'rows': '2',
                'style': 'height: 50px;max-height:70px;width:430px;max-width:430px'
            }
        ))
    telp = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Telp',
                'style': 'width:200px'}))
    hp = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Phone Number',
                'style': 'width:220px'}))
    contactperson = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'NA-Form-Control',
                'placeholder': 'Contact Person',
                'style': 'width:200px'}))
    inactive = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    mode = forms.CharField(widget=forms.HiddenInput())
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    @transaction.atomic
    def save(self, user):
        data = self.cleaned_data
        mode = self.cleaned_data.get('mode')
        supplier = NASupplier()
        force_insert = True
        activity = 'Created'
        if mode == 'Add':
            data.update({
                'createddate': datetime.datetime.now(),
                'createdby': user
            })
        elif mode == 'Edit':
            activity = 'Updated'
            try:
                supplier = NASupplier.objects.get(
                    suppliercode=self.cleaned_data.get('suppliercode')
                )
            except NASupplier.DoesNotExist:
                raise NAError(
                    error_code=NAErrorConstant.DATA_LOST
                )

            data.update({
                'modifieddate': datetime.datetime.now(),
                'modifiedby': user
            })
            force_insert = False
            del data['suppliercode']

        del(data['mode'], data['initializeForm'])

        for key, value in data.items():
            setattr(supplier, key, value)

        try:
            supplier.save(force_insert=force_insert)
        except IntegrityError as e:
            raise NAError(
                error_code=NAErrorConstant.DATA_EXISTS,
                message=e,
                instance=supplier
            )
        else:
            log = LogActivity(
                models=NASupplier,
                activity=activity,
                user=user,
                data=supplier
            )
            log.record_activity()
        return Data.Success,


@decorators.ensure_authorization
@decorators.read_permission(form_name=NASupplier.FORM_NAME_ORI)
def EntrySupplier(request):
    if request.method == 'POST':
        form = NA_Supplier_form(request.POST)
        if form.is_valid():
            try:
                result = form.save(user=request.user.username)
            except NAError as e:
                if e.error_code == NAErrorConstant.DATA_EXISTS:
                    result = NAErrorHandler.handle_data_exists(err=e)
                elif e.error_code == NAErrorConstant.DATA_LOST:
                    raise NotImplementedError
        else:
            result = NAErrorHandler.handle_form_error(form_error=form.errors)
        return commonFunct.response_default(result)
    elif request.method == 'GET':
        supplier_code = request.GET['suppliercode']
        mode = request.GET['mode']
        if mode == 'Edit' or mode == 'Open':
            try:
                result = NASupplier.objects.get(suppliercode=supplier_code)
            except NASupplier.DoesNotExist:
                return HttpResponse(
                    json.dumps(
                        {
                            'message': Message.get_lost_info(pk=supplier_code,
                                                             table='supplier')
                        }
                    ),
                    status=404,
                    content_type='application/json'
                )
            else:
                form = NA_Supplier_form(initial=forms.model_to_dict(result))
                form.fields['suppliercode'].widget.attrs['disabled'] = 'disabled'
                return render(
                    request,
                    'app/MasterData/NA_Entry_Supplier.html',
                    {'form': form}
                )
        else:
            form = NA_Supplier_form()
            return render(
                request,
                'app/MasterData/NA_Entry_Supplier.html',
                {'form': form}
            )


@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
    cols = []
    cols.append({'name': 'suppliercode',
                 'value': 'suppliercode',
                 'selected': '',
                 'dataType': 'varchar',
                 'text': 'Supplier Code'})
    cols.append({'name': 'suppliername',
                 'value': 'suppliername',
                 'selected': 'True',
                 'dataType': 'varchar',
                 'text': 'Supplier Name'})
    cols.append({'name': 'address',
                 'value': 'address',
                 'selected': '',
                 'dataType': 'varchar',
                 'text': 'Address'})
    cols.append({'name': 'telp', 'value': 'telp', 'selected': '',
                 'dataType': 'varchar', 'text': 'Telp'})
    cols.append({'name': 'hp', 'value': 'hp', 'selected': '',
                 'dataType': 'varchar', 'text': 'Hp'})
    cols.append({'name': 'contactperson',
                 'value': 'contactperson',
                 'selected': '',
                 'dataType': 'varchar',
                 'text': 'Contact Person'})
    cols.append({'name': 'inactive',
                 'value': 'inactive',
                 'selected': '',
                 'dataType': 'boolean',
                 'text': 'InActive'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols})


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('POST')
@decorators.read_permission(form_name=NASupplier.FORM_NAME_ORI, action='Delete')
def NA_Supplier_delete(request):
    supplier_code = request.POST.get('suppliercode')
    if NASupplier.objects.HasRef(supplier_code):
        result = Data.HasRef, Message.HasRef_del
        return commonFunct.response_default(result)
    try:
        supplier = NASupplier.objects.get(suppliercode=supplier_code)
        result = Data.Success,
    except NASupplier.DoesNotExist:
        result = Data.Lost,
    else:
        with transaction.atomic():
            log = LogActivity(
                models=NASupplier,
                activity='Deleted',
                user=request.user.username,
                data=supplier
            )
            log.record_activity()
            supplier.delete()
            raise Exception('error taiii ...')
    return commonFunct.response_default(result)


@decorators.ajax_required
@decorators.detail_request_method('GET')
def SearchSupplierbyForm(request):
    """get supplier data for grid return supplier code,suppliername, criteria = icontains"""
    searchText = request.GET.get('suppliername')
    Ilimit = request.GET.get('rows')
    Isidx = request.GET.get('sidx')
    Isord = request.GET.get('sord')
    NAData = NASupplier.objects.getSupplierByForm(searchText)
    if NAData == Data.Empty:
        results = {"page": "1", "total": 0, "records": 0, "rows": []}
        return HttpResponse(
            json.dumps(results, indent=4, cls=DjangoJSONEncoder),
            content_type='application/json'
        )
    try:
        multi_sort = commonFunct.multi_sort_queryset(NAData, Isidx, Isord)
    except ValueError:
        multi_sort = NAData
    else:
        NAData = multi_sort
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
    i = 0
    for row in dataRows.object_list:
        i += 1
        datarow = {
            "id": row['suppliercode'], "cell": [
                i, row['suppliercode'], row['suppliername'], row['address']
            ]
        }
        rows.append(datarow)
    results = {
        "page": page,
        "total": paginator.num_pages,
        "records": totalRecord,
        "rows": rows}
    return HttpResponse(
        json.dumps(
            results,
            indent=4,
            cls=DjangoJSONEncoder),
        content_type='application/json')
