from django.conf.urls import url
from app.NA_Views import NA_GoodsLost_View

urlpatterns = [
	url(r'^$',NA_GoodsLost_View.NA_Goods_Lost, name='NA_GoodsLost'),
    url(r'^getData/$',NA_GoodsLost_View.NA_GoodsLost_GetData),
    url(r'^ShowEntry/$',NA_GoodsLost_View.EntryGoods_Lost),
    url(r'^SearchGoodsByForm/',NA_GoodsLost_View.SearchGoodsbyForm),
	url(r'^customFilter/$',NA_GoodsLost_View.ShowCustomFilter),
]