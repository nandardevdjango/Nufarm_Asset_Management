from django.dispatch import Signal

logevent = Signal(providing_args=['models', 'activity', 'user', 'data'])

class NASignal(object):

    def record_activity(self, models, activity, user, data):
        logevent.send(
            sender=models,
            models=models,
            activity=activity,
            user=user,
            data=data
        )
