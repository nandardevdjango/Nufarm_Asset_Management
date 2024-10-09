from django.conf.urls import url, include
from app.NA_Views.Reports.NA_Report_View import create_ad_hoc
urlpatterns = [
    url(r'^ByRecipient/', include('app.NA_Urls.Reports.ByRecipient_url',
                                  namespace='ReportByRecipient')),
    url(r'^ByRefNumber/', include('app.NA_Urls.Reports.ByRefNumber_url',
                                  namespace='ReportByRefNumber')),
    #    url(r'^Reports/BySerialNumber', include('app.NA_Urls.Reports.BySerialNumber',
    #                                            namespace='ReportBySerialNumber'))
]
