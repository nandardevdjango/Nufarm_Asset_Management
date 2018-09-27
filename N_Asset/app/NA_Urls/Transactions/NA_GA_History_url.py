from django.conf.urls import url

from app.NA_Views.Transactions.NA_GA_History_View import (
    NAGaVnHistoryView, NAExtendGaVnHistoryView
)

urlpatterns = [
    url(r'^$', NAGaVnHistoryView.as_view()),
    url(r'^Extend/$', NAExtendGaVnHistoryView.as_view())
]
