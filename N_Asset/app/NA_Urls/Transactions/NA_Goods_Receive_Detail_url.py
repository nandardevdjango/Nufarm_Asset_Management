from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_Detail,NA_Goods_Receive_View
urlpatterns = [
		url(r'^$',NA_Goods_Receive_Detail.entrybatchdetail,name='entrybatchdetail'),
        	url(r'^getBrandForDetailEntry/$',NA_Goods_Receive_View.getBrandForDetailEntry,name='getBrandForDetailEntry'),
	url(r'^getTypeApps/$',NA_Goods_Receive_View.getTypeApps,name='getTypeApps'),
    url(r'^deleteDetail/$',NA_Goods_Receive_View.deleteDetail,name='deleteDetail'),
    url(r'^getData/$',NA_Goods_Receive_Detail.getData),
	]