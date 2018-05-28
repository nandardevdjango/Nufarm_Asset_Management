from django.conf.urls import url
from app.NA_Views.OtherPages import NA_Maintenance_View

urlpatterns = [
	url(r'^$',NA_Maintenance_View.NA_Maintenance,name='NA_Maintenance'),
    url(r'^getData/$',NA_Maintenance_View.NA_MaintenanceGetData),
    url(r'^ShowEntry/$',NA_Maintenance_View.EntryMaintenance),
    url(r'^SearchGoodsByForm/$',NA_Maintenance_View.SearchGoodsbyForm),
    url(r'^getGoods/$',NA_Maintenance_View.get_GoodsData),
    url(r'^delete/$',NA_Maintenance_View.Delete_M_data),
]