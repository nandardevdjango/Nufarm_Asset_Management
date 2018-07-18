from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_GA_View

urlpatterns = [
    url(r'^$', NA_Goods_Receive_GA_View.NA_Goods_Receive_GA, name='GoodsReceive'),
    url(r'^getData/$', NA_Goods_Receive_GA_View.NA_Goods_Receive_GAGetData),
    url(r'^ShowEntry/$', NA_Goods_Receive_GA_View.Entry_Goods_Receive_GA)
]