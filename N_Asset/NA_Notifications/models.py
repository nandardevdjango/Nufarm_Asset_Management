from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.functional import cached_property

from NA_DataLayer.fields import JSONField


User = get_user_model()


class NANotifications(models.Model):

    idapp = models.AutoField(primary_key=True, db_column='idapp')
    user = models.ManyToManyField(
        User,
        db_constraint=False
    )
    name = models.CharField(max_length=100, db_column='name')
    title = models.CharField(max_length=150, db_column='title')
    message = models.CharField(max_length=255, db_column='message')
    is_active = models.BooleanField(default=True, db_column='is_active')
    data = JSONField(db_column='data')
    created_date = models.DateTimeField(db_column='created_date')

    def __str__(self):
        return self.name

    @cached_property
    def recipients(self):
        return list(self.user.all())

    @classmethod
    @transaction.atomic
    def push_notifications(cls, to, name, title, message, data):
        notifications = cls()
        notifications.name = name
        notifications.title = title
        notifications.message = message
        notifications.data = data
        notifications.created_date = datetime.now()
        notifications.save()

        if isinstance(to, models.query.QuerySet):
            to = list(to)
        notifications.user.add(*to)

    @classmethod
    def dismiss_notifications(cls, notif_id):
        filter_kwargs = {
            'idapp': notif_id
        }
        if isinstance(notif_id, list):
            filter_kwargs = {
                'idapp__in': notif_id
            }
        notifications = cls.objects.filter(**filter_kwargs)
        for notif in notifications:
            notif.data.update({
                'is_dismissed': True
            })
            notif.save()

    class Meta:
        managed = True
        db_table = 'n_a_notifications'
