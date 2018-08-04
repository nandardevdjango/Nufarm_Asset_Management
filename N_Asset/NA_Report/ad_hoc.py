from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class ReportAdHoc(object):
    def __init__(self, title, sub_title, detail):
        self.title = title
        self.sub_title = sub_title
        self.detail = detail
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer)
        self.layout = [Spacer(1, 0.5 * inch)]
        self.style = getSampleStyleSheet()

        self.style.add(
            ParagraphStyle(
                name='sub_title',
                parent=self.style['Normal'],
                fontSize=12,
                leading=16
            )
        )

        self.style.add(
            ParagraphStyle(
                name='detail',
                parent=self.style['Normal'],
                leading=24
            )
        )

    def create_title(self):
        self.layout.append(
            Paragraph(self.title, self.style['Title'])
        )

    def create_sub_title(self):
        self.layout.append(
            Paragraph(self.sub_title, self.style['sub_title'])
        )

    def create_detail(self):
        self.layout.append(Spacer(0, 20))
        detail = Table(
            [(key, ': {value}'.format(value=value)) for key, value in self.detail.items()],
            hAlign='LEFT'
        )
        self.layout.append(detail)

    def write_pdf_view(self):
        self.create_title()
        self.create_sub_title()
        self.create_detail()
        self.doc.build(self.layout)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
        response.write(self.buffer.getvalue())
        self.buffer.close()
        return response
