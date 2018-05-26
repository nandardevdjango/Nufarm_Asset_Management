from django.conf.urls import url
from app.NA_Views import NA_Acc_Fa_View

urlpatterns = [
	url(r'^$',NA_Acc_Fa_View.NA_Acc_FA, name='NA_Acc'),
	url(r'^ShowEntry/$',NA_Acc_Fa_View.EntryAcc, name='NA_Acc_Entry'),
    url(r'getData/$',NA_Acc_Fa_View.NA_AccGetData),
	url(r'^getGoods/$',NA_Acc_Fa_View.getGoods_data),
    url(r'^SearchGoodsByForm/$',NA_Acc_Fa_View.SearchGoodsbyForm),
    url(r'^customFilter/',NA_Acc_Fa_View.ShowCustomFilter),
]