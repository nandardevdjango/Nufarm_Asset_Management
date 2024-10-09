from django.conf.urls import url
from app.NA_Views.Reports import NA_ReportByRefNumber_View
from django.views.generic import RedirectView
urlpatterns = [
    url(r'^$', NA_ReportByRefNumber_View.NA_Report_ByRefNumber,
        name='Report_ByRefNumber'),
    url(r'^NA_Report_ByRefNo_Search/$',
        NA_ReportByRefNumber_View.NA_Report_ByRefNumber_Search, name='SearchReportByRefNumber'),
    url(r'^customFilter/$', NA_ReportByRefNumber_View.ShowCustomFilter),
    url(r'^ExportToExcel/$', NA_ReportByRefNumber_View.export_to_excels,
        name='export_ReportByRefNumber_xls')
]
