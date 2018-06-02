from django.db import models
from NA_DataLayer.common import commonFunct, Data, Message

class NA_BR_Sys_Priviledge(models.Manager):
    def setInActive(self,idapp):
        NA_Sys_p = super(NA_BR_Sys_Priviledge,self).get_queryset().filter(idapp=idapp)
        if NA_Sys_p.exists():
            NA_Sys_p.inactive = commonFunct.str2bool(inactive)
            NA_Sys_p.save()
            return (Data.Success,)
        else:
            return (Data.Lost,Message.Lost)

    def Delete(self,idapp):
        data = super(NA_BR_Sys_Priviledge,self).get_queryset().filter(idapp=idapp)
        if data.exists():
            data.delete()
            return (Data.Success,)
        else:
            return (Data.Lost,Message.Lost)