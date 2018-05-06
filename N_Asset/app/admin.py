from django.contrib import admin
from NA_Models.models import *

admin.site.register(Employee)
admin.site.register(NASuplier)
admin.site.register(NAAccFa)
admin.site.register(goods)
admin.site.register(NAPriviledge)
admin.site.register(NAPriviledge_form)
admin.site.register(NASysPriviledge)
class LogAdmin(admin.ModelAdmin):

    list_filter = ["nameapp", "createddate"]
    list_display = ["idapp","createddate", "createdby", "nameapp"]
    search_fields = ["user__username", "user__email"]


admin.site.register(LogEvent, LogAdmin)