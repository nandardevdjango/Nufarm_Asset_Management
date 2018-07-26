from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_View,NA_Goods_Disposal_View,NA_Goods_Receive_View

urlpatterns = [
	url(r'^$',NA_Goods_Disposal_View.NA_Goods_Disposal,name='GoodsDisposal'),
    url(r'^NA_Goods_Disposal_Search/$',NA_Goods_Disposal_View.NA_Goods_Disposal_Search,name='GoodsDisposalManager'),
    url(r'^ShowEntry_Disposal',NA_Goods_Disposal_View.ShowEntry_Disposal,name='ShowEntryDisposal'),
	url(r'^getLastTransGoods/$',NA_Goods_Disposal_View.getLastTransGoods,name='getlastTransGoods_Disposal'),
	url(r'^getGoodsWithHistory/$',NA_Goods_Disposal_View.getGoodsWithHistory,name='getGoodsWithHistory_Disposal'),
	url(r'^SearchEmployeebyform/$',NA_Goods_Receive_View.SearchEmployeebyform),
	url(r'^getBookValue/$',NA_Goods_Disposal_View.getBookValue),
	url(r'^getEmployee/$',NA_Goods_Receive_View.getEmployee),#ambil funtion yang sudah ada di receive view
 #  url(r'^HasExists/$',NA_Goods_Outwards_View.hasExists),
	#url(r'^Delete/$',NA_Goods_Outwards_View.Delete),
	url(r'^customFilter/$',NA_Goods_Disposal_View.ShowCustomFilter)
	]