from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Receive_Detail
urlpatterns = [
		url(r'^$',NA_Goods_Receive_Detail.entrybatchdetail,name='entrybatchdetail'),
	]