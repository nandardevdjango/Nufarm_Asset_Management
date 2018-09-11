from datetime import datetime

from django.http import JsonResponse
from django.views.generic import View

from .models import NANotifications
from NA_DataLayer.common import Message, decorators


class NANotificationView(View):

    def __init__(self, *args, **kwargs):
        super(NANotificationView, self).__init__(*args, **kwargs)
        self.queryset = NANotifications.objects.filter(
            is_active=True
        )

    def get(self, request):
        name = request.GET.get('name')
        notification_type = request.GET.get('type')
        notifications = self.queryset.filter(
            name=name,
            user=request.user,
            data__is_dismissed=False
        )
        result = []
        if notification_type == 'popup':
            no = 0
            notifications = notifications.values('idapp', 'data')

            for notif in notifications:
                no += 1
                date_expire = notif['data'].get('date_expire')
                date_expire_ = datetime.strptime(date_expire, '%d/%m/%Y')
                time, unit = Message.get_time_info(
                    times=date_expire_,
                    format='day'
                )
                notif_type = 'normal'
                days_left = f'{time} {unit}'
                if notif['data'].get('is_expire'):
                    notif_type = 'danger'
                    days_left = 'has expired'
                elif time <= 3:
                    notif_type = 'warning'
                result.append({
                    'no': no,
                    'notif_id': notif['idapp'],
                    'idapp': notif['data'].get('idapp'),
                    'reg_number': notif['data'].get('reg_number'),
                    'date_expire': date_expire,
                    'day_left': days_left,
                    'notif_type': notif_type,
                    'employee_name': notif['data'].get('employee_name'),
                    'employee_phone': notif['data'].get('employee_phone'),
                    'employee_inactive': notif['data'].get('employee_inactive')
                })

        return JsonResponse(result, safe=False)

@decorators.ensure_authorization
@decorators.ajax_required
@decorators.detail_request_method('POST')
def dismiss_notification(request):
    notif_id = request.POST['notif_id'].split(',')
    notifications = NANotifications.objects.filter(idapp__in=notif_id)
    for notif in notifications:
        notif.data.update({
            'is_dismissed': True
        })
        notif.save()
    return JsonResponse({'success': True})
