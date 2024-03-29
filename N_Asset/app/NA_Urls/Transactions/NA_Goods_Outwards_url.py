from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Outwards_View,NA_Goods_Receive_View
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$',NA_Goods_Outwards_View.NA_Goods_Outwards,name='GoodsOutwards'),
    url(r'^NA_Goods_Outwards_Search/$',NA_Goods_Outwards_View.NA_Goods_Outwards_Search,name='GoodsOutwardManager'),
    url(r'^ShowEntry_Outwards',NA_Goods_Outwards_View.ShowEntry_Outwards,name='ShowEntryOutwards'),
    url(r'^getEmployee/$',NA_Goods_Receive_View.getEmployee),#ambil funtion yang sudah ada di receive view
    url(r'^SearchEmployeebyform/$',RedirectView.as_view(url='/Transactions/Goods_Receive/IT/SearchEmployeebyform/',permanent=False,query_string=True),name='redirect-to-SearchEmployeebyform-from-outwards'),#ambil funtion yang sudah ada di receive view
    url(r'^getGoodsWithHistory/$',NA_Goods_Outwards_View.getGoodsWithHistory,name='getGoodsWithHistory_Outwards'),
    url(r'^getLastTransGoods/$',NA_Goods_Outwards_View.getLastTransGoods,name='getlastTransGoods'),
    url(r'^HasExists/$',NA_Goods_Outwards_View.hasExists),
	url(r'^getLastDateTrans/$',NA_Goods_Outwards_View.getLastDateTrans),
	url(r'^Delete/$',NA_Goods_Outwards_View.Delete),
    url(r'^customFilter/$', NA_Goods_Outwards_View.ShowCustomFilter),
    url(r'^getReportAdHoc/$', NA_Goods_Outwards_View.getReportAdHoc),
    url(r'^ExportToExcel/$',NA_Goods_Outwards_View.export_to_excels,name='export_goods_xls')
]
