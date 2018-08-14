from datetime import date
from django.db import models

class NAGaVnHistoryBR(models.Manager):

    def active(self):
        today = date.today()
        return super(NAGaVnHistoryBR, self).get_queryset().filter(
            expired_reg__gt=today,
            bpkb_expired__gt=today
        )