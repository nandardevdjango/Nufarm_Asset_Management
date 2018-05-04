#from io import BytesIO
#from reportlab.pdfgen import canvas
#from django.http import HttpResponse
#from django.conf import settings
#from NA_Models.models import Employee
#from reportlab.lib import colors
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
#def write_pdf_view(request):
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

#    buffer = BytesIO()
#    #p = canvas.Canvas(buffer)

#    ## Start writing the PDF here
#    #dir_image = settings.BASE_DIR + '/app/static/app/images/NufarmLogo2.jpg'
#    #p.drawImage(dir_image,15,730,100,100)

 
#    doc = SimpleDocTemplate(settings.BASE_DIR + '/app/static/app/Upload/Template_Report.pdf')
#    # container for the 'Flowable' objects
#    elements = []
 
#    data= [['00', '01', '02', '03', '04'],
#           ['10', '11', '12', '13', '14'],
#           ['20', '21', '22', '23', '24'],
#           ['30', '31', '32', '33', '34']]
#    t=Table(data)
#    t.setStyle(TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
#                           ('TEXTCOLOR',(0,0),(1,-1),colors.red)]))
#    elements.append(t)
#    # write the document to disk
#    doc.build(elements)

#    #thead = ['Nik','Employee Name']
#    #data = Employee.objects.all().values('nik','employee_name')
#    #tbody = [i for i in data]
#    #for i in range(len(thead)):
#    #    p.drawString(15 + (i*30),680,thead[i])
#    #    for j in range(len(tbody)):
#    #        p.drawString(15,650-(j*30),tbody[j]['nik'])
#    # End writing

#    #p.showPage()
#    #p.save()

    
#    #canvas = doc.canv(buffer)
#    #pdf = buffer.getvalue()
#    #buffer.close()
#    pdf = open(settings.BASE_DIR + '/app/static/app/Upload/Template_Report.pdf','r')
#    response.write(pdf)
#    return response

#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.lib.units import inch
#from reportlab.lib.pagesizes import A4, landscape
#from reportlab.lib import colors
#from NA_Models.models import NAAccFa
#from django.http import HttpResponse

#def cetak_daftar_hadir(request):
#    # pengaturan respon berformat pdf
#    filename = "daftar_hadir_"
#    response = HttpResponse(content_type='application/pdf')
#    response['Content-Disposition'] = 'inline; filename="' + filename + '.pdf"'

#    # mengambil daftar kehadiran dan mengubahnya menjadi data ntuk tabel
#    data = NAAccFa.objects.values('depr_accumulation','bookvalue')
#    table_data = []
#    table_data.append([ "Depreciation Accumulation", "Book Value" ])
#    for x in data:
#        table_data.append([ x['depr_accumulation'], x['bookvalue'] ])


#    # membuat dokumen baru
#    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
#    print(doc.width)
#    styles = getSampleStyleSheet()

#    # pengaturan tabel di pdf
#    table_style = TableStyle([
#                               ('ALIGN',(1,1),(-2,-2),'RIGHT'),
#                               ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                               ('VALIGN',(0,0),(0,-1),'TOP'),
#                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#                           ])
#    kehadiran_table = Table(table_data, colWidths=[150,125])
#    kehadiran_table.setStyle(table_style)

#    # mengisi pdf
#    content = []
#    content.append(Paragraph('Daftar Kehadiran', styles['Title']))
#    content.append(Spacer(1,12))
#    content.append(Paragraph('Berikut ini adalah hasil rekam jejak kehadiran Anda selama :' , styles['Normal']))
#    content.append(Spacer(1,12))
#    content.append(kehadiran_table)
#    content.append(Spacer(1,36))
#    content.append(Paragraph('Mengetahui, ', styles['Normal']))
#    content.append(Spacer(1,48))
#    content.append(Paragraph('Mira Kumalasari, Head of Department PT. Ngabuburit Sentosa Sejahtera. ', styles['Normal']))

#    # menghasilkan pdf untk di download
#    doc.build(content)
#    return response