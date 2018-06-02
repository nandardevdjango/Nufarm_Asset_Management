from django.http import HttpResponse
from NA_Models.models import NAPriviledge, NASysPriviledge,NAPriviledge_form
from NA_DataLayer.common import ResolveCriteria, Data, commonFunct, decorators
from django.core.paginator import Paginator, EmptyPage, InvalidPage
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
        datarow = {
            "id" :row['idapp'], "cell" :[
                i,row['idapp'],row['first_name'],row['last_name'],row['username'],
                row['email'],row['password'],row['divisi'],row['last_login'],row['last_form'],
                row['is_active'],row['date_joined'],row['createdby']
                ]
            }
        rows.append(datarow)
    results = {"page": page,"total": paginator.num_pages ,"records": totalRecord,"rows": rows }
    return HttpResponse(json.dumps(results, indent=4,cls=DjangoJSONEncoder),content_type='application/json')

@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
	cols = []
	cols.append({'name':'first_name','value':'first_name','selected':'True','dataType':'varchar','text':'First Name'})
	cols.append({'name':'last_name','value':'last_name','selected':'','dataType':'varchar','text':'Last Name'})
	cols.append({'name':'username','value':'username','selected':'','dataType':'varchar','text':'User Name'})
	cols.append({'name':'email','value':'email','selected':'','dataType':'varchar','text':'Email'})
	cols.append({'name':'divisi','value':'divisi','selected':'','dataType':'varchar','text':'Divisi'})
	cols.append({'name':'last_form','value':'last_form','selected':'','dataType':'varchar','text':'Last Form'})
	cols.append({'name':'inactive','value':'inactive','selected':'','dataType':'boolean','text':'InActive'})
	return render(request, 'app/UserControl/customFilter.html', {'cols': cols})

def NA_Priviledge_sys(request):
    user_id = request.GET['user_id']
    data = NAPriviledge.objects.Get_Priviledge_Sys(user_id)
    totalRecords = len(data)
    page = request.GET.get('page','1')
    limit_row = request.GET.get('rows','10')
    paginator = Paginator(data,int(limit_row))
    data = paginator.page(page).object_list
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
    
    return HttpResponse(
        json.dumps({"page": page,"total": paginator.num_pages ,"records": totalRecords,"rows": data },cls=DjangoJSONEncoder),
        content_type='application/json'
    )

def Entry_Priviledge(request):
    if request.method == 'POST':
        form = NA_Priviledge_Form(request.POST)
        if form.is_valid():
            result = form.save()
            return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data = NAPriviledge.objects.retrieveData(idapp)
            form = NA_Priviledge_Form(initial=data)
        else:
            form = NA_Priviledge_Form()
            form.fields['password'].widget.attrs['required'] = ''
            form.fields['confirm_password'].widget.attrs['required'] = ''
        return render(request,'app/MasterData/NA_Entry_Priviledge.html',{'form':form})

def Delete_user(request):
    idapp = request.POST['idapp']
    result = NAPriviledge.objects.Delete(idapp)
    return commonFunct.response_default(result)


class NA_Priviledge_Form(forms.Form):
    idapp = forms.IntegerField(widget=forms.HiddenInput())
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
        ('Guest','Guest'),
        ('IT','IT'),
        ('GA','GA')
        ))
    statusForm = forms.CharField(widget=forms.TextInput(
        attrs={'style':'display:none'}),required=True)
    password = forms.CharField(max_length=30,required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Password','style':'height:unset'}))
    confirm_password = forms.CharField(max_length=30,required=False,widget=forms.PasswordInput(
        attrs={'class':'form-control','placeholder':'Confirm Password','style':'height:unset'}))
    initializeForm = forms.CharField(widget=forms.HiddenInput(),required=False)

    def clean_password(self):
        if self.cleaned_data['statusForm'] == 'Add':
            password = self.cleaned_data.get('password')
            if password is None or password == '':
                raise forms.ValidationError(
                    'Please fill out password'
                )

    def clean_confirm_password(self):
        if self.cleaned_data['statusForm'] == 'Add':
            confirm_password = self.cleaned_data.get('confirm_password')
            if confirm_password is None or confirm_password == '':
                raise forms.ValidationError(
                    'Please fill out confirm password'
                )

    def clean(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password didn\'t match with confirm password'
            )

    def getFormData(self):
        return {
            'first_name':self.cleaned_data.get('first_name'),
            'last_name':self.cleaned_data.get('last_name'),
            'username':self.cleaned_data.get('username'),
            'email':self.cleaned_data.get('email'),
            'divisi':self.cleaned_data.get('divisi')
        }

    def save(self):
        statusForm = self.cleaned_data.get('statusForm')
        if statusForm is None or statusForm == '':
            raise forms.ValidationError(
                'Status Form cannot be null'
            )
        else:
            if statusForm == 'Add':
                with transaction.atomic():
                    user = NAPriviledge()
                    user.first_name = self.cleaned_data['first_name']
                    user.last_name = self.cleaned_data['last_name']
                    user.username = self.cleaned_data['username']
                    user.email = self.cleaned_data['email']
                    user.divisi = self.cleaned_data['divisi']
                    user.set_password(self.cleaned_data['password'])
                    user.save()
                    if user.divisi != NAPriviledge.Guest:
                        NASysPriviledge.set_permission(user)

            elif statusForm == 'Edit':
                idapp = self.cleaned_data.get('idapp')
                data = NAPriviledge.objects.values('first_name','last_name','username','email','divisi')\
                    .filter(idapp=idapp)
                if data.exists():
                    data = data[0]
                    data_init = {
                        'first_name': data['first_name'],
                        'last_name': data['last_name'],
                        'username':data['username'],
                        'email': data['email'],
                        'divisi':data['divisi']
                    }
                    data_form = self.getFormData()
                    sames = [k for k in data_form if data_form[k] == data_init[k]]
                    for same in sames:
                        data_form.pop(same)
                    print(data_form)
                    NAPriviledge.objects.filter(idapp=idapp).update(**data_form)
        return (Data.Success,)

@decorators.admin_required_action('change')
@decorators.ajax_required
@decorators.detail_request_method('POST')
def NA_Sys_Priviledge_setInactive(request,idapp):
    inactive = request.POST['inactive']
    result = NASysPriviledge.objects.setInActive(idapp)
    return commonFunct.response_default(result)

@decorators.admin_required_action('delete')
@decorators.ajax_required
@decorators.detail_request_method('POST')
def NA_Sys_Priviledge_delete(request,idapp):
    result = NASysPriviledge.objects.filter(idapp=idapp)
    return commonFunct.response_default(result)


def NA_Priviledge_login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next'))
    else:
        title = "Login"
        form = NA_Priviledge_Login_Form(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=email, password=password) 
            login(request, user)
            next_action = request.GET.get('next')
            if next_action is not None:
                return redirect(next_action)
            else:
                return redirect('home')
        else:
            raise forms.ValidationError(form.errors)

        return render(
            request, 
            "app/layout.html", 
            {"form":form,"title":title}
        )

class NA_Priviledge_Login_Form(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("User Does Not Exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)