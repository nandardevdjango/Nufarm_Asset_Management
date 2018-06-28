from django.conf.urls import url,include

urlpatterns = [
	url(r'^Employee/',include('app.NA_Urls.MasterData.NA_Employee_url',namespace='NA_Employee')),
	url(r'^Suplier/',include('app.NA_Urls.MasterData.NA_Suplier_url',namespace='NA_Suplier')),
	url(r'^Goods/',include('app.NA_Urls.MasterData.NA_Goods_url',namespace='NA_Goods')),
	url(r'^Priviledge/',include('app.NA_Urls.MasterData.NA_Priviledge_url',namespace='NA_Priviledge'))
]