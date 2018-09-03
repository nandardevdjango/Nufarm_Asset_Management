from datetime import date, datetime

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from app.signals import logevent


class LogActivity:

    def __init__(self, models, activity, user, data):
        self.models = models
        self.activity = activity
        self.user = user

        if isinstance(data, Model):
            data = self.model_to_dict(
                model=data,
                to_json=True
            )
        self.data = data

    @staticmethod
    def model_to_dict(model, to_json=False):
        """
        helper for serialize instance of model
        """
        result = {}
        for field in model._meta.fields:
            name = field.name  # field name
            data = getattr(model, name)
            if to_json:
                if isinstance(data, datetime):
                    data = data.strftime('%d/%m/%Y %H:%M:%S')
                elif isinstance(data, date):
                    data = data.strftime('%d/%m/%Y')
            try:
                result[name] = eval(
                    'model.get_%s_display()' % name
                )
            except AttributeError:
                result[name] = data
        return result

    def record_activity(self):

        logevent.send(
            sender=self.models,
            models=self.models,
            activity=self.activity,
            user=self.user,
            data=self.data
        )

    @staticmethod
    def record(sender, models, activity, user, data, **kwargs):
        if not hasattr(models, 'FORM_NAME'):
            raise AttributeError('Please define form name')

        from NA_Models.models import LogEvent
        log = LogEvent()
        log.nameapp = '{activity} {models}'.format(
            activity=activity,
            models=models.FORM_NAME
        )
        log.model = ContentType.objects.get_for_model(models).model
        log.descriptions = data
        log.createdby = user
        log.createddate = datetime.now()
        log.save()

        return log


logevent.connect(LogActivity.record, weak=False)
