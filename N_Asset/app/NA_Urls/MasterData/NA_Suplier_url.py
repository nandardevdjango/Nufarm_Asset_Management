from django.conf.urls import url
from app.NA_Views import NA_Suplier_View

urlpatterns = [
	url(r'^$', NA_Suplier_View.NA_Suplier, name='NA_Suplier'),
    url(r'^delete/$', NA_Suplier_View.NA_Suplier_delete, name='NA_Suplier_delete'),
    url(r'^EntrySuplier/$', NA_Suplier_View.EntrySuplier),
    url(r'^getData/', NA_Suplier_View.NA_SuplierGetData,name='NA_Suplier_data'),
    url(r'^customFilter/$', NA_Suplier_View.ShowCustomFilter),
    url(r'^SearchSuplierbyForm/$',NA_Suplier_View.SearchSuplierbyForm),
]