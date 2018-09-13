from django.conf.urls import url
from app.NA_Views.MasterData import NA_Supplier_View

urlpatterns = [
	url(r'^$', NA_Supplier_View.NA_Supplier, name='NA_Supplier'),
    url(r'^delete/$', NA_Supplier_View.NA_Supplier_delete, name='NA_Supplier_delete'),
    url(r'^EntrySupplier/$', NA_Supplier_View.EntrySupplier),
    url(r'^getData/', NA_Supplier_View.NA_SupplierGetData,name='NA_Supplier_data'),
    url(r'^customFilter/$', NA_Supplier_View.ShowCustomFilter),
    url(r'^SearchSupplierbyForm/$',NA_Supplier_View.SearchSupplierbyForm),
]
