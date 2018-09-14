from NA_Notifications.models import NANotifications


class NAPushNotificationService(object):
    def __init__(self, reg_expire, user):
        self.reg_expire = reg_expire
        self.user = user

    def execute(self):
        if self.reg_expire:
            for reg in self.reg_expire:
                title = 'Please extend the tax {reg_number}'.format(
                    reg_number=reg.get('reg_number')
                )
                message = 'Reg Number {reg_number} will expire at {date_expire}'.format(
                    reg_number=reg.get('reg_number'),
                    date_expire=reg.get('date_expire')
                )

                try:
                    recent_notif = NANotifications.objects.get(
                        is_active=True,
                        data__idapp=reg.get('idapp')
                    )
                    if reg.get('is_expire'):
                        message = 'Reg Number {reg_number} has expired at {date_expire}'
                        message = message.format(
                            reg_number=reg.get('reg_number'),
                            date_expire=reg.get('date_expire')
                        )
                    reg['is_dismissed'] = recent_notif.data['is_dismissed']
                    recent_notif.message = message
                    recent_notif.data = reg
                    recent_notif.save(update_fields=['message', 'data'])
                except NANotifications.DoesNotExist:
                    NANotifications.push_notifications(
                        to=self.user,
                        name='ga_reg_notif',
                        title=title,
                        message=message,
                        data=reg
                    )


class NAUpdateNotificationService(object):
    def __init__(self, lookup, data):
        self.lookup = lookup
        self.data = data

    def execute(self):
        filter_kwargs = {
            'is_active': True
        }
        for k, v in self.lookup.items():
            filter_kwargs.update({
                'data__%s' % k: v
            })
        notifications = NANotifications.objects.filter(**filter_kwargs)
        if notifications.exists():
            for notif in notifications:
                notif.data.update(self.data)
                notif.save()