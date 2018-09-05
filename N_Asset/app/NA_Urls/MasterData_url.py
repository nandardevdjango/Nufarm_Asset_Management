from django.conf.urls import url,include

urlpatterns = [
	url(r'^Employee/',include('app.NA_Urls.MasterData.NA_Employee_url',namespace='NA_Employee')),
	url(r'^Supplier/',include('app.NA_Urls.MasterData.NA_Supplier_url',namespace='NA_Supplier')),
	url(r'^Goods/',include('app.NA_Urls.MasterData.NA_Goods_url',namespace='NA_Goods')),
	url(r'^Privilege/',include('app.NA_Urls.MasterData.NA_Privilege_url',namespace='NA_Privilege'))
]