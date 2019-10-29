import json
from datetime import datetime

from django import forms
from django.contrib.auth import login, logout, authenticate
from django.core import signing
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import resolve, Resolver404
from django.db import transaction, IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from NA_DataLayer.common import ResolveCriteria, Data, commonFunct, decorators
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from NA_DataLayer.logging import LogActivity
from NA_Models.models import NAPrivilege, NASysPrivilege, NAPrivilege_Form
from NA_Worker.task import NATask
from NA_Worker.worker import NATaskWorker


@decorators.ensure_authorization
def NA_Privilege(request):
    return render(request, 'app/MasterData/NA_F_Privilege.html')


def NA_PrivilegeGetData(request):
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
        privilegeData = NAPrivilege.objects.PopulateQuery(
            IcolumnName, IvalueKey, criteria, dataType).order_by('-' + str(Isidx))
    else:
        privilegeData = NAPrivilege.objects.PopulateQuery(
            IcolumnName, IvalueKey, criteria, dataType)

    totalRecord = privilegeData.count()
    paginator = Paginator(privilegeData, int(Ilimit))
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
                i, row['idapp'], row['first_name'], row['last_name'], row['username'],
                row['email'], row['divisi'], row['role'], row['password'], row['last_login'], row['last_form'],
                row['is_active'], row['date_joined'], row['createdby']
            ]
        }
        rows.append(datarow)
    results = {"page": page, "total": paginator.num_pages,
               "records": totalRecord, "rows": rows}
    return HttpResponse(json.dumps(results, indent=4, cls=DjangoJSONEncoder), content_type='application/json')


@decorators.ajax_required
@decorators.detail_request_method('GET')
def ShowCustomFilter(request):
    cols = []
    cols.append({'name': 'first_name', 'value': 'first_name',
                 'selected': 'True', 'dataType': 'varchar', 'text': 'First Name'})
    cols.append({'name': 'last_name', 'value': 'last_name',
                 'selected': '', 'dataType': 'varchar', 'text': 'Last Name'})
    cols.append({'name': 'username', 'value': 'username',
                 'selected': '', 'dataType': 'varchar', 'text': 'User Name'})
    cols.append({'name': 'email', 'value': 'email', 'selected': '',
                 'dataType': 'varchar', 'text': 'Email'})
    cols.append({'name': 'divisi', 'value': 'divisi',
                 'selected': '', 'dataType': 'varchar', 'text': 'Divisi'})
    cols.append({'name': 'last_form', 'value': 'last_form',
                 'selected': '', 'dataType': 'varchar', 'text': 'Last Form'})
    cols.append({'name': 'inactive', 'value': 'inactive',
                 'selected': '', 'dataType': 'boolean', 'text': 'InActive'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols})


