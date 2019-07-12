from reportlab.pdfgen.canvas import Canvas
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import units, colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
class NA_GR_PDF:
    main_display_table = []
    main_display_add_hoc = []