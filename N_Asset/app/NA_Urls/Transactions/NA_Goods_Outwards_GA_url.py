from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Outwards_GA_View as ga_outwards

urlpatterns = [
    url(r'^$', ga_outwards.NA_Goods_Outwards_GA, name='GoodsOutwards'),
    url(r'^getData/$', ga_outwards.NA_Goods_Outwards_GAGetData),
    url(r'^ShowEntry/$', ga_outwards.Entry_Goods_Outwards_GA)
]
