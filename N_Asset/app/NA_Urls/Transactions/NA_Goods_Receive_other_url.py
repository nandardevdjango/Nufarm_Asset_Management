from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_Other_View

urlpatterns = [
	url(r'^$',NA_Goods_Receive_Other_View.NA_Goods_Receive_other,name='NA_Goods_Receive_other'),
    url(r'^getData/$',NA_Goods_Receive_Other_View.NA_Goods_Receive_otherGetData),
    url(r'^ShowEntry/$',NA_Goods_Receive_Other_View.Entry_Goods_Receive_other),
    url(r'^delete/$',NA_Goods_Receive_Other_View.Delete_data),
    url(r'^customFilter/$',NA_Goods_Receive_Other_View.ShowCustomFilter)
]