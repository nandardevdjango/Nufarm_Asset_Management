from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.utils.dateformat import DateFormat
from NA_Models.models import NAGoodsOutwards
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


def NA_Report_ByRecipient(request):
    populate_combo = []
    populate_combo.append(
        {'label': 'Goods Name', 'columnName': 'goods', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Goods Type', 'columnName': 'typeapp', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Serial Number', 'columnName': 'serialnumber', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'For Employee', 'columnName': 'for_employee', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Territory', 'columnName': 'territory', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Date Released', 'columnName': 'datereleased', 'dataType': 'datetime'})
    populate_combo.append(
        {'label': 'Sender ', 'columnName': 'senderby', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Goods From', 'columnName': 'refgoodsfrom', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'GoodNew', 'columnName': 'isGoodNew', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Created By', 'columnName': 'createdby', 'dataType': 'varchar'})
    populate_combo.append(
        {'label': 'Created Date', 'columnName': 'createddate', 'dataType': 'datetime'})
    return render(request, 'app/Reports/NA_Report_ByRecipient.html', {'populateColumn': populate_combo, 'CompanyName': 'Nufarm', 'title': 'Report by Recipient'})


def ShowCustomFilter(request):
    cols = []
    cols.append({'name': 'goods', 'value': 'goods', 'selected': 'True',
                 'dataType': 'varchar', 'text': 'Goods name'})
    cols.append({'name': 'typeapp', 'value': 'typeapp',
                 'selected': '', 'dataType': 'varchar', 'text': 'Goods type'})
    cols.append({'name': 'serialnumber', 'value': 'serialnumber',
                 'selected': '', 'dataType': 'varchar', 'text': 'Serial Number'})
    cols.append({'name': 'daterequest', 'value': 'daterequest',
                 'selected': '', 'dataType': 'datetime', 'text': 'Date Requested'})
    cols.append({'name': 'datereleased', 'value': 'datereleased',
                 'selected': '', 'dataType': 'datetime', 'text': 'Date Released'})
    cols.append({'name': 'for_employee', 'value': 'for_employee',
                 'selected': '', 'dataType': 'varchar', 'text': 'For Employee'})
    cols.append({'name': 'mobile', 'value': 'mobile',
                 'selected': '', 'dataType': 'varchar', 'text': 'Mobile Phone'})
    cols.append({'name': 'territory', 'value': 'territory',
                 'selected': '', 'dataType': 'varchar', 'text': 'Territory'})
    cols.append({'name': 'responsibleby', 'value': 'responsibleby',
                 'selected': '', 'dataType': 'varchar', 'text': 'Responsible by'})
    cols.append({'name': 'senderby', 'value': 'senderby', 'selected': '',
                 'dataType': 'varchar', 'text': 'Sent  By'})
    cols.append({'name': 'isGoodNew', 'value': 'isGoodNew', 'selected': '',
                 'dataType': 'boolean', 'text': 'Good New'})
    cols.append({'name': 'refgoodsfrom', 'value': 'refgoodsfrom',
                 'selected': '', 'dataType': 'varchar', 'text': 'Reference goods from'})
    cols.append({'name': 'descriptions', 'value': 'descriptions',
                 'selected': '', 'dataType': 'varchar', 'text': 'descriptions/Remark'})
    cols.append({'name': 'createdby', 'value': 'createdby',
                 'selected': '', 'dataType': 'varchar', 'text': 'Created By'})
    cols.append({'name': 'createddate', 'value': 'createddate',
                 'selected': '', 'dataType': 'datetime', 'text': 'Created Date'})
    return render(request, 'app/UserControl/customFilter.html', {'cols': cols, 'CompanyName': 'Nufarm', 'title': 'Report by Recipient'})


