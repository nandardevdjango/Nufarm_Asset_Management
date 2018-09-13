from datetime import datetime
from decimal import Decimal

from celery.schedules import crontab
from celery.task import task, periodic_task
from django.db import transaction

from NA_Models.models import NAGaVnHistory, NAPrivilege
from NA_Notifications.email import EmailNotification, EmailSubject
from NA_Notifications.services.notifications_service import (
    NAPushNotificationService,
    NAUpdateNotificationService
)

class NATask(object):

    @staticmethod
    @task(name='task_email_password_user')
    def task_email_password_user(email, password):
        notification = EmailNotification(
            subject=EmailSubject.USER_PASSWORD,
            body=password
        )
        if not isinstance(email, list):
            email = [email]
        notification.send(to=email)
        return 'Successfully send email notifications to %s' % email

    @staticmethod
    @task(name='task_generate_fix_asset')
    def task_generate_fix_asset(idapp, user):
        from NA_Models.models import NAAccFa
        from app.NA_Views.OtherPages.NA_Acc_Fa_View import generate_acc_value

        data_arr = NAAccFa.objects.searchAcc_ByForm(idapp=idapp)
        for data in data_arr:
            startdate = data['startdate'].strftime('%Y-%m-%d')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            price = data['priceperunit']
            depr_method = data['depreciationmethod']
            economiclife = data['economiclife']
            values_insert = []

            def settings_generate(opt):
                settings = {
                    'month_of': opt['month_of'],
                    'economiclife': economiclife,
                    'typeApp': data['typeapp'],
                    'serialNumber': data['serialnumber'],
                    'price': price,
                    'depr_method': depr_method,
                    'depr_expense': opt['depr_Expense'],
                    'startdate': startdate,
                    'fk_goods': data['fk_goods'],
                    'createddate': now,
                    'createdby': user
                }
                if opt['depr_method'] == 'SYD':
                    settings['depr_acc'] = opt['depr_acc']
                return settings

            if depr_method == 'SL' or depr_method == 'DDB':
                depr_expense = price / (economiclife * 12)
                for i in range(int(economiclife * 12) + 1):
                    generate_acc_value(settings_generate({
                        'depr_method': depr_method,
                        'month_of': i,
                        'depr_Expense': depr_expense
                    }), values_insert)
            elif depr_method == 'SYD':
                arr_year = [i for i in range(int(economiclife), 0, -1)]
                total_year = 0
                for i in arr_year:
                    total_year += i
                arr_depr_expense = [int(i / total_year * int(price))
                                    for i in arr_year]  # per tahun
                depr_acc = 0
                month_of = 0
                generate_acc_value(settings_generate({
                    'depr_method': 'SYD',
                    'depr_acc': Decimal('0.00'),
                    'depr_Expense': Decimal(arr_depr_expense[0] / 12),
                    'month_of': 0
                }), values_insert)
                for i in arr_depr_expense:
                    for j in range(1, 13):
                        depr_acc += Decimal(i / 12)
                        month_of += 1
                        generate_acc_value(settings_generate({
                            'depr_method': 'SYD',
                            'depr_acc': depr_acc,
                            'depr_Expense': Decimal(i / 12),
                            'month_of': month_of
                        }), values_insert)
            str_values = ','.join(values_insert)
            NAAccFa.objects.create_acc_FA(str_values)
        return 'Successfully generate fix asset'

    @staticmethod
    @task(name='task_update_notifications')
    def task_update_notications(lookup, data):
        services = NAUpdateNotificationService(
            lookup=lookup,
            data=data
        )
        services.execute()
        return 'Successfully update notifications'


class NATaskSchedule(object):

    @staticmethod
    @periodic_task(run_every=(crontab(hour=23, minute=59)),
                   name="task_push_notification_ga_reg_expire",
                   ignore_result=True)
    @transaction.atomic
    def task_push_notification_ga_reg_expire():
        reg_expire = NAGaVnHistory.get_expired_regs()
        if reg_expire:
            ga_user = NAPrivilege.objects.filter(
                divisi=NAPrivilege.GA,
                is_active=True,
                role=NAPrivilege.SUPER_USER
            )
            ga_user = list(ga_user)
            if ga_user:
                services = NAPushNotificationService(reg_expire=reg_expire, user=ga_user)
                services.execute()
                return 'Successfully push notifications'
            return 'There\'s No User for receive notifications'
        return 'There\'s no notifications'
