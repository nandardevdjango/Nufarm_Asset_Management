import io
import datetime
from NA_DataLayer.common import *
from reportlab.pdfgen.canvas import Canvas
from django.conf import settings
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib import units, colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer
from NA_Report.PDFBaseHelper import BaseHelper
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
class NA_GR_PDF:
    helper = BaseHelper()
    main_display_table = ['Goods','BrandName', 'Serial_Number', 'Goods_Type', 'Date_Request', 'Date_Released','IsNew', 'for_employee','Eks_Employee','Sender','Responsible_by', 'Ref_GoodsFrom', 'Equipment','Descriptions']
    main_display_add_hoc = ['GoodsName', 'BrandName', 'SerialNumber', 'Type',
                            'DateReleased', 'ToEmployee', 'Equipment', 'Descriptions', 'Conditions', ]
    Header_Cols = None

    def __init__(self, canv=None, Data=None):
        self.file = io.BytesIO()
        self.width, self.height = A4
        self.canvas = canv
        self.flowables = []
        self.Header_Cols = [[self.helper.create_bold_text(
            BoldCols, size=9) for BoldCols in self.main_display_table]]
        if not canv:
            self.canv = Canvas(self.file, pagesize=A4)
            self.canv.setAuthor('Nandar HayHay')
        #set margin canvas
        self.frameDoc = self.helper.Margin(self.helper.u('0.4in'), self.helper.u('0.3in'), self.helper.u('0.4in'), self.helper.u('0.3in'))
        #set cursor langsung
        self.cursor = self.helper.Position(
            self.frameDoc.left,
             self.height - self.frameDoc.top
         )
        self.doc = SimpleDocTemplate(self.file, pagesize=A4, topMargin=self.frameDoc.top,
                                     leftMargin=self.frameDoc.left,
                                     rightMargin=self.frameDoc.right,
                                     bottomMargin=self.frameDoc.bottom)
    def set_cursor(self, x, y):
        self.cursor = self.helper.Position(x, y)
        return self.cursor

    def move_cursor(self, x=0, y=0):
        return self.set_cursor(
            self.cursor.x + x,
            self.cursor.y + y)
    def buildAddHocPDF(self,Data=None):
        #buat text centered
        BAState = Paragraph("Berita Acara ",helper.CENTER_STYLE_H1)
        self.flowables.append(BAState)
        self.flowables.append(Spacer(0, 50))
        self.flowables.append("""Telah diserahkan 1 unit barang inventaris kepada {ToEmployee}, {Descriptions} Berupa {GoodsName}
        """ .format(ToEmployee=Data[0][main_display_add_hoc[5]], Descriptions=Data[0][main_display_add_hoc[7]], GoodsName=Data[0][main_display_add_hoc[0]]))
        self.flowables.append(Spacer(0, 25))
        kondisi = main_display_add_hoc[7]
        self.flowables.append(Paragraph("""<b>Merek&emsp;&emsp;: {BrandName}<br/>Type&emsp;&emsp;: {Type}<br/>
        ServiceTag/FA_Number&emsp;&emsp;: {SerialNumber}<br/>
        Kelengkapan:</b>""" .format(BrandName=main_display_add_hoc[1], Type=main_display_table[3], SerialNumber=main_display_add_hoc[2,]), helper.LABEL_STYLE))
        self.flowables.append(Spacer(0, 20))
        self.flowables.append(Paragraph("{}".format(main_display_add_hoc[6]), helper.LABEL_STYLE))
        self.flowables.append(Spacer(0,20))
        self.flowables.append(Paragraph("Demikian berita acara ini di buat dengan sebenarnya", helper.LABEL_STYLE))
        self.flowables.append(Spacer(0, 25))
        self.flowables.append(Paragraph("Jakarta {}".format(datetime.datetime.strptime(main_display_add_hoc[4], '%Y-%m-%d')), helper.LABEL_STYLE))
        self.flowables.append