def na_privilege_permissions(request):
    user_id = request.GET['user_id']
    data = NAPrivilege.objects.Get_Privilege_Sys(user_id)
    totalRecords = len(data)
    page = request.GET.get('page', '1')
    limit_row = request.GET.get('rows', '10')
    paginator = Paginator(data, int(limit_row))
    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
    data = page.object_list
    same_data = {}
    len_data = len(data)
    for index, j in enumerate(data):
        if (index + 1) < len_data:
            if j['form_name'] == data[index + 1]['form_name']:
                if j['form_name'] in same_data:
                    same_data[j['form_name']] += 1
                else:
                    same_data[j['form_name']] = 2
    for index, i in enumerate(data):
        if i['form_name'] in same_data:
            i['attr'] = {}
            i['attr']['form_name'] = {}
            if index > 0:
                if 'attr' in data[index - 1]:
                    if i['form_name'] != data[index - 1]['form_name']:
                        if data[index + 1]['form_name'] == i['form_name']:
                            i['attr']['form_name']['rowspan'] = same_data[i['form_name']]
                    else:
                        i['attr']['form_name']['display'] = "none"
                else:
                    i['attr']['form_name']['rowspan'] = same_data[i['form_name']]
            else:
                i['attr']['form_name']['rowspan'] = same_data[i['form_name']]

    return HttpResponse(
        json.dumps(
            {"page": page.number, "total": paginator.num_pages,
                "records": totalRecords, "rows": data},
            cls=DjangoJSONEncoder
        ),
        content_type='application/json'
    )


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.read_permission(form_name=NAPrivilege.FORM_NAME_ORI)
def Entry_Privilege(request):
    if request.method == 'POST':
        form = NAPrivilegeForm(request.POST)
        if form.is_valid():
            try:
                result = form.save(user=request.user.username)
            except NAError as e:
                result = NAErrorHandler.handle(err=e)
        else:
            result = NAErrorHandler.handle_form_error(form_error=form.errors)
        return commonFunct.response_default(result)
    elif request.method == 'GET':
        statusForm = request.GET['statusForm']
        if statusForm == 'Edit' or statusForm == 'Open':
            idapp = request.GET['idapp']
            data = NAPrivilege.objects.retrieveData(idapp)
            form = NAPrivilegeForm(initial=data)
            if int(data['role']) == NAPrivilege.GUEST:
                form.fields['divisi'].widget.attrs['disabled'] = ''
        else:
            form = NAPrivilegeForm()
            form.fields['password'].widget.attrs['required'] = ''
            form.fields['confirm_password'].widget.attrs['required'] = ''
            form.fields['divisi'].widget.attrs['disabled'] = ''
        return render(request, 'app/MasterData/NA_Entry_Privilege.html', {'form': form})


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('POST')
@decorators.read_permission(form_name=NAPrivilege.FORM_NAME_ORI)
def Delete_user(request):
    idapp = request.POST['idapp']
    try:
        user = NAPrivilege.objects.get(idapp=idapp)
    except NAPrivilege.DoesNotExist:
        result = NAErrorHandler.handle_data_lost(
            pk=idapp, model=NAPrivilege
        )
    else:
        with transaction.atomic():
            log = LogActivity(
                models=NAPrivilege,
                activity=LogActivity.DELETED,
                user=request.user.username,
                data=user
            )
            log.record_activity()
            user.delete()
            result = Data.Success,
    return commonFunct.response_default(result)


@decorators.ajax_required
@decorators.detail_request_method('POST')
def change_role(request, email):
    try:
        user = NAPrivilege.objects.get(email=email)
        result = Data.Success,
    except NAPrivilege.DoesNotExist:
        result = NAErrorHandler.handle_data_lost(
            model=NAPrivilege,
            email=email
        )
    else:
        role = request.POST['role']
        divisi = request.POST['divisi']
        user.role = role
        user.divisi = divisi
        user.save()
    return commonFunct.response_default(result)


