from django.db import models
from NA_DataLayer.common import commonFunct, Data, Message
from django.db.models import F

class NA_BR_Sys_Priviledge(models.Manager):
    def setInActive(self,idapp,inactive):
        NA_Sys_p = super(NA_BR_Sys_Priviledge,self).get_queryset().filter(idapp=idapp)
        if NA_Sys_p.exists():
            NA_Sys_p = NA_Sys_p[0]
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

    def CheckPermission(self,fk_form,user_id):
        data = super(NA_BR_Sys_Priviledge, self).get_queryset()\
            .annotate(form_name=F('fk_p_form__form_name'))\
            .values('form_name','permission')