from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsLending
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
#from NA_DataLayer.jqgrid import JqGrid
from django.conf import settings 
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
def NA_Goods_Outwards(request):
    populate_combo = []
    #jieun heula query
    return render(request,'app/Transactions/NA_F_Goods_Outwards.html',{'populateColumn':populate_combo})