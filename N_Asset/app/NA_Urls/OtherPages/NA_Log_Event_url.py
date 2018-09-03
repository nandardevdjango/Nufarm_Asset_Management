from django.conf.urls import url
from app.NA_Views.OtherPages import NA_LogEvent_View

urlpatterns = [
	url(r'^NA_LogEvent/$', NA_LogEvent_View.NA_LogEvent_data, name='NA_LogEvent'),
    url(r'^NA_LogEvent/desc/$', NA_LogEvent_View.log_activity_data, name='NA_LogEvent_descriptions'),
]