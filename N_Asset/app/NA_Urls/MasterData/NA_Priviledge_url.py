from django.conf.urls import url
from app.NA_Views.MasterData import NA_Priviledge_View

urlpatterns = [
	url(r'^$',NA_Priviledge_View.NA_Priviledge,name='NA_Priviledge'),
    url(r'^getData/$',NA_Priviledge_View.NA_PriviledgeGetData),
    url(r'^sys/$',NA_Priviledge_View.NA_Priviledge_sys),
    url(r'^ShowEntry/$',NA_Priviledge_View.Entry_Priviledge),
    url(r'^delete/$',NA_Priviledge_View.Delete_user)
]