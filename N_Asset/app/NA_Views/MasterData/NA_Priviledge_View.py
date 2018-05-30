from django.http import HttpResponse
from NA_Models.models import NAPriviledge, NASysPriviledge,NAPriviledge_form
from NA_DataLayer.common import ResolveCriteria
from django.core.paginator import Paginator
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.db import transaction

def NA_Priviledge(request):
    return render(request,'app/MasterData/NA_F_Priviledge.html')

def NA_PriviledgeGetData(request):
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
        priviledgeData = NAPriviledge.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType).order_by('-' + str(Isidx))
    else:
        priviledgeData = NAPriviledge.objects.PopulateQuery(IcolumnName,IvalueKey,criteria,dataType)

    totalRecord = priviledgeData.count()
    paginator = Paginator(priviledgeData, int(Ilimit))
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
        datarow = {"id" :row['idapp'], "cell" :[i,row['idapp'],row['username'],row['email'],row['password'],row['last_login'],row['last_form'], \
		    row['is_active'],row['date_joined'],row['createdby']]}
        rows.append(datarow)
    results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

def NA_Priviledge_sys(request):
    user_id = request.GET['user_id']
    data = NAPriviledge.objects.Get_Priviledge_Sys(user_id)
    same_data = {}
    len_data = len(data)
    for index,j in enumerate(data):
        if (index + 1) < len_data:
            if j['form_name'] == data[index+1]['form_name']:
                if j['form_name'] in same_data:
                    same_data[j['form_name']] += 1
                else:
                    same_data[j['form_name']] = 2
    for index,i in enumerate(data):
        if i['form_name'] in same_data:
            i['attr'] = {}
            i['attr']['form_name'] = {}
            if index > 0:
                if 'attr' in data[index-1]:
                    if i['form_name'] != data[index-1]['form_name']:
                        if data[index+1]['form_name'] == i['form_name']:
                            i['attr']['form_name']['rowspan'] = same_data[i['form_name']]
                    else:
                        i['attr']['form_name']['display'] = "none"
                else:
                    i['attr']['form_name']['rowspan'] = same_data[i['form_name']]
            else:
                i['attr']['form_name']['rowspan'] = same_data[i['form_name']]
    return HttpResponse(json.dumps(data,cls=DjangoJSONEncoder),content_type='application/json')

def Entry_Priviledge(request):
    if request.method == 'POST':
        form = NA_Priviledge_Form(request.POST)
        if form.is_valid():
            form.save()
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
        else:
            form = NA_Priviledge_Form()
        return render(request,'app/MasterData/NA_Entry_Priviledge.html',{'form':form})


class NA_Priviledge_Form(forms.Form):
    first_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'First Name','style':'height:unset'}))
    last_name = forms.CharField(max_length=30,required=False,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Last Name','style':'height:unset'}))
    username = forms.CharField(max_length=30,required=True,widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'User Name','style':'height:unset'}))
    email = forms.CharField(max_length=30,required=True,widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Email'}))
    divisi = forms.ChoiceField(widget=forms.Select(
        attrs={'class':'form-control'}),choices=(
        ('IT','IT'),
        ('GA','GA')
        ))
    password = forms.CharField(max_length=30,required=True,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password','style':'height:unset'}))
    confirm_password = forms.CharField(max_length=30,required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Confirm Password','style':'height:unset'}))
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

    def save(self):
        with transaction.atomic():
            user = NAPriviledge()
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.username = self.username
            user.email = self.email
            user.divisi = self.divisi
            user.set_password(self.password)
            user.save()
            fk_form = NAPriviledge_form.get_form_IT()
            data = []
            for i in fk_form:
                priviledge_form = NAPriviledge_form.objects.get(idapp=i)
                data.append({
                    'fk_p_form':priviledge_form,
                    'permission':'Allow View',
                    'user_id': user
                })
                data.append({
                    'fk_p_form':priviledge_form,
                    'permission':'Allow Add',
                    'user_id': user
                })
                data.append({
                    'fk_p_form':priviledge_form,
                    'permission':'Allow Edit',
                    'user_id': user
                })
                data.append({
                    'fk_p_form':priviledge_form,
                    'permission':'Allow Delete',
                    'user_id': user
                })
            sys_priviledge = NASysPriviledge.objects.bulk_create([
                NASysPriviledge(**q) for q in data
            ])
        return user