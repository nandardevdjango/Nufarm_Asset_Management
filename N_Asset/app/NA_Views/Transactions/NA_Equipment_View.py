from datetime import datetime

from django import forms
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core.serializers import serialize

from NA_Models.models import NAGoodsEquipment
from NA_DataLayer.common import Data, decorators, commonFunct


class NAEquipmentForm(forms.Form):
    name_app = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'NA-Form-Control',
            'style': 'display:inline-block;width:215px;',
            'placeholder': 'equipment name'
        }
    ))

    def clean(self):
        name_app = self.cleaned_data.get('name_app')
        if name_app:
            if NAGoodsEquipment.objects.filter(name_app__iexact=name_app).exists():
                self.add_error('name_app', Data.Exists.value)
        return super(NAEquipmentForm, self).clean()

    def save(self, request):
        equipment = NAGoodsEquipment()
        equipment.name_app = self.cleaned_data.get('name_app')
        equipment.type_app = NAGoodsEquipment.get_type_app(request)
        equipment.createdby = request.user.username
        equipment.createddate = datetime.now()
        equipment.save()
        return Data.Success, forms.model_to_dict(equipment, fields=['idapp', 'name_app'])


class NAEquipmentView(View):

    def get(self, request):
        form = NAEquipmentForm()
        return render(request, 'app/Transactions/NA_Entry_Equipment.html', {'form': form})

    def post(self, request):
        form = NAEquipmentForm(request.POST)
        if form.is_valid():
            result = form.save(request=request)
            return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)


@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('GET')
def equipment_list(request):
    return JsonResponse(
        commonFunct.serialize_queryset(
            NAGoodsEquipment.get_equipment(request).values('idapp', 'name_app')
        ),
        safe=False
    )