class NAPrivilegeForm(forms.Form):
    idapp = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name', 'style': 'height:unset'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name', 'style': 'height:unset'}))
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'User Name', 'style': 'height:unset'}))
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    divisi = forms.ChoiceField(
        required=False,
        choices=(
            ('', '-----------'),
            ('IT', 'IT'),
            ('GA', 'GA')
        ),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )

    )
    role = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}), choices=NAPrivilege.ROLE_CHOICES)
    statusForm = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'display:none'}), required=True)
    password = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'height:unset'}))
    confirm_password = forms.CharField(max_length=30, required=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password',
            'style': 'height:unset'
        }
    ))
    initializeForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    def clean_password(self):
        if self.cleaned_data['statusForm'] == 'Add':
            password = self.cleaned_data.get('password')
            if password is None or password == '':
                raise forms.ValidationError({'password': 'This field is required'})

    def clean_confirm_password(self):
        if self.cleaned_data['statusForm'] == 'Add':
            confirm_password = self.cleaned_data.get('confirm_password')
            if confirm_password is None or confirm_password == '':
                raise forms.ValidationError(
                    {'confirm_password': 'This field is required'}
                )

    def clean(self):
        statusForm = self.cleaned_data['statusForm']
        role = self.cleaned_data['role']
        if isinstance(role, str):
            role = int(role)

        divisi = self.cleaned_data.get('divisi')
        if role == NAPrivilege.GUEST:
            if divisi:
                raise forms.ValidationError({
                    'divisi': 'Can\'t set divisi to user guest.'
                })
        else:

            if not divisi:
                raise forms.ValidationError({
                    'divisi': 'This field is required'
                })
        if statusForm == 'Edit':
            idapp = self.cleaned_data.get('idapp')
            if not idapp:
                raise forms.ValidationError({
                    'idapp': 'This field is required'
                })
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password didn\'t match with confirm password'
            )
        return super(NAPrivilegeForm, self).clean()

    @transaction.atomic
    def save(self, user):
        status_form = self.cleaned_data.get('statusForm')
        must_set_perms = False
        password = self.cleaned_data.get('password')
        if status_form == 'Add':
            user_ = NAPrivilege()
            user_.set_password(password)
            user_.date_joined = datetime.now()
            user_.createdby = user
            must_set_perms = True
            activity = LogActivity.CREATED
        elif status_form == 'Edit':
            try:
                user_ = NAPrivilege.objects.get(
                    idapp=self.cleaned_data.get('idapp')
                )
            except NAPrivilege.DoesNotExist:
                raise NAError(
                    error_code=NAErrorConstant.DATA_LOST
                )
            else:
                if (user_.role == NAPrivilege.GUEST and
                        self.cleaned_data.get('role') != NAPrivilege.GUEST):
                    must_set_perms = True
                if password:
                    user_.set_password(password)
            activity = LogActivity.UPDATED

        user_.first_name = self.cleaned_data['first_name']
        user_.last_name = self.cleaned_data['last_name']
        user_.username = self.cleaned_data['username']
        user_.email = self.cleaned_data['email']
        user_.role = self.cleaned_data['role']
        if user_.role != NAPrivilege.GUEST:
            user_.divisi = self.cleaned_data['divisi']

        try:
            user_.save()
        except IntegrityError as e:
            raise NAError(
                error_code=NAErrorConstant.DATA_EXISTS,
                message=e,
                instance=user_
            )
        else:
            log = LogActivity(
                models=NAPrivilege,
                activity=activity,
                user=user,  # user's who created this data
                data=user_  # instance
            )
            log.record_activity()
        if must_set_perms:
            NASysPrivilege.set_permission(user_)

        if password:
            worker = NATaskWorker(
                func=NATask.task_email_password_user,
                args=[user_.email, password]
            )
            worker.run()

        return Data.Success,


@decorators.admin_required_action('change')
@decorators.ajax_required
@decorators.detail_request_method('POST')
def na_privilege_inactive_permission(request, idapp):
    inactive = request.POST['inactive']
    result = NASysPrivilege.objects.setInActive(idapp, inactive)
    return commonFunct.response_default(result)


@decorators.admin_required_action('delete')
@decorators.ajax_required
@decorators.detail_request_method('POST')
def na_privilege_delete_permission(request, idapp):
    result = NASysPrivilege.objects.Delete(idapp)
    return commonFunct.response_default(result)


@decorators.admin_required_action('add')
@decorators.ajax_required
def na_privilege_add_permission(request, email):
    if request.method == 'POST':
        form = NA_Permission_Form(request.POST)
        if form.is_valid():
            result = form.save(request)
            if isinstance(result, HttpResponse):
                return result
            return commonFunct.response_default(result)
        raise forms.ValidationError(form.errors)
    elif request.method == 'GET':
        form = NA_Permission_Form()
        return render(request, 'app/MasterData/NA_Entry_Permission.html', {'form': form})


def na_privilege_check_permission(request, user_id):
    fk_form = request.GET['fk_form']
    data = NASysPrivilege.objects.CheckPermission(fk_form, user_id)
    if data == Data.Empty:
        return HttpResponse(
            json.dumps(commonFunct.EmptyGrid()),
            content_type='application/json'
        )
    dataRow = []
    no = 0
    for row in data:
        no += 1
        dataRow.append({
            'idapp': row['idapp'],
            'no': no,
            'form_name': row['form_name'],
            'permission': row['permission'],
            'set': '1',
            # 'inactive': row['inactive'],
        })
    return HttpResponse(
        json.dumps(dataRow),
        content_type='application/json'
    )


def na_privilege_get_permission(request, email):
    form_name_ori = request.GET['form_name']
    user = NAPrivilege.objects.get(email=email)
    return commonFunct.response_default(
        (Data.Success, user.get_permission(form_name_ori))
    )


