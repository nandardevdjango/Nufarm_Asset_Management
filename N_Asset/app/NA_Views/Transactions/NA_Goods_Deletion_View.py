from django.shortcuts import render, render_to_response
from datetime import datetime
from django.template import RequestContext
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsOutwards
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
from NA_DataLayer.common import decorators
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.views.decorators.csrf import ensure_csrf_cookie
from distutils.util import strtobool
from decimal import Decimal
import math
from NA_DataLayer.exceptions import NAError, NAErrorConstant, NAErrorHandler
from django.conf import settings
def NA_Goods_Deletion(request):
    	populate_combo = []
	#jieun heula query
	populate_combo.append(
	    	{'label': 'Goods Name', 'columnName': 'goods', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'Goods Type', 'columnName': 'typeapp', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'Serial Number', 'columnName': 'serialnumber', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'Book Value', 'columnName': 'bookvalue', 'dataType': 'decimal'})
	populate_combo.append({'label': 'Submission Value',
                        'columnName': 'submission_value', 'dataType': 'decimal'})
	populate_combo.append({'label': 'Date Released',
                        'columnName': 'datereleased', 'dataType': 'datetime'})
	populate_combo.append(
	    	{'label': 'Sender ', 'columnName': 'senderby', 'dataType': 'varchar'})
	populate_combo.append({'label': 'Responsible By',
                        'columnName': 'responsibleby', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'Goods From', 'columnName': 'refgoodsfrom', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'IsNew', 'columnName': 'isnew', 'dataType': 'boolean'})
	populate_combo.append(
	    	{'label': 'Created By', 'columnName': 'createdby', 'dataType': 'varchar'})
	populate_combo.append(
	    	{'label': 'Created Date', 'columnName': 'createddate', 'dataType': 'datetime'})
	return render(request, 'app/Transactions/NA_F_Goods_Outwards.html', {'populateColumn': populate_combo, 'CompanyName': 'Nufarm', 'title': 'Goods Outwards'})
