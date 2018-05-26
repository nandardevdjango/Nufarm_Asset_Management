from django.conf.urls import url
from app.NA_Views import NA_Priviledge_View

urlpatterns = [
	url(r'^$',NA_Priviledge_View.NA_Priviledge,name='NA_Priviledge'),
    url(r'^getData/$',NA_Priviledge_View.NA_PriviledgeGetData),
    url(r'^sys/$',NA_Priviledge_View.NA_Priviledge_sys),
]