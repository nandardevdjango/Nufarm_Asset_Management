from django.conf.urls import url
from app.NA_Views.OtherPages import NA_EmailData_View

urlpatterns = [
	url(r'^NA_EmailData/$', NA_EmailData_View.NA_EmailData, name='NA_EmailData'),
    url(r'^NA_EmailUplData/$', NA_EmailData_View.NA_EmailUplData, name='NA_EmailUplData'),
    url(r'^NA_EmailData/searchBiodata/$', NA_EmailData_View.searchBiodata, name='NA_EmailData_searchBiodata'),
    url(r'^NA_Email/retriveBio/$', NA_EmailData_View.NA_Email_retriveBio, name='NA_Email_retriveBio'),
]