def NA_Report_ByRecipient_Search(request):
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
            NAData = NAGoodsOutwards.objects.getreport_byrecipient(str(Isidx), Isord, Ilimit, request.GET.get(
                'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
        else:
            NAData = NAGoodsOutwards.objects.getreport_byrecipient('', 'DESC', Ilimit, request.GET.get(
                'page', '1'), request.user.username, IcolumnName, IvalueKey, criteria, dataType)  # return tuples
        totalRecord = NAData[1]
        dataRows = NAData[0]
        rows = []
        #column idapp,goods,goodstype,serialnumber,daterequest,datereleased,isnew,fk_employee,for_employee,fk_usedemployee,eks_employee,
        #fk_responsibleperson,responsible_by,fk_sender,senderby,fk_stock,refgoodsfrom,descriptions,createdby,createddate

        #no,territory,goods,typeapp,serialnumber,for_employee,datereleased,isnew,mobile,eks_employee,senderby,refgoodsfrom,equipment_desc,descriptions,createdby,createddate
        i = 0
        for row in dataRows:
            i = i+1
            datarow = {"id": i, 'cell': [i, row['territory'], row['goods'], row['goodstype'], row['serialnumber'], row['datereleased'],
                                         1 if row['isGoodNew'] == 'YESS' else 0, row['for_employee'], row['mobile'], row['eks_employee'],  row['refgoodsfrom'], row['equipment_desc'], row['descriptions'], row['createddate'], row['createdby']]}
            #datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
            #	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
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
	colNames = ['NO', 'Territory', 'Goods Name', 'Type', 'Serial Number', 'Date Released', 'Is New', 'For Employee', 'mobile',
             'Eks Employee', 'Ref Goods From', 'Equipment', 'Descriptions', 'Created Date', 'Created By']
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
			NAData = NAGoodsOutwards.objects.getreport_byrecipient(str(Isidx), Isord, Ilimit, request.GET.get('page', '1'), request.user.username if (
			    request.user.username is not None and request.user.username != '') else 'Admin', IcolumnName, IvalueKey, criteria, dataType)  # return tuples
		else:
			NAData = NAGoodsOutwards.objects.getreport_byrecipient('', 'DESC', Ilimit, request.GET.get('page', '1'), request.user.username if (
			    request.user.username is not None and request.user.username != '') else 'Admin', IcolumnName, IvalueKey, criteria, dataType)  # return tuples
		#totalRecord = NAData[1]
		dataRows = NAData[0]
		rows = []
        #territory,goods,FK_Goods_Outwards,FK_goods,goodstype,serialnumber,datereleased,
        # isGoodNew,fk_employee,for_employee,mobile,eks_employee,refgoodsfrom,createdby,createddate,equipment_desc,descriptions
		i = 0
		for row in dataRows:
			i = i + 1
			datarow = tuple([i, row['territory'], row['goods'], row['goodstype'], row['serialnumber'], datetime.strftime(row['datereleased'], "%m/%d/%Y"),
                            row['isGoodNew'], row['for_employee'], row['mobile'], row['eks_employee'],
                            row['refgoodsfrom'], row['equipment_desc'], row['descriptions'], datetime.strftime(row['createddate'], "%m/%d/%Y"), row['createdby']])
			#datarow = {"id" :row.idapp, "cell" :[row.idapp,row.itemcode,row.goodsname,row.brandname,row.unit,row.priceperunit, \
			#	row.placement,row.depreciationmethod,row.economiclife,row.createddate,row.createdby]}
			rows.append(datarow)
		dataRows = list(dict(zip(colNames, row)) for row in rows)
		column_hidden = ["fk_employee", "FK_Goods_Outwards", "FK_Goods_Outwards"]
		response = commonFunct.create_excel(
			colNames, column_hidden, dataRows, 'ReportByRecipient_' + datetime.strftime(datetime.now(), "%Y_%m_%d"), 'Report By goods Recipient')
		return response
	except Exception as e:
		result = repr(e)
		return HttpResponse(json.dumps({'message': result}), status=500, content_type='application/json')
