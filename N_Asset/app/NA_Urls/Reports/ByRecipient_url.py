from django.conf.urls import url
from app.NA_Views.Reports import NA_ReportByRecipient_View
from django.views.generic import RedirectView
urlpatterns = [
    url(r'^$', NA_ReportByRecipient_View.NA_Report_ByRecipient,
        name='Report_ByRecipient'),
    url(r'^NA_Report_ByRecipient_Search/$',
        NA_ReportByRecipient_View.NA_Report_ByRecipient_Search, name='SearchReportByRecipient'),
    url(r'^customFilter/$', NA_ReportByRecipient_View.ShowCustomFilter),
    url(r'^ExportToExcel/$', NA_ReportByRecipient_View.export_to_excels,
        name='export_ReportByRecipient_xls')
]
