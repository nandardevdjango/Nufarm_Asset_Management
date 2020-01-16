import io
import datetime
from django.conf import settings
from NA_DataLayer.common import *
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter,A4,landscape
from reportlab.lib import units, colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT,TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,SimpleDocTemplate,Spacer,Table,TableStyle,Image,Indenter
from NA_Report.PDFBaseHelper import BaseHelper
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
class NA_GO_PDF:
    helper = BaseHelper()
    main_display_table = ['GoodsName','BrandName', 'Serial_Number', 'Goods_Type', 'Date_Request', 'Date_Released','IsNew', 'for_employee','Eks_Employee','Sender','Responsible_by', 'Ref_GoodsFrom', 'Equipment','Descriptions']
    main_display_add_hoc = ['GoodsName', 'BrandName', 'SerialNumber', 'Type',
                            'DateReleased', 'ToEmployee', 'Equipment', 'Descriptions', 'Conditions','Eks_Employee','Sender' ]
    Header_Cols = None

    def __init__(self,title):
        self.file = io.BytesIO()
        self.width, self.height = A4
        #self.canvas = canv
        self.flowables = []
        self.Header_Cols = [[self.helper.create_bold_text(BoldCols, size=9) for BoldCols in self.main_display_table]]
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
                                     bottomMargin=self.frameDoc.bottom, title=title, displayDocTitle=True)
    def set_cursor(self, x, y):        
        self.cursor = self.helper.Position(x, y)
        self.doc.Position = self.cursor
        return self.cursor
    #def move_cursor(self, x=0, y=0):
    #    return self.set_cursor(
    #        self.cursor.x + x,
    #        self.cursor.y + y)
    def AddLogoHeader(self, canv, doc):
        width, height = doc.pagesize
        img = Image(doc.logo_path_header, width=113, height=28)
        img.wrapOn(canv, width, height)
        x, y = doc.Position
        img.drawOn(canv, x, y)
    def buildAddHocPDF(self,Data=None):
        #buat text centered
        BAState = Paragraph("Berita Acara ", self.helper.CENTER_STYLE_H1)       
        self.flowables.append(BAState)
        self.flowables.append(Spacer(0, 50))
        ToEmployee = Data[self.main_display_add_hoc[5]]
        Descriptions = Data[self.main_display_add_hoc[7]]
        GoodsName = Data[self.main_display_add_hoc[0]]
        self.canv.setTitle("Goods_Outwards_" + GoodsName)
        self.canv.setTitle("Goods_Outwards_" + GoodsName)
        BrandName = Data[self.main_display_add_hoc[1]]
        Type = Data[self.main_display_add_hoc[3]]
        SerialNumber = Data[self.main_display_add_hoc[2]]
        Kondisi = Data[self.main_display_add_hoc[8]]
        Equipment = Data[self.main_display_add_hoc[6]]
        DateReleased = Data[self.main_display_add_hoc[4]]
        Sender = Data[self.main_display_add_hoc[10]]
        self.flowables.append(Paragraph("""Telah diserahkan 1 unit barang inventaris kepada Saudara/(Saudari){ToEmployee}, <br/> <br/>
        """ .format(ToEmployee=ToEmployee, GoodsName=GoodsName),self.helper.LABEL_STYLE))

        self.flowables.append(Spacer(0, 25))

        #self.flowables.ap(Indenter(-90))
        colWidthBarang = [120, 250]
        
        berupa = Paragraph("<b>Berupa</b>", self.helper.LABEL_STYLE)
        barang = Paragraph(": {GoodsName}".format(GoodsName=GoodsName), self.helper.LABEL_STYLE)

        merk = Paragraph("<b>Merek</b>",self.helper.LABEL_STYLE)
        merkBarang = Paragraph(": {BrandName}".format(BrandName=BrandName), self.helper.LABEL_STYLE)

        LabelType = Paragraph("<b>Type</b>", self.helper.LABEL_STYLE)
        TypeBarang = Paragraph(": {Type}".format(Type=Type),self.helper.LABEL_STYLE)

        LabelSN = Paragraph("<b>SerialNumber/FA NO</b>", self.helper.LABEL_STYLE)
        DataSN = Paragraph(": {SerialNumber}".format(SerialNumber=SerialNumber), self.helper.LABEL_STYLE)
        
        DataBarang = [[berupa, barang], [merk, merkBarang], [LabelType, TypeBarang], [LabelSN, DataSN]]
        tblBarang = Table(DataBarang, colWidthBarang, None, style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT')]), hAlign='LEFT')
        self.flowables.append(tblBarang)

        self.flowables.append(Spacer(0, 20))
        self.flowables.append(Paragraph("{Descriptions}".format(Descriptions=Descriptions),self.helper.LABEL_STYLE))

        #self.flowables.append(Paragraph("""<b>Berupa&nbsp;&nbsp;: {GoodsName}<br/>Merek&nbsp;&nbsp;: {BrandName}<br/>Type&nbsp;&nbsp;: {Type}<br/>
        #ServiceTag/FA_Number&nbsp;&nbsp;: {SerialNumber}<br/><br/><br/>
        #Kelengkapan:</b>""" .format(GoodsName=GoodsName,BrandName=BrandName, Type=Type, SerialNumber=SerialNumber), self.helper.LABEL_STYLE))
        self.flowables.append(Spacer(0, 20))
        self.flowables.append(Paragraph("Kelengkapan : {}".format(Equipment), self.helper.LABEL_STYLE))#kelengkapan
        self.flowables.append(Spacer(0, 20))
        if Kondisi == "Bekas":
            EksEmployee = Data[self.main_display_add_hoc[9]]
            self.flowables.append(Paragraph("{GoodsName} ({Conditions} {EksEmployee})".format(
                GoodsName=GoodsName, Conditions=Kondisi, EksEmployee=EksEmployee), self.helper.LABEL_STYLE))
        elif Kondisi == "Baru":
            self.flowables.append(Paragraph("{GoodsName} {Conditions}".format(
                GoodsName=GoodsName, Conditions=Kondisi), self.helper.LABEL_STYLE))
        self.flowables.append(Spacer(0,20))
        self.flowables.append(Paragraph("Demikian berita acara ini di buat dengan sebenarnya", self.helper.LABEL_STYLE))
        self.flowables.append(Spacer(0, 25))
        self.flowables.append(Paragraph("Jakarta, {},".format(parse(str(DateReleased)).strftime('%d %B %Y')), self.helper.LABEL_STYLE))
        self.flowables.append(Spacer(0, 160))
        self.flowables.append(Indenter(left=130))
        #create table
        colWidths = [(self.width / 1.8) - 5, (self.width / 2) - 5]
        #self.flowables.append(i)
        Accepter = Paragraph("Yang Menerima", self.helper.LABEL_STYLE)
        Submitter = Paragraph("Yang Menyerahkan", self.helper.LABEL_STYLE)
        
        Data1 = [[Accepter,Submitter ]]
        tbl1 = Table(data=Data1,colWidths=colWidths, style=TableStyle([('ALIGN', (0,0), (-2,-1), 'LEFT'),('ALIGN',(0,1),(-1,-1),'RIGHT')]))
        self.flowables.append(tbl1)
        self.flowables.append(Spacer(0, 50))
        Data2 = [[Paragraph("(&nbsp;&nbsp;{}&nbsp;&nbsp;)".format(ToEmployee), self.helper.LABEL_STYLE), Paragraph(
            "(&nbsp;&nbsp;{}&nbsp;&nbsp;)".format(Sender), self.helper.LABEL_STYLE)]]
        tbl2 = Table(data=Data2, colWidths=colWidths, style=TableStyle([('ALIGN', (0, 0), (-2, -1), 'LEFT'), ('ALIGN', (0, 1), (-1, -1), 'RIGHT')]))
        self.flowables.append(tbl2)

        #add logo
        widthLogo = 187.5
        heightLogo = 137.25
        x, y = self.helper.coord(self.width - widthLogo, self.height-heightLogo, self.height,self.helper.unit_lookup["pt"] )
        self.set_cursor(x + 50, y-95)
        #self.doc.canv.setTitle("Goods_Outwards_" + GoodsName)
        self.doc.widthLogo = widthLogo
        self.doc.heigLogo = heightLogo
        self.doc.logo_path_header = settings.LOGO_IMAGE + "LogoHeader.jpg"
        self.doc.logo_path_footer = settings.LOGO_IMAGE + "LogoFooter.jpg"
        #self.helper.AddLogoHeader(self.canvas, self.doc)
        self.doc.build(
            self.flowables, onFirstPage=self.helper.header_and_footer)
        #self.doc.build(self.flowables, onFirstPage=self.AddLogoHeader)

        ReportFile = self.file.getvalue()
        self.file.close()
        return ReportFile
