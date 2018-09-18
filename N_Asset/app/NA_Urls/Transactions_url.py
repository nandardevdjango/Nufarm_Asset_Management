from django.conf.urls import url, include

urlpatterns = [
    url(r'^Goods_Receive/IT/', include('app.NA_Urls.Transactions.NA_Goods_Receive_url',
                                       namespace='NA_Goods_Receive')),
    url(r'^Goods_Receive/Accessories/',
        include('app.NA_Urls.Transactions.NA_Goods_Receive_other_url', namespace='NA_Goods_Receive_other')),
    url(r'^Goods_Receive/GA/', include('app.NA_Urls.Transactions.NA_Goods_Receive_GA_url',
                                       namespace='NA_Goods_Receive_GA')),
    url(r'^Goods_Outwards/IT/', include('app.NA_Urls.Transactions.NA_Goods_Outwards_url',
                                     namespace='NA_Goods_Outwards')),
    url(r'^Goods_Lending/', include('app.NA_Urls.Transactions.NA_Goods_Lending_url',
                                    namespace='NA_Goods_Lending')),
    url(r'^Goods_Return/', include('app.NA_Urls.Transactions.NA_Goods_Return_url',
                                   namespace='NA_Goods_Return')),
    url(r'^Goods_Lost/', include('app.NA_Urls.Transactions.NA_Goods_Lost_url',
                                 namespace='NA_Goods_Lost')),
    url(r'^Goods_Disposal/', include('app.NA_Urls.Transactions.NA_Goods_Disposal_url',
                                     namespace='NA_Goods_Disposal')),
    url(r'^Goods_Outwards/GA/', include('app.NA_Urls.Transactions.NA_Goods_Outwards_GA_url',
                                    namespace='NA_Goods_Outwards_GA')),
    url(r'^GA_History/', include('app.NA_Urls.Transactions.NA_GA_History_url'))
]
