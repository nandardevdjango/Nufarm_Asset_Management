from django.conf.urls import url
from app.NA_Views import NA_Employee_View

urlpatterns = [
	url(r'^$', NA_Employee_View.NA_Employee, name='NA_Employee'),
    url(r'^delete/$', NA_Employee_View.NA_Employee_delete, name='NA_Employee_delete'),
    url(r'^EntryEmployee/$', NA_Employee_View.EntryEmployee),
    url(r'^customFilter/$', NA_Employee_View.ShowCustomFilter),
    url(r'^getData/$', NA_Employee_View.NA_EmployeeGetData, name='NA_Employee_data'),
    url(r'^setInActive/$',NA_Employee_View.Set_InActive),
    url(r'^SearchEmployeeByForm/$',NA_Employee_View.SearchEmployeebyform),
]