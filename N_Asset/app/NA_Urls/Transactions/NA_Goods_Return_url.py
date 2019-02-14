from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Return_View,NA_Goods_Receive_View

urlpatterns = [
	url(r'^$',NA_Goods_Return_View.NA_Goods_Return,name='GoodsReturn'),
    url(r'^getData/$',NA_Goods_Return_View.NA_Goods_ReturnGetData),
    url(r'^ShowEntry/$',NA_Goods_Return_View.Entry_GoodsReturn),
    url(r'^SearchGoodsByForm/$',NA_Goods_Return_View.SearchGoodsbyForm),
    url(r'^getGoods/$',NA_Goods_Return_View.get_GoodsData),
    url(r'^delete/$',NA_Goods_Return_View.Delete_data),
    url(r'^customFilter/$',NA_Goods_Return_View.ShowCustomFilter),
	url(r'^getLastTrans/$',NA_Goods_Return_View.getLastTrans),
    url(r'^getEmployee/$',NA_Goods_Receive_View.getEmployee)#ambil funtion yang sudah ada di receive view
]