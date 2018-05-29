from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Outwards_View
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$',NA_Goods_Outwards_View.NA_Goods_Outwards,name='GoodsOutwards'),
    url(r'^NA_Goods_Outwards_Search/$',NA_Goods_Outwards_View.NA_Goods_Outwards_Search,name='GoodsOutwardManager'),
    url(r'^ShowEntry_Outwards/$',NA_Goods_Outwards_View.ShowEntry_Outwards,name='ShowEntryOutwards'),
    url(r'^getEmployee/$', RedirectView.as_view(url='/NA_Goods_Receive/getEmployee/',permanent=False,query_string=True),name='redirect-to-getEmployee-from-outwards'),#ambil funtion yang sudah ada di receive view
    url(r'^SearchEmployeebyform/$',RedirectView.as_view(url='/NA_Goods_Receive/SearchEmployeebyform/',permanent=False,query_string=True),name='redirect-to-SearchEmployeebyform-from-outwards'),#ambil funtion yang sudah ada di receive view
    url(r'^getGoodsWithHistory/$',NA_Goods_Outwards_View.getGoodsWithHistory,name='getGoodsWithHistory_Outwards'),
    url(r'^getLastTransGoods/$',NA_Goods_Outwards_View.getLastTransGoods,name='getlastTransGoods'),
]