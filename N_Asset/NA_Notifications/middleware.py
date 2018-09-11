from datetime import date, datetime, timedelta

from NA_Models.models import NAPrivilege

TEMPLATE_URL = [
    'home',
    'NA_Employee',
    'GoodMaster',
    'NA_Privilege',
    'NA_Supplier',
    'NA_Acc',
    'NA_Maintenance',
    'GoodsDisposal',
    'GoodsLending',
    'NA_GoodsLost',
    'GoodsOutwards',
    'GoodsReceive',
    'NA_Goods_Receive_other',
    'GoodsReturn'
]


class NotificationMiddleware(object):

    def process_response(self, request, response):
        if (request.user.is_authenticated()
                and request.user.divisi == NAPrivilege.GA
                and request.user.role == NAPrivilege.SUPER_USER):

            is_template_url = (hasattr(request.resolver_match, 'url_name')  # handle
                               # attribute error
                               and request.resolver_match.url_name in TEMPLATE_URL)

            if (request.session.get('ga_reg_notif') is None
                    and is_template_url):
                # set session only one time
                self._check_notifications(request=request)
            else:
                notif_expired = request.session.get('ga_notif_expired')
                if is_template_url and notif_expired:
                    notif_expired = datetime.strptime(notif_expired, '%d/%m/%Y').date()
                    if notif_expired <= date.today():
                        del request.session['ga_reg_notif']
                        self._check_notifications(request=request)

        return response

    def _check_notifications(self, request):
        from .models import NANotifications

        notifications = NANotifications.objects.filter(
            is_active=True,
            name='ga_reg_notif'
        )
        if notifications.exists():
            request.session['ga_reg_notif'] = True
        else:
            request.session['ga_reg_notif'] = False
        request.session['ga_notif_expired'] = (
                date.today() + timedelta(days=1)
        ).strftime('%d/%m/%Y')
