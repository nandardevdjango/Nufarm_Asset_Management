from django.conf.urls import url

from .views import NANotificationView

urlpatterns = [
    url(r'^$', NANotificationView.as_view())
]
