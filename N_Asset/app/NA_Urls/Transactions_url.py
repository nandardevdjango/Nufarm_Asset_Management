from django.conf.urls import url,include

urlpatterns = [
	url(r'^Goods_Receive/IT/',include('app.NA_Urls.Transactions.NA_Goods_Receive_url',namespace='NA_Goods_Receive')),
	url(r'^Goods_Receive/Accessories/',include('app.NA_Urls.Transactions.NA_Goods_Receive_other_url',namespace='NA_Goods_Receive_other')),

	url(r'^Goods_Outwards/',include('app.NA_Urls.Transactions.NA_Goods_Outwards_url',namespace='NA_Goods_Outwards')),
	url(r'^Goods_Lending/',include('app.NA_Urls.Transactions.NA_Goods_Lending_url',namespace='NA_Goods_Lending')),

	url(r'^Goods_Return/',include('app.NA_Urls.Transactions.NA_Goods_Return_url',namespace='NA_Goods_Return')),
	url(r'^Goods_Lost/',include('app.NA_Urls.Transactions.NA_Goods_Lost_url',namespace='NA_Goods_Lost')),
	url(r'^Assets_Depreciation/',include('app.NA_Urls.Transactions.NA_Acc_FA_url',namespace='NA_Acc_FA')),
	url(r'^Maintenance/',include('app.NA_Urls.Transactions.NA_Maintenance_url',namespace='NA_Maintenance'))
]