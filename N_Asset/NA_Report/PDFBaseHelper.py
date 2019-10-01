import string
import collections

from reportlab.pdfgen.canvas import Canvas
from django.conf import settings
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_RIGHT,TA_LEFT
from reportlab.lib import units, colors
from reportlab.lib.styles import ParagraphStyle,getSampleStyleSheet
from reportlab.platypus import Paragraph,Flowable,Image
class BaseHelper:
	digit_chars = string.digits + '.'
	unit_lookup = {
		'pt': 1,
		'in': units.inch,
		'cm': units.cm,
		'mm': units.mm
	}

	Margin = collections.namedtuple("Margin", ['top', 'right', 'bottom', 'left'])
	#Size = collections.namedtuple("Size", ['x', 'y', 'width', 'height'])
	Position = collections.namedtuple("Position", ['x', 'y'])
	LEADING_FACTOR = 1.2
	#A4 width = 8.25 -->jadinya 7.8 inch an
	#  height = 11.67 -->jadinya 10.9inh an lah
	#ipixel = 0.75pt
	def Style(name, font='Helvetica', size=12, leading=14, color=colors.black,alignment=TA_LEFT):
		return ParagraphStyle(
			name,
			fontName=font,
			fontSize=size,
			leading=leading or (size * LEADING_FACTOR),
			textColor=color,
			alignment=alignment
		)
	LABEL_STYLE =Style('label', 'Helvetica', size=10, color=colors.gray)
	BODY_STYLE = Style('body', 'Times')
	VALUE_STYLE = Style('value', 'Helvetica')
	FOOTNOTE_STYLE =Style('footnote', 'Courier', size=9)
	CENTER_STYLE = Style('Centered', 'Times',alignment=TA_CENTER)
	CENTER_STYLE_H1 = Style('Centered', 'Times', size=16, alignment=TA_CENTER)

	@classmethod
	def AddLogoHeader(cls,canv, doc):
		width,height = doc.pagesize
		img = Image(doc.logo_path_header, width=113, height=28)
		img.wrapOn(canv, width, height)
		x,y = doc.Position
		img.drawOn(canv, x, y)

	@classmethod	
	def coord(cls,x, y, height, unit):
		"""
		Helper class to help position flowables in Canvas objects
		"""
		retx, rety = x * unit, height - y * unit
		return retx, rety

	@classmethod
	def draw_paragraph(cls,text,Cursor_x,cursor_y, max_width, max_height, style,canv):
		if not text:
			text = ''
		if not isinstance(text, str):
			text = str(text)
		text = text.strip(string.whitespace)
		text = text.replace('\n', "<br/>")
		p = Paragraph(text, style)
		used_width, used_height = p.wrap(max_width, max_height)
		line_widths = p.getActualLineWidths0()
		number_of_lines = len(line_widths)
		if number_of_lines > 1:
			actual_width = used_width
		elif number_of_lines == 1:
			actual_width = min(line_widths)
			used_width, used_height = p.wrap(actual_width + 0.1, max_height)
		else:
			return 0, 0
		p.drawOn(canv, Cursor_x, cursor_y - used_height)
		return used_width, used_height

	@classmethod
	def create_bold_text(cls,text, size=8):
		return Paragraph('''<font size={size}><b>
		{text}</b></font>
		'''.format(size=size, text=text),cls.Style('Normal', font='Times', leading=1.35))
			
	@classmethod
	def u(cls,amount):
		units = ''.join([c for c in amount if c in string.ascii_letters])
		units = units.lower()
		number_string = ''.join([c for c in amount if c in cls.digit_chars])
		if '.' in number_string:
			number = float(number_string)
		else:
			number = int(number_string)
		multiplier = cls.unit_lookup.get(units, 1)
		return number * multiplier
	@classmethod
	def header(cls, canvas, doc):
		#canvas.savestate()
		cls.AddLogoHeader(canvas,doc)
		#width, height = doc.pagesize
		#styles = getSampleStyleSheet()
		#ptext = '<font size=10><b>Statement Date: {}' \
		#	'</b></font>'.format('01/01/2017')
		#p = Paragraph(ptext, styles["Normal"])
		#p.wrapOn(canvas, width, height)
		#p.drawOn(canvas, 400, 800)
		#ptext = '''<font size=10>
		#<b>Member:</b> {member}<br/>
		#<b>Member ID:</b> {member_id}<br/>
		#<b>Group #:</b> {group_num}<br/>
		#<b>Group name:</b> {group_name}<br/>
		#</font>
		#'''.format(member=doc.xml.member_name,
		#		member_id=doc.xml.member_id,
		#		group_num=doc.xml.group_num,
		#		group_name=doc.xml.group_name
		#		)
		#p = Paragraph(ptext, styles["Normal"])
		#p.wrapOn(canvas, width, height)
		#p.drawOn(canvas, 400, 730)
		## Add page number
		#page_num = canvas.getPageNumber()
		#text = "Page #%s" % page_num
		#canvas.drawRightString(200*mm, 20*mm, text)

	@classmethod
	def footer(cls, canvas, doc):
		#width, height = doc.pagesize
		#ptext = """<font name=times-roman size=16 color="#028654">Grow A better Tommorrow </font><img src="{LogoPath}" width="112.5" height="54.75"/>""".format(
		#	LogoPath= doc.logo_path_footer)
		#p = Paragraph(ptext, cls.LABEL_STYLE)
		#p.wrapOn(canvas, width, height)
		#p.drawOn(canvas, 250, 35)

		width, height = doc.pagesize
		img = Image(doc.logo_path_footer, width=160, height=75)
		img.wrapOn(canvas, width, height)
		x, y = doc.Position
		img.drawOn(canvas, x-30, y)
		#ptext = """Here is a picture:<img src="{LogoPath}" width="112.5" height="54.75"/> in the  middle of our text"""
		#width, height = doc.pagesize
		#img = Image(doc.logo_path, width=112.5, height=54.75)
		#img.wrapOn(canvas, width, height)
		#img.drawOn(canvas, 344, 50)

		#p = Paragraph(ptext, styles["Normal"])
		#p.wrapOn(canvas, width, height)
		#p.drawOn(canvas, 250, 35)
	@classmethod
	def header_and_footer(cls,canvas, doc):
		"""
		Add the header and footer to each page
		setting pertama footer, jadi untuk header nya mesti di tambahy position
		"""	
		cls.footer(canvas, doc)
		x, y = doc.Position
		y = y + 750
		doc.Position = x,y
		cls.header(canvas, doc)
	
class PageNumCanvas(Canvas):
	helper = BaseHelper
	"""untuk membuat page number"""
	def __init__(self, *args, **kwargs):
		"""Constructor"""
		Canvas.__init__(self, *args, **kwargs)
		self.pages = []
	def showPage(self):
		"""
		On a page break, add information to the list
		"""
		self.pages.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""
		Add the page number to each page (page x of y)
		"""
		page_count = len(self.pages)

		for page in self.pages:
			self.__dict__.update(page)
			self.draw_page_number(page_count)
			Canvas.showPage(self)

		Canvas.save(self)

	def draw_page_number(self, page_count):
		"""
		Add the page number
		"""
		page = "Page %s of %s" % (self._pageNumber, page_count)
		self.setFont("Helvetica", 9)
		self.drawRightString(helper.u('200mm'), helper.u('20mm'), page)