def na_privilege_set_default_permission(request, email):
    user = NAPrivilege.objects.get(email=email)
    if int(user.role) != NAPrivilege.GUEST:
        NASysPrivilege.set_permission(user)
        return commonFunct.response_default((Data.Success,))


class NA_Permission_Form(forms.Form):
    fk_form = forms.ModelChoiceField(
        queryset=NAPrivilege_Form.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'display:inline-block'})
    )
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    allow_view = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'style': 'display:none'}), required=False)
    allow_add = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'style': 'display:none'}), required=False)
    allow_edit = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'style': 'display:none'}), required=False)
    allow_delete = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'style': 'display:none'}), required=False)
    initialize_permissionForm = forms.CharField(
        widget=forms.HiddenInput(), required=False)

    def save(self, request):
        user_id = self.cleaned_data['user_id']
        # instance of NA_Privilege_form
        fk_form = self.cleaned_data['fk_form']
        allow_view = self.cleaned_data['allow_view']
        allow_add = self.cleaned_data['allow_add']
        allow_edit = self.cleaned_data['allow_edit']
        allow_delete = self.cleaned_data['allow_delete']
        permissions = {
            'Allow View': allow_view,
            'Allow Add': allow_add,
            'Allow Edit': allow_edit,
            'Allow Delete': allow_delete
        }
        user = NAPrivilege.objects.get(idapp=user_id)
        if user.role == NAPrivilege.GUEST:
            if allow_add or allow_edit or allow_delete:
                message = '__cannot_add_other_permission_guest'
                return HttpResponse(
                    json.dumps({'message': message}),
                    status=403,
                    content_type='application/json'
                )

            permissions.pop('Allow Add')
            permissions.pop('Allow Edit')
            permissions.pop('Allow Delete')

        data_permissions = []
        for k, v in permissions.items():
            if v:
                data_permissions.append(k)

        if user.is_have_permission(fk_form.form_name_ori):
            users_permission = user.get_permission(fk_form.form_name_ori)
            for i in users_permission:
                if i['permission'] in data_permissions:
                    data_permissions.pop(
                        data_permissions.index(i['permission']))

        NASysPrivilege.set_custom_permission(
            user_id=user_id,
            fk_form=fk_form.idapp,
            permissions=data_permissions,
            createdby=request.user.username
        )
        return (Data.Success,)


def na_privilege_login(request):
    if request.user.is_authenticated():
        return redirect(request.GET.get('next', '/'))
    else:
        title = "Login"
        cookie_data = {
            'is_ever_sign': True
        }
        cookie_key = '__na_cookie'
        if request.method == 'POST':
            form = NAPrivilegeLoginForm(request.POST or None)
            if form.is_valid():
                form.login(request)
                try:
                    next_action = request.META.get('HTTP_REFERER').split('?')[1]
                    next_action = next_action.replace('next=', '')
                except IndexError:
                    next_action = '/'
                else:
                    try:
                        resolve(next_action)
                    except Resolver404:
                        next_action = '/'
                response = JsonResponse({'redirect': next_action})
                cookie_data.update({
                    'role': int(request.user.role)
                })
                cookie_value = signing.dumps(cookie_data)  # Cryptographic: for security
                response.set_cookie(key=cookie_key, value=cookie_value)
                return response
            else:
                _, result = NAErrorHandler.handle_form_error(
                    form_error=form.errors,
                    as_dict=True
                )
                return JsonResponse(result, status=400)

        form = NA_Permission_Form()
        template_name = "app/NA_User/login.html"
        if request.COOKIES.get(cookie_key):
            cookie_data = signing.loads(request.COOKIES.get(cookie_key))
            if int(cookie_data.get('role')) in [NAPrivilege.SUPER_USER, NAPrivilege.USER]:
                template_name = "app/layout.html"
        return render(
            request,
            template_name,
            {"form": form, "title": title}
        )


class NAPrivilegeLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = NAPrivilege.objects.get(email=email)
            except NAPrivilege.DoesNotExist:
                raise forms.ValidationError({
                    'email': 'Email does not exist'
                })
            else:
                if not user.check_password(password):
                    raise forms.ValidationError({
                        'password': 'Password incorrect'
                    })

        return super(NAPrivilegeLoginForm, self).clean(*args, **kwargs)

    def login(self, request):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # authenticates Email & Password
        user = authenticate(email=email, password=password)
        login(request, user)


