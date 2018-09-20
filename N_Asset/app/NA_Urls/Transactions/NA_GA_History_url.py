from django.conf.urls import url

from app.NA_Views.Transactions.NA_GA_History_View import NAGaVnHistoryView

urlpatterns = [
    url('^$', NAGaVnHistoryView.as_view())
]
