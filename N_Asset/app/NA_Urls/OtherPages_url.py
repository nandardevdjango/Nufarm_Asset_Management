from django.conf.urls import url,include

urlpatterns = [
	url(r'',include('app.NA_Urls.OtherPages.NA_Log_Event_url',namespace='NA_Log_Event')),
	url(r'',include('app.NA_Urls.OtherPages.NA_Email_Data_url',namespace='NA_Email_Data'))
]