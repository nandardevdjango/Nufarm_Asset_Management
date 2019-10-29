from django.conf.urls import url
from app.NA_Views.Transactions import NA_GoodsLost_View
from app.NA_Views.MasterData import NA_Employee_View
from app.NA_Views.Transactions import NA_Goods_Receive_View

urlpatterns = [
	url(r'^$',NA_GoodsLost_View.NA_Goods_Lost, name='NA_GoodsLost'),
    url(r'^getData/$',NA_GoodsLost_View.NA_GoodsLost_GetData),
    url(r'^ShowEntry/$',NA_GoodsLost_View.EntryGoods_Lost),
    url(r'^SearchGoodsByForm/',NA_GoodsLost_View.SearchGoodsbyForm),
	url(r'^customFilter/$', NA_GoodsLost_View.ShowCustomFilter),
    url(r'^SearchEmployeeByForm/$', NA_Employee_View.SearchEmployeebyform),
    url(r'^GetEmployeeByNIK', NA_Goods_Receive_View.getEmployee),
    url(r'^GetGoodsBySN/', NA_GoodsLost_View.GetGoodsBySN)
    #url(r'^api/Test/Get/(?P<SN>\w+)$',NA_GoodsLost_View.GetGoodsBySN)#only accept alphanumeric (?P<pk>[0-9]+)$
]
