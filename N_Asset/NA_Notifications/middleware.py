from datetime import date, timedelta
from django.contrib.sessions.models import Session

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
        if request.user.is_authenticated():
            if (not request.session.get('ga_reg_notif')  # if session doesn't exists
                    and hasattr(request.resolver_match, 'url_name')  # handle attribute error
                    and request.resolver_match.url_name in TEMPLATE_URL):

                # set session only one time
                from .models import NANotifications

                notifications = NANotifications.objects.filter(
                    is_active=True,
                    name='ga_reg_notif'
                )
                if notifications.exists():
                    request.session['ga_reg_notif'] = True
                else:
                    request.session['ga_reg_notif'] = False
                db_session = Session.objects.get(session_key=request.session.session_key)
                db_session.expired_date = date.today() + timedelta(days=1)
                db_session.save()
        return response
