from django.contrib.auth import get_user_model
from django.db import models
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
    is_active = models.BooleanField(default=True, db_column='is_active')
    data = JSONField(db_column='data')
    created_date = models.DateTimeField(db_column='created_date')

    def __str__(self):
        return self.name

    @cached_property
    def recipients(self):
        return list(self.user.all())

    class Meta:
        managed = True
        db_table = 'n_a_notifications'
