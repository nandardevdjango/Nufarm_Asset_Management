﻿import datetime
import json

from django import forms
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.shortcuts import render

from NA_DataLayer.common import (
    Data, ResolveCriteria,
    commonFunct, decorators, Message, StatusForm
)
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from NA_DataLayer.logging import LogActivity
from NA_Models.models import Employee
from NA_Worker.task import NATask
from NA_Worker.worker import NATaskWorker


@decorators.ensure_authorization
def NA_Employee(request):
    return render(request, 'app/MasterData/NA_F_Employee.html')


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('GET')
def NA_EmployeeGetData(request):
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
        emplData = Employee.objects.PopulateQuery(
            IcolumnName, IvalueKey, criteria, dataType).order_by('-' + str(Isidx))
    else:
        emplData = Employee.objects.PopulateQuery(
            IcolumnName, IvalueKey, criteria, dataType)
    emplData = commonFunct.multi_sort_queryset(emplData, Isidx, Isord)
    totalRecord = emplData.count()
    paginator = Paginator(emplData, int(Ilimit))
    try:
        page = request.GET.get('page', '1')
    except ValueError:
        page = 1
    try:
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
        data = paginator.page(paginator.num_pages)

    rows = []
    i = 0
    for row in data.object_list:
        i += 1
        datarow = {"id": row['idapp'], "cell": [
            row['idapp'],
            i,
            row['nik'],
            row['employee_name'],
            row['typeapp'],
            row['jobtype'],
            row['gender'],
            row['status'],
            row['telphp'],
            row['territory'],
            row['descriptions'],
            row['inactive'],
            row['createddate'],
            row['createdby']
        ]}
        rows.append(datarow)
    results = {"page": data.number, "total": paginator.num_pages,
               "records": totalRecord, "rows": rows}
    return HttpResponse(
        json.dumps(results, indent=4, cls=DjangoJSONEncoder),
        content_type='application/json'
    )


class NA_Employee_form(forms.Form):
    idapp = forms.IntegerField(required=False, widget=forms.HiddenInput())
    nik = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'Enter Nik'
        }
    ))
    employee_name = forms.CharField(max_length=40, required=True, widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'Enter Employee Name'
        }
    ))
    typeapp = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'Type of Employee'
        }), choices=(('', '--choose--'), ('K', 'Contract'), ('P', 'Permanent'), ('C', 'Casual')))
    jobtype = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Jobtype'}))
    gender = forms.CharField(required=True, widget=forms.RadioSelect(
        choices=[('M', 'Male'), ('F', 'Female')]))
    status = forms.CharField(required=True, widget=forms.RadioSelect(
        choices=[('S', 'Single'), ('M', 'Married')]))
    telphp = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'NA-Form-Control', 'placeholder': 'Phone Number'}))
    territory = forms.CharField(max_length=150, required=True, widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'Territory'
        }
    ))
    descriptions = forms.CharField(max_length=250, required=True, widget=forms.Textarea(
        attrs={
            'class': 'NA-Form-Control', 'placeholder': 'Descriptions of Employee',
            'cols': '100', 'rows': '2',
                    'style': 'height: 50px;clear:left;width:500px;max-width:600px'
        }
    ))
    inactive = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    mode = forms.CharField(widget=forms.HiddenInput(), required=False)
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    def clean(self):
        mode = self.cleaned_data.get('mode')
        if mode == 'Edit':
            idapp = self.cleaned_data.get('idapp')
            if not idapp:
                raise forms.ValidationError(
                    {'idapp': 'This Field is required'})
        return super(NA_Employee_form, self).clean()

    @transaction.atomic
    def save(self, user):
        mode = self.cleaned_data.get('mode')
        employee = Employee()
        initial_data = {}
        if mode == 'Edit':
            idapp = self.cleaned_data.get('idapp')
            try:
                employee = Employee.objects.get(idapp=idapp)
                initial_data.update({
                    'employee_name': employee.employee_name,
                    'employee_phone': employee.telphp,
                    'employee_inactive': employee.inactive
                })
            except employee.DoesNotExist:
                raise NAError(
                    error_code=NAErrorConstant.DATA_LOST,
                    model=Employee,
                    pk=idapp
                )
        form_data = self.cleaned_data
        del(form_data['mode'], form_data['initializeForm'])

        for key, value in form_data.items():
            setattr(employee, key, value)

        #activity = LogActivity.CREATED
        status = StatusForm.Input
        if mode == 'Add':
            employee.createddate = datetime.datetime.now()
            employee.createdby = user
            form_data.update(createddate=employee.createddate)
            form_data.update(createdby=employee.createddate)
        elif mode == 'Edit':
            #activity = LogActivity.UPDATED
            employee.modifieddate = datetime.datetime.now()
            employee.modifiedby = user
            form_data.update(modifieddate=employee.modifieddate)
            form_data.update(modifiedby=employee.modifieddate)
            status = StatusForm.Edit
        try:
            Employee.objects.SaveData(status, **form_data)
            # employee.save()
        except IntegrityError as e:
            raise NAError(
                error_code=NAErrorConstant.DATA_EXISTS,
                message=e,
                instance=employee
            )
        changed_data = {
            'employee_name': employee.employee_name,
            'employee_phone': employee.telphp,
            'employee_inactive': employee.inactive
        }
        diff = commonFunct.get_difference_dict_values(
            initial_data, changed_data)
        if diff:
            worker = NATaskWorker(
                func=NATask.task_update_notifications,
                args=[initial_data, diff]
            )
            worker.run()
        return Data.Success,


