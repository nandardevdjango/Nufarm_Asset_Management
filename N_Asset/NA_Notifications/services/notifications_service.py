from datetime import datetime

from app.sessions import NASession, SessionStore
from NA_Models.models import NAPrivilege
from NA_Notifications.models import NANotifications


class NAPushNotificationService(object):
    def __init__(self, data, user):
        self.data = data
        self.user = user

    def execute(self):
        if self.data:
            for reg in self.data:
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
        micro service: -- update notifications data, if other relation data has updated
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


class NAClearNotificationService(object):
    def __init__(self, lookup):
        self.lookup = lookup

    def execute(self):
        filter_kwargs = {
            'is_active': True
        }
        for k, v in self.lookup.items():
            filter_kwargs.update({
                'data__%s' % k: v
            })
        notification = NANotifications.objects.get(**filter_kwargs)
        notification.is_active = False
        notification.save()

        if not (NANotifications.objects.filter(is_active=True)
                                       .exists()):
            ga_user = NAPrivilege.get_ga_super_user().values_list('idapp', flat=True)
            sessions = NASession.objects.filter(
                expire_date__gte=datetime.now(),
                user_id__in=ga_user
            )

            for session in sessions:
                session_data = session.get_decoded()
                del session_data['ga_reg_notif']
                del session_data['ga_notif_expired']
                encoded_data = SessionStore.encode_session(session_data)
                session.session_data = encoded_data
                session.save()
