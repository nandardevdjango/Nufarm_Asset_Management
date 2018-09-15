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

                if reg.get('is_expire'):
                    message = 'Reg Number {reg_number} has expired at {date_expire}'
                else:
                    message = 'Reg Number {reg_number} will expire at {date_expire}'

                message = message.format(
                    reg_number=reg.get('reg_number'),
                    date_expire=reg.get('date_expire')
                )

                try:
                    recent_notif = NANotifications.objects.get(
                        is_active=True,
                        data__idapp=reg.get('idapp')
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
        """
        :param lookup: -- for filter notifications by field(data) json
        :param data: -- data that has changed
        """
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
        try:
            notification = NANotifications.objects.get(**filter_kwargs)
            notification.data.update(self.data)
            notification.save()
        except NANotifications.MultipleObjectsReturned:
            notification = NANotifications.objects.filter(**filter_kwargs)
            for notif in notification:
                notif.data.update(self.data)
                notif.save()
        except NANotifications.DoesNotExist:
            pass

# TODO: Create service clear notifications if reg number has extended and clear session
