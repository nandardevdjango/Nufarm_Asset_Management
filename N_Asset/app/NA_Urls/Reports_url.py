from django.conf.urls import url
from ..NA_Views.NA_Report_View import create_ad_hoc

urlpatterns = [
    url(r'^first/$', create_ad_hoc)
]
