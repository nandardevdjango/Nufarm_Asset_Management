from django import forms
from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import View

from NA_DataLayer.common import decorators
from NA_Models.models import NAGaOutwards


class NAGaVnHistoryForm(forms.Form):
    idapp = forms.IntegerField(widget=forms.HiddenInput())
    reg_no = forms.CharField(widget=forms.TextInput())
    expired_reg = forms.CharField(widget=forms.TextInput())


@method_decorator(decorators.ensure_authorization, name='dispatch')
@method_decorator(decorators.ajax_required, name='dispatch')
class NAGaVnHistoryView(View):

    def get(self, request):
        q = request.GET.get('q')

        only_fields = [
            'idapp',
            'fk_app__reg_no',
            'fk_app__expired_reg',
            'fk_employee__employee_name',
            'fk_employee__telphp',
            'fk_employee__inactive',
            'fk_goods__goodsname',
            'fk_receive__brand',
            'fk_receive__typeapp',
            'fk_receive__colour',
            'fk_receive__invoice_no'
        ]

        regs = (NAGaOutwards.objects.filter(fk_app__is_active=True)
                .select_related('fk_app', 'fk_employee', 'fk_goods', 'fk_receive')
                .only(*only_fields))

        if q:
            filter_fields = only_fields.copy()
            for field in ['idapp', 'fk_employee__inactive', 'fk_app__expired_reg']:
                filter_fields.remove(field)
            filter_kwargs = Q(**{filter_fields.pop(0): q})
            for field in filter_fields:
                filter_kwargs = filter_kwargs | Q(**{field: q})
            regs = regs.filter(filter_kwargs)
        regs = list(regs)

        result = []
        if regs:
            no = 0
            for reg in regs:
                no += 1
                result.append({
                    'no': no,
                    'idapp': reg.fk_app_id,
                    'reg_number': reg.fk_app.reg_no,
                    'is_expire': reg.fk_app.is_expired_reg,
                    'expire_date': reg.fk_app.expired_reg,
                    'idapp_outwards': reg.idapp,
                    'employee_name': reg.fk_employee.employee_name,
                    'mobile_phone': reg.fk_employee.telphp,
                    'inactive': reg.fk_employee.inactive,

                    'goods_name': reg.fk_goods.goodsname,
                    'brand': reg.fk_receive.brand,
                    'type': reg.fk_receive.typeapp,
                    'colour': reg.fk_receive.colour,
                    'invoice_no': reg.fk_receive.invoice_no
                })
        return JsonResponse(result, safe=False)

    def post(self, request):
        form = NAGaVnHistoryForm(request.POST)
        if form.is_valid():
            pass
