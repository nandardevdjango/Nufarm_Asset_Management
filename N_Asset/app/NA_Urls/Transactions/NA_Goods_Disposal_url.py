from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_View,NA_Goods_Disposal_View
urlpatterns = [
	url(r'^$',NA_Goods_Disposal_View.NA_Goods_Disposal,name='GoodsDisposal'),
    url(r'^NA_Goods_Disposal_Search/$',NA_Goods_Disposal_View.NA_Goods_Disposal_Search,name='GoodsDisposalManager'),
    url(r'^ShowEntry_Disposal',NA_Goods_Disposal_View.ShowEntry_Disposal,name='ShowEntryDisposal'),
 #   url(r'^HasExists/$',NA_Goods_Outwards_View.hasExists),
	#url(r'^Delete/$',NA_Goods_Outwards_View.Delete),
	#url(r'^customFilter/$',NA_Goods_Outwards_View.ShowCustomFilter)
	]