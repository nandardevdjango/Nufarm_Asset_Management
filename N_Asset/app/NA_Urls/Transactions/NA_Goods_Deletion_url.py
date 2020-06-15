from django.conf.urls import url
from app.NA_Views.Transactions import NA_Goods_Deletion_View
urlpatterns = [
    url(r'^$',NA_Goods_Deletion_View.NA_Goods_Deletion,name="GoodsDeletion")
]