@decorators.ajax_required
@decorators.detail_request_method('POST')
def Set_InActive(request):
    idapp = request.POST['idapp']
    inactive = request.POST['inactive']
    result = Employee.objects.setInActive(
        idapp, commonFunct.str2bool(inactive))
    return commonFunct.response_default(result)


@decorators.ajax_required
@decorators.detail_request_method('GET')
def getJobType(request):
    IvalueKey = request.GET.get('term')
    TypesRows = Employee.objects.getJobType(IvalueKey)
    results = []
    for JobTyperow in TypesRows:
        JsonResult = {}
        JsonResult['id'] = JobTyperow['jobtype']
        JsonResult['label'] = JobTyperow['jobtype']
        JsonResult['value'] = JobTyperow['jobtype']
        results.append(JsonResult)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')


def getTerritories(request):
    IvalueKey = request.GET.get('term')
    TypesRows = Employee.objects.getTerritories(IvalueKey)
    results = []
    for JobTyperow in TypesRows:
        JsonResult = {}
        JsonResult['id'] = JobTyperow['territory']
        JsonResult['label'] = JobTyperow['territory']
        JsonResult['value'] = JobTyperow['territory']
        results.append(JsonResult)
    data = json.dumps(results, cls=DjangoJSONEncoder)
    return HttpResponse(data, content_type='application/json')


@decorators.ensure_authorization
@decorators.read_permission(form_name=Employee.FORM_NAME_ORI)
def EntryEmployee(request):
    if request.method == 'POST':
        form = NA_Employee_form(request.POST)
        if form.is_valid():
            try:
                result = form.save(user=request.user.username)
            except NAError as e:
                # error kalau user salah input, ada form yang tidak di isi
                result = NAErrorHandler.handle(err=e)
        else:
            result = NAErrorHandler.handle_form_error(form_error=form.errors)
        return commonFunct.response_default(result)
    elif request.method == 'GET':
        idapp = request.GET['idapp']
        mode = request.GET['mode']
        employee = Employee()
        if mode == 'Edit' or mode == 'Open':
            try:
                result = Employee.objects.get(idapp=idapp)
            except employee.DoesNotExist:
                result = NAErrorHandler.handle_data_lost(
                    model=Employee, pk=idapp)
                return commonFunct.response_default(result)
            else:
                form = NA_Employee_form(initial=forms.model_to_dict(result))
                form.fields['nik'].widget.attrs['disabled'] = 'disabled'
        else:
            form = NA_Employee_form()
            del form.fields['inactive']
        return render(request, 'app/MasterData/NA_Entry_Employee.html', {'form': form})


@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
    cols = []
    cols.append({'name': 'nik', 'value': 'nik', 'selected': '',
                 'dataType': 'varchar', 'text': 'Nik'})
    cols.append({'name': 'employee_name', 'value': 'employee_name',
                 'selected': 'True', 'dataType': 'varchar', 'text': 'Employee Name'})
    cols.append({'name': 'typeapp', 'value': 'typeapp', 'selected': '',
                 'dataType': 'varchar', 'text': 'type of brand'})
    cols.append({'name': 'jobtype', 'value': 'jobtype',
                 'selected': '', 'dataType': 'varchar', 'text': 'Job type'})
    cols.append({'name': 'gender', 'value': 'gender',
                 'selected': '', 'dataType': 'varchar', 'text': 'Gender'})
    cols.append({'name': 'status', 'value': 'status',
                 'selected': '', 'dataType': 'varchar', 'text': 'Status'})
    cols.append({'name': 'telphp', 'value': 'telphp',
                 'selected': '', 'dataType': 'varchar', 'text': 'Telp/Hp'})
    cols.append({'name': 'territory', 'value': 'territory',
                 'selected': '', 'dataType': 'varchar', 'text': 'Territory'})
    cols.append({'name': 'descriptions', 'value': 'descriptions',
                 'selected': '', 'dataType': 'varchar', 'text': 'Descriptions'})
    cols.append({'name': 'inactive', 'value': 'inactive',
                 'selected': '', 'dataType': 'boolean', 'text': 'InActive'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols})


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('POST')
@decorators.read_permission(form_name=Employee.FORM_NAME_ORI, action='Delete')
def NA_Employee_delete(request):
    idapp = request.POST.get('idapp')
    try:
        employee = Employee.objects.get(idapp=idapp)
    except employee.DoesNotExist:
        result = NAErrorHandler.handle_data_lost(
            pk=idapp,
            model=Employee
        )
    else:
        if Employee.objects.hasRef(idapp=idapp):
            message = Message.HasRef_del.value
            return commonFunct.response_default((Data.HasRef, message))
        with transaction.atomic():
            log = LogActivity(
                models=Employee,
                activity=LogActivity.DELETED,
                user=request.user.username,
                data=employee
            )
            log.record_activity()
            employee.delete()
            result = Data.Success,
    return commonFunct.response_default(result)


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('GET')
def SearchEmployeebyform(request):
    """
    for common search employee by form
    """
    searchText = request.GET.get('employee_filter')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    NAData = Employee.objects.getEmloyeebyForm(searchText)

    # if data is empty.. don't use Paginator and looping, to improve performance
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
            "id": row['idapp'], "cell": [
                row['idapp'], i, row['nik'], row['employee_name']
            ]
        }
        rows.append(datarow)
    results = {"page": page, "total": paginator.num_pages,
               "records": totalRecord, "rows": rows}
    return HttpResponse(
        json.dumps(results, indent=4, cls=DjangoJSONEncoder),
        content_type='application/json'
    )
