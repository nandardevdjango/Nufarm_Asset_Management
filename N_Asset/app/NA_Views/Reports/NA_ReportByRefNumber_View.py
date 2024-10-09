from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsReceive
from NA_DataLayer.common import CriteriaSearch
from NA_DataLayer.common import ResolveCriteria
from NA_DataLayer.common import StatusForm
from NA_DataLayer.common import commonFunct
from NA_DataLayer.common import decorators
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import ensure_csrf_cookie
from decimal import Decimal
import math

#no,refno, descr_purchase(Laptop /tgl diterima / dari supplier /total di beli),territory,goodstype,serialnumber,datereleased,for_employee,mobile


def NA_Report_ByRefNumber(request):
    populate_combo = []
    populate_combo.append(
        {'label': 'Reference Number', 'columnName': 'REFNO', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Goods Name', 'columnName': 'goods', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Supplier Name', 'columnName': 'suppliername', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Territory', 'columnName': 'territory', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Goods Type', 'columnName': 'typeapp', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Serial Number', 'columnName': 'serialnumber', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Date Released', 'columnName': 'datereleased', 'dataType': 'datetime'})
    populate_combo.append(
        {'label': 'For Employee', 'columnName': 'for_employee', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'mobile', 'columnName': 'mobile', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Reference goods from', 'dataType': 'varchar', })
    return render(request, 'app/Reports/NA_Report_ByRefNumber.html', {'populateColumn': populate_combo, 'CompanyName': 'Nufarm', 'title': 'Report by RefNo'})


def ShowCustomFilter(request):
    cols = []
    cols.append({'name': 'REFNO', 'value': 'REFNO', 'selected': 'True',
                 'dataType': 'varchar', 'text': 'Reference Number'})
    cols.append({'name': 'goods', 'value': 'goods', 'selected': '',
                 'dataType': 'varchar', 'text': 'Goods name'})
    cols.append({'name': 'suppliername', 'value': 'suppliername',
                 'selected': '', 'dataType': 'varchar', 'text': 'Supplier Name'})
    cols.append({'name': 'territory', 'value': 'territory',
                 'selected': '', 'dataType': 'varchar', 'text': 'Territory'})
    cols.append({'name': 'goodstype', 'value': 'goodstype',
                 'selected': '', 'dataType': 'varchar', 'text': 'Type Or Model'})
    cols.append({'name': 'serialnumber', 'value': 'serialnumber',
                 'selected': '', 'dataType': 'varchar', 'text': 'Serial Number'})
    cols.append({'name': 'datereleased', 'value': 'datereleased',
                 'selected': '', 'dataType': 'datetime', 'text': 'Date Released'})
    cols.append({'name': 'for_employee', 'value': 'for_employee',
                 'selected': '', 'dataType': 'varchar', 'text': 'For Employee'})
    cols.append({'name': 'mobile', 'value': 'mobile',
                 'selected': '', 'dataType': 'varchar', 'text': 'Mobile Phone'})
    cols.append({'name': 'refgoodsfrom', 'value': 'refgoodsfrom',
                 'selected': '', 'dataType': 'varchar', 'text': 'Reference goods from'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols, 'CompanyName': 'Nufarm', 'title': 'Report by RefNumber'})


def NA_Report_ByRefNumber_Search(request):
    try:
        IcolumnName = request.GET.get('columnName')
        IvalueKey = request.GET.get('valueKey')
        IdataType = request.GET.get('dataType')
        Icriteria = request.GET.get('criteria')
        Ilimit = request.GET.get('rows', '')
        Isidx = request.GET.get('sidx', '')
        Isord = request.GET.get('sord', '')
        criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
        dataType = ResolveCriteria.getDataType(str(IdataType))
        NAData = []
        if(Isord is not None and str(Isord) != '') or (Isidx is not None and str(Isidx) != ''):
            NAData = NAGoodsReceive.objects.getreport_byrecipient(str(Isidx), Isord, Ilimit, request.GET.get(
                'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
        else:
            NAData = NAGoodsReceive.objects.getreport_byrecipient('', 'DESC', Ilimit, request.GET.get(
                'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
        totalRecord = NAData[1]
        dataRows = NAData[0]
        rows = []
        i = 0
#REFNO,goods,descr_purchase,territory,for_employee,mobile,goodstype,serialnumber,datereleased,refgoodsfrom
        for row in dataRows:
            i = i+1
            datarow = {"id": i, 'cell': [i, row['REFNO'], row['goods'], row['descr_purchase'], row['territory'], row['for_employee'],
                                         row['mobile'], row['goodstype'], row['serialnumber'], row['datereleased'],
                                         row['refgoodsfrom'], row['last_possition']]}
            rows.append(datarow)
        TotalPage = 1 if totalRecord < int(Ilimit) else (
            math.ceil(float(totalRecord/int(Ilimit))))  # round up to next number
        results = {"page": int(request.GET.get(
            'page', '1')), "total": TotalPage, "records": totalRecord, "rows": rows}
        return HttpResponse(json.dumps(results, indent=4, cls=DjangoJSONEncoder), content_type='application/json')
    except Exception as e:
        result = repr(e)
        return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')


def export_to_excels(request):
    	#get qryset
	NAData = []
	#tentukan column
 #REFNO,goods,descr_purchase,territory,for_employee,mobile,goodstype,serialnumber,datereleased,refgoodsfrom
	colNames = ['NO', 'Reference Number', 'Goods Name', 'Purchase Descriptions', 'User Territory', 'For Employee', 'mobile', 'Goods Type',
             'Serial Number', 'Date Released', 'Reference Goods From', 'Last Possition']
	try:
		IcolumnName = request.GET.get('columnName')
		IvalueKey = request.GET.get('valueKey')
		IdataType = request.GET.get('dataType')
		Icriteria = request.GET.get('criteria')
		Ilimit = request.GET.get('rows', '')
		Isidx = request.GET.get('sidx', '')
		Isord = request.GET.get('sord', '')
		criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
		dataType = ResolveCriteria.getDataType(str(IdataType))
		if(Isord is not None and str(Isord) != '') or(Isidx is not None and str(Isidx) != ''):
			NAData = NAGoodsReceive.objects.getreport_byrecipient(str(Isidx), Isord, Ilimit, request.GET.get('page', '1'), request.user.username if (
			    request.user.username is not None and request.user.username != '') else 'Admin', IcolumnName, IvalueKey, criteria, dataType)  # return tuples
		else:
			NAData = NAGoodsReceive.objects.getreport_byrecipient('', 'DESC', Ilimit, request.GET.get('page', '1'), request.user.username if (
			    request.user.username is not None and request.user.username != '') else 'Admin', IcolumnName, IvalueKey, criteria, dataType)  # return tuples
		#totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
 #REFNO,goods,descr_purchase,territory,for_employee,mobile,goodstype,serialnumber,datereleased,refgoodsfrom
		i = 0
		for row in dataRows:
			i = i + 1
			datarow = tuple([i, row['REFNO'], row['goods'], row['descr_purchase'], row['territory'], row['for_employee'], row['mobile'], row['goodstype'], row['serialnumber'], datetime.strftime(row['datereleased'], "%m/%d/%Y"),
                            row['refgoodsfrom'], row['last_possition']])
			rows.append(datarow)
		dataRows = list(dict(zip(colNames, row)) for row in rows)
		column_hidden = []
		response = commonFunct.create_excel(
			colNames, column_hidden, dataRows, 'ReportByReRefNumber_' + datetime.strftime(datetime.now(), "%Y_%m_%d"), 'Report_By_Reference_Number')
		return response
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')
