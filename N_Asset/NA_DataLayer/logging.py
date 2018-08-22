from datetime import datetime
from django.dispatch import receiver
from NA_Models.models import LogEvent
from app.signals import NASignal, logevent


class LogActivity(object):

    def __init__(self, **kwargs):
        self.models = kwargs.get('models')
        self.activity = kwargs.get('activity')
        self.user = kwargs.get('user')
        data = kwargs.get('data')
        if isinstance(data, list):
            self.data = data
        else:
            self.data = [data]

@receiver(logevent)
def record(sender, models, activity, user, data, **kwargs):
    print('record')
        # log = LogEvent()
        # log.nameapp = '{models} {activity}'.format(
        #     models=self.models,
        #     activity=self.activity
        # )
        # log.descriptions = {
        #     self.activity: self.data
        # }
        # log.createdby = self.user
        # log.createddate = datetime.now()
        # log.save()

        # return log
