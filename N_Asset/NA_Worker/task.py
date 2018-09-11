from datetime import datetime
from decimal import Decimal

from celery.schedules import crontab
from celery.task import task, periodic_task
from django.db import transaction

from NA_Models.models import NAGaVnHistory, NAPrivilege
from NA_Notifications.email import EmailNotification, EmailSubject
from NA_Notifications.models import NANotifications


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
            for reg in reg_expire:
                title = 'Please extend the tax {reg_number}'.format(
                    reg_number=reg.get('reg_number')
                )
                message = 'Reg Number {reg_number} will expire at {date_expire}'.format(
                    reg_number=reg.get('reg_number'),
                    date_expire=reg.get('date_expire')
                )

                try:
                    recent_notif = NANotifications.objects.get(
                        data__idapp=reg.get('idapp')
                    )
                    if reg.get('is_expire'):
                        message = 'Reg Number {reg_number} has expired at {date_expire}'
                        message = message.format(
                            reg_number=reg.get('reg_number'),
                            date_expire=reg.get('date_expire')
                        )
                    recent_notif.message = message
                    recent_notif.data = reg
                    recent_notif.save(update_fields=['message', 'data'])
                except NANotifications.DoesNotExist:
                    NANotifications.push_notifications(
                        to=ga_user,
                        name='ga_reg_notif',
                        title=title,
                        message=message,
                        data=reg
                    )
