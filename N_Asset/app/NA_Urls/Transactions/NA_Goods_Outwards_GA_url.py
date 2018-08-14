from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Outwards_GA_View as ga_outwards
from app.NA_Views.Transactions.NA_Equipment_View import NAEquipmentView, equipment_list

urlpatterns = [
    url(r'^$', ga_outwards.NA_Goods_Outwards_GA, name='GoodsOutwards'),
    url(r'^getData/$', ga_outwards.NA_Goods_Outwards_GAGetData),
    url(r'^ShowEntry/$', ga_outwards.Entry_Goods_Outwards_GA, name='ga_entry_outwards'),
    url(r'^add_equipment/$', NAEquipmentView.as_view(), name='ga_equipment'),
    url(r'^equipment/list/$', equipment_list, name='ga_equipment_list'),
    url(r'^search_ga_by_form/$', ga_outwards.search_ga_by_form)
]
