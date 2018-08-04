from io import BytesIO
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_RIGHT


class ReportAdHoc(object):
    def __init__(self, title, sub_title, detail):
        self.title = title
        self.sub_title = sub_title
        self.detail = detail
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(self.buffer, pagesize=A4)
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

        self.style.add(
            ParagraphStyle(
                name='signature_left',
                parent=self.style['Normal'],
                alignment=TA_LEFT,
                fontSize=12
            )
        )

        self.style.add(
            ParagraphStyle(
                name='signature_right',
                parent=self.style['Normal'],
                alignment=TA_RIGHT,
                fontSize=12
            )
        )

    def restore_default_canvas(self, canvas):
        canvas.restoreState()
        canvas.saveState()

    def mix_canvas_paragraph(self, paragraph, doc):
        paragraph.wrap(doc.width, doc.bottomMargin)

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

    def create_signature(self, canvas, doc, **kwargs):
        receiver = "Yang Menerima,"
        receiver = Paragraph(receiver, self.style['signature_left'])
        self.mix_canvas_paragraph(receiver, doc)
        receiver.drawOn(canvas, doc.leftMargin, 3.6 * inch)

        receiver_name = kwargs.get('receiver_name')
        receiver_name = Paragraph(receiver_name, self.style['signature_left'])
        self.mix_canvas_paragraph(receiver, doc)
        receiver_name.drawOn(canvas, doc.leftMargin, 4 * inch)

        sender = "Yang Menyerahkan,"
        sender = Paragraph(sender, self.style['signature_right'])
        self.mix_canvas_paragraph(sender, doc)
        sender.drawOn(canvas, doc.rightMargin, 3.6 * inch)

    def create_footer(self, canvas, doc):
        canvas.saveState()
        text = "Demikian Berita Acara ini dibuat dengan sebenarnya"
        canvas.drawString(inch, 4.5 * inch, text)
        tgl = "Jakarta, 14 Desember 2016"
        canvas.setFont('Helvetica-Bold', 13)
        canvas.drawString(inch, 4.2 * inch, tgl)
        self.create_signature(
            canvas=canvas,
            doc=doc,
            receiver_name='Nugraha Dila Prawisda'
        )
        canvas.restoreState()

    def first_page(self, canvas, doc):
        if doc.page > 1:
            return
        self.create_footer(canvas, doc)

    def last_page(self, canvas, doc):
        if doc.page > 1:
            self.create_footer(canvas, doc)

    def write_pdf_view(self):
        self.create_title()
        self.create_sub_title()
        self.create_detail()
        self.doc.build(
            self.layout,
            onFirstPage=self.first_page,
            onLaterPages=self.last_page
        )

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
        response.write(self.buffer.getvalue())
        self.buffer.close()
        return response
