from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Lending_View
from django.views.generic import RedirectView

urlpatterns = [
	url(r'^$',NA_Goods_Lending_View.NA_Goods_Lending,name='GoodsLending'),
	url(r'^NA_Goods_Lending_Search/$',NA_Goods_Lending_View.NA_Goods_Lending_Search,name='GoodsLendingManager'),
	url(r'^ShowEntry_Lending',NA_Goods_Lending_View.ShowEntry_Lending,name='ShowEntryLending'),
	url(r'^UpdateStatus/$',NA_Goods_Lending_View.UpdateStatus,name='UpdateStatusNAGoodsLending'),
	url(r'^Delete/$',NA_Goods_Lending_View.Delete,name='delete'),
	url(r'^HasExists/$',NA_Goods_Lending_View.HasExists,name='existsLending'),
	url(r'^geInterests/$',NA_Goods_Lending_View.getInterest,name='getinterests'),
	url(r'^getLastTransGoods/$',NA_Goods_Lending_View.getLastTransGoods,name='getlastTransGoods'),
	url(r'^getGoodsWithHistory/$',NA_Goods_Lending_View.getGoodsWithHistory,name='getGoodsWithHistory'),
    url(r'^getEmployee/$', RedirectView.as_view(url='/Transactions/Goods_Receive/IT/getEmployee/',permanent=False,query_string=True),name='redirect-to-getEmployee'),#ambil funtion yang sudah ada di receive view
	#url(r'^getEmployee/$', RedirectView.as_view(url='/NA_Goods_Receive/getEmployee/',permanent=False,query_string=True),name='redirect-to-getEmployee'),#ambil funtion yang sudah ada di receive view
	url(r'^SearchEmployeebyform/$',RedirectView.as_view(url='/Transactions/Goods_Receive/IT/SearchEmployeebyform/',permanent=False,query_string=True),name='redirect-to-SearchEmployeebyform'),#ambil funtion yang sudah ada di receive view
	url(r'^customFilter/$',NA_Goods_Lending_View.ShowCustomFilter,name='SowCustomFilter_Lending'),
	url(r'^ExportToExcel/$',NA_Goods_Lending_View.export_to_excels,name='export_goods_Lending_xls')
]
