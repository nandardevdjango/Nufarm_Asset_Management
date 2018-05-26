from django.conf.urls import url
from app.NA_Views import NA_Goods_View

urlpatterns = [
	url(r'^$',NA_Goods_View.NA_Goods,name='GoodMaster'),
	url(r'^NA_Goods_Search/$',NA_Goods_View.NA_Goods_Search,name='GoodsManager'),
	url(r'^SearchBrand/$',NA_Goods_View.Search_Brand, name='SearchBrand'),
    url(r'^ShowEntry',NA_Goods_View.ShowEntry,name='ShowEntry'),
	url(r'^customFilter',NA_Goods_View.ShowCustomFilter,name='ShowCustomFilter'),
	url(r'^Delete/$',NA_Goods_View.deleteItem,name='DeleteGoods'),
	url(r'^setInActive/$',NA_Goods_View.setInActive,name='SetInActive'),
    url(r'^SearchGoodsbyForm/$',NA_Goods_View.SearchGoodsbyForm)
]