def na_privilege_register(request):
    if request.method == 'POST':
        form = NAPrivilegeRegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                user = form.save()
            except NAError as e:
                error_column = NAErrorHandler.retrieve_integrity_column(err=e)
                error_field = NAErrorHandler.retrieve_integrity_field(
                    column=error_column,
                    model=NAPrivilege
                )
                message = {
                    error_field: (
                        '%s already exists' % NAPrivilege.HUMAN_DISPLAY.get(error_field)
                    )
                }
                return JsonResponse(message, status=400)
            login(request, user, backend='NA_DataLayer.NA_Auth.NA_AuthBackend')
            return redirect('home')
        else:
            _, err = NAErrorHandler.handle_form_error(form_error=form.errors, as_dict=True)
            return JsonResponse(err, status=400)
    else:
        form = NAPrivilegeRegisterForm()
        template_name = 'app/NA_User/register.html'
        if False:
            template_name = 'app/MasterData/na_privilege_register.html'
        return render(
            request,
            template_name,
            {'form': form}
        )


def NA_Privilege_logout(request):
    logout(request)
    return redirect('login')


class NAPrivilegeRegisterForm(forms.Form):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Last Name'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Enter Username'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Email Address'}))
    picture = forms.ImageField(required=False)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm Password'}))
    initializeForm_user = forms.CharField(
        required=False, widget=forms.HiddenInput())

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError({
                'password2': 'Password doesn\'t match'
            })
        return super(NAPrivilegeRegisterForm, self).clean()

    @transaction.atomic
    def save(self):
        user = NAPrivilege()
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        pict = self.cleaned_data.get('picture')
        if pict:
            user.picture = pict
        user.set_password(self.cleaned_data['password1'])
        try:
            user.save()
        except IntegrityError as e:
            raise NAError(
                error_code=NAErrorConstant.DATA_EXISTS,
                message=e,
                instance=user
            )
        NASysPrivilege.set_permission(user)
        return user


def NA_Privilege_change_picture(request, email):
    if request.user.email != email:
        return commonFunct.permision_denied('<h1>403 Forbidden</h1>')
    user = request.user
    picture = request.FILES['picture']
    user.picture = picture
    user.save()
    return commonFunct.response_default((Data.Success, user.get_picture_name()))



class EditProfileForm(forms.Form):
    idapp = forms.IntegerField(widget=forms.HiddenInput())
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ), required=False)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ), required=False)
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ), disabled=True, required=False)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ), disabled=True, required=False)
    divisi = forms.ChoiceField(choices=(
        ('IT', 'IT'),
        ('GA', 'GA')
    ),
    widget=forms.Select(attrs={
        'class': 'form-control'
    }), required=False
    )
    role = forms.ChoiceField(widget=forms.Select(
        attrs={'class': 'form-control'}),
        choices=NAPrivilege.ROLE_CHOICES,
        disabled=True,
        required=False
    )
    picture = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ), required=False)
    
    def save(self):
        fields = [
            'first_name', 'last_name', 'divisi', 'picture',
            'password'
        ]
        idapp = self.cleaned_data.get('idapp')
        user = NAPrivilege.objects.get(idapp=idapp)
        change = False
        for field in fields:
            value = self.cleaned_data.get(field)
            if value and value != getattr(user, field):
                change = True
                setattr(user, field, value)
        if change:
            user.save()
        return user

@decorators.ensure_authorization
@decorators.ajax_required
def edit_profile(request: HttpRequest):
    if request.method == "GET":
        init_data = forms.model_to_dict(instance=request.user)
        form = EditProfileForm(initial=init_data)
        return render(
            request,
            'app/NA_User/NA_User_Profile.html',
            {
                'form': form
            }
        )
    else:
        data = request.POST.copy()
        data.update({
            'idapp': request.user.idapp
        })
        form = EditProfileForm(data, request.FILES or None)
        if form.is_valid():
            form.save()
            return commonFunct.response_default((Data.Success,))
