from django.conf.urls import url

from .views import NANotificationView, dismiss_notification

urlpatterns = [
    url(r'^$', NANotificationView.as_view()),
    url('^dismiss/$', dismiss_notification)
]
