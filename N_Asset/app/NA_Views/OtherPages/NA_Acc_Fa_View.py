import json
import datetime
from decimal import Decimal
from django import forms
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from celery.decorators import task

from NA_Models.models import NAAccFa, goods
from NA_DataLayer.common import CriteriaSearch, ResolveCriteria, commonFunct, Data




def NA_AccGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey = request.GET.get('valueKey')
    IdataType = request.GET.get('dataType')
    Icriteria = request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    getColumn = commonFunct.retriveColumn(
        table=[NAAccFa, goods], resolve=IcolumnName, initial_name=['ac', 'g'])
    criteria = ResolveCriteria.getCriteriaSearch(str(Icriteria))
    dataType = ResolveCriteria.getDataType(str(IdataType))
    is_parent = request.GET.get('is_parent')
    serial_number = request.GET.get('serialnumber')
    accData = NAAccFa.objects.PopulateQuery(
        columnKey=getColumn,
        is_parent=int(is_parent),
        serialnumber=serial_number,
        ValueKey=IvalueKey,
        criteria=criteria,
        typeofData=dataType,
        sidx=Isidx,
        sord=Isord
    )
    paginator = Paginator(accData, Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    totalRecord = len(accData)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i += 1
        datarow = {
            "id": row['idapp'],
            "cell": [
                row['idapp'], i, row['itemcode'], row['goods'], row['serialnumber'],
                row['startdate'], row['year'], row['datedepreciation'],
                row['depreciationmethod'], row['depr_expense'],
                row['depr_accumulation'], row['bookvalue'], row['createddate'], row['createdby']
            ]
        }
        rows.append(datarow)
    results = {"page": dataRows.number, "total": paginator.num_pages,
               "records": totalRecord, "rows": rows}
    return HttpResponse(json.dumps(results, indent=4, cls=DjangoJSONEncoder), content_type='application/json')


class NA_Acc_Form(forms.Form):
    idapp_detail_receive = forms.CharField()


def NA_Acc_FA(request):
    return render(request, 'app/MasterData/NA_F_Acc_FA.html')


def EntryAcc(request):
    if request.method == 'POST':
        form = NA_Acc_Form(request.POST)
        if form.is_valid():
            idapp_detail_receive = form.cleaned_data.get('idapp_detail_receive')
            if request.POST['mode'] == 'Add':
                idapp = idapp_detail_receive.split(',')
                result = generate_acc_fa(
                    request=request,
                    idapp=idapp
                )
                return commonFunct.response_default(result)
        else:
            raise forms.ValidationError(form.errors)


@task(name='generate_fix_asset')
def generate_acc_fa(request, idapp):
    sid = transaction.savepoint()
    try:
        data_arr = NAAccFa.objects.searchAcc_ByForm(idapp=idapp)
        createdby = str(request.user.username)
        for data in data_arr:
            fk_goods = data['fk_goods']
            startdate = data['startdate'].strftime('%Y-%m-%d')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            price = data['priceperunit']
            depr_method = data['depreciationmethod']
            economiclife = data['economiclife']
            values_insert = []

            def settings_generate(opt):
                settings = {
                    'month_of': opt['month_of'],
                    'economiclife': economiclife,
                    'typeApp': data['typeapp'],
                    'serialNumber': data['serialnumber'],
                    'price': price,
                    'depr_method': depr_method,
                    'depr_expense': opt['depr_Expense'],
                    'startdate': startdate,
                    'fk_goods': data['fk_goods'],
                    'createddate': now,
                    'createdby': createdby
                }
                if opt['depr_method'] == 'STYD':
                    settings['depr_acc'] = opt['depr_acc']
                return settings

            if depr_method == 'SL' or depr_method == 'DDB':
                depr_expense = price / (economiclife * 12)
                for i in range(int(economiclife * 12) + 1):
                    generate_acc(settings_generate({
                        'depr_method': depr_method,
                        'month_of': i,
                        'depr_Expense': depr_expense
                    }), values_insert)
            elif depr_method == 'STYD':
                arr_year = [i for i in range(int(economiclife), 0, -1)]
                total_year = 0
                for i in arr_year:
                    total_year += i
                arr_depr_expense = [int(i / total_year * int(price))
                                    for i in arr_year]  # per tahun
                depr_acc = 0
                month_of = 0
                generate_acc(settings_generate({
                    'depr_method': 'STYD',
                    'depr_acc': Decimal('0.00'),
                    'depr_Expense': Decimal(arr_depr_expense[0] / 12),
                    'month_of': 0
                }), values_insert)
                for i in arr_depr_expense:
                    for j in range(1, 13):
                        depr_acc += Decimal(i / 12)
                        month_of += 1
                        generate_acc(settings_generate({
                            'depr_method': 'STYD',
                            'depr_acc': depr_acc,
                            'depr_Expense': Decimal(i / 12),
                            'month_of': month_of
                        }), values_insert)
            str_values = ','.join(values_insert)
            NAAccFa.objects.create_acc_FA(str_values)

    except Exception as e:
        transaction.savepoint_rollback(sid)
        return (e,)
    else:
        return (Data.Success,)

def ShowCustomFilter(request):
    if request.is_ajax():
        cols = []
        cols.append({'name': 'goodsname', 'value': 'goodsname',
                     'selected': 'True', 'dataType': 'varchar', 'text': 'Goods Name'})
        cols.append({'name': 'brandname', 'value': 'brandname',
                     'selected': '', 'dataType': 'varchar', 'text': 'Brand Name'})
        cols.append({'name': 'itemcode', 'value': 'itemcode',
                     'selected': '', 'dataType': 'varchar', 'text': 'Item code'})
        cols.append({'name': 'serialnumber', 'value': 'serialnumber',
                     'selected': '', 'dataType': 'varchar', 'text': 'Serial Number'})
        cols.append({'name': 'year', 'value': 'year',
                     'selected': '', 'dataType': 'decimal', 'text': 'Year'})
        cols.append({'name': 'startdate', 'value': 'startdate',
                     'selected': '', 'dataType': 'varchar', 'text': 'Start Date'})
        cols.append({'name': 'depr_expense', 'value': 'depr_expense',
                     'selected': '', 'dataType': 'decimal', 'text': 'Depreciation Expense'})
        cols.append({'name': 'depr_accumulation', 'value': 'depr_accumulation',
                     'selected': '', 'dataType': 'decimal', 'text': 'Depreciation Accumulation'})
        cols.append({'name': 'bookvalue', 'value': 'bookvalue',
                     'selected': '', 'dataType': 'decimal', 'text': 'Book Value'})
        return render(request, 'app/UserControl/customFilter.html', {'cols': cols})


def generate_acc(acc, values_insert):
    month_of = acc['month_of']
    price = acc['price']
    typeApp = acc['typeApp']
    serialNumber = acc['serialNumber']
    depr_method = acc['depr_method']
    startdate = acc['startdate']
    date_depr = lambda year: datetime.datetime.strptime(
        startdate, '%Y-%m-%d'
    ).date() + datetime.timedelta(
        days=(float(year) * 365)
    )
    depr_expense = Decimal(acc['depr_expense'])
    economiclife = acc['economiclife']
    if month_of == 0:
        if depr_method == 'DDB':
            depr_expense = depr_expense * 2
        date_depr = date_depr(economiclife)
        str_values = [
            '("' + str(acc['fk_goods']),
            str(serialNumber),
            str(typeApp),
            str(economiclife),
            date_depr.strftime('%Y-%m-%d'),
            str(startdate),
            str(depr_expense),
            '0.00',
            str('%0.2f' % price),
            '1',  # is_parent
            acc['createddate'],
            acc['createdby'] + '")'
        ]
    else:
        total_rows = int(economiclife * 12)
        if depr_method == 'SL' or depr_method == 'DDB':
            # if depr_method == 'SL':
            if depr_method == 'DDB':
                depr_expense = depr_expense * 2
                #depr_accumulation = 2*(depr_expense*month_of)
            depr_accumulation = depr_expense * month_of
        elif depr_method == 'STYD':
            depr_accumulation = acc['depr_acc']
        residue_eccLife = economiclife * (total_rows - month_of) / total_rows
        if residue_eccLife == 0:
            bookvalue = 0
            depr_accumulation = price
        else:
            if depr_accumulation > price:
                depr_accumulation = price
            bookvalue = price - depr_accumulation
        date_depr = date_depr(residue_eccLife)
        str_values = [
            '("' + str(acc['fk_goods']),
            str(serialNumber), str(typeApp),
            str('%0.2f' % residue_eccLife),
            date_depr.strftime('%Y-%m-%d'),
            str(startdate),
            str('%0.2f' % depr_expense),
            str('%0.2f' % depr_accumulation),
            str('%0.2f' % bookvalue),
            '0',  # is_parent
            acc['createddate'],
            acc['createdby'] + '")'
        ]
    str_values = '","'.join(str_values)
    return values_insert.insert(0, str_values)


def getGoods_data(request):
    if request.is_ajax() and request.method == 'GET':
        idapp = request.GET['idapp']
        goods_obj = NAAccFa.objects.getGoods_data(idapp)[0]

        def depr_method(dm):
            return 'Straight Line Method' if dm == 'SL'\
            else('Double Declining Balance' if dm == 'DDB' else 'Sum of The Year Digit')
        goods_obj['startdate'] = goods_obj['startdate'].strftime('%d/%m/%Y')
        goods_obj['enddate'] = goods_obj['enddate'].strftime('%d/%m/%Y')
        goods_obj['depr_method'] = depr_method(goods_obj['depr_method'])
        return HttpResponse(json.dumps(goods_obj, cls=DjangoJSONEncoder), content_type='application/json')


def SearchGoodsbyForm(request):
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    goodsFilter = request.GET.get('goods_filter')
    Ilimit = request.GET.get('rows', '')
    try:
        NAData = NAAccFa.objects.searchAcc_ByForm(q=goodsFilter)
        if NAData == []:
            results = {"page": "1", "total": 0, "records": 0, "rows": []}
            return HttpResponse(
                json.dumps(results, indent=4, cls=DjangoJSONEncoder),
                content_type='application/json'
            )
        else:
            totalRecord = len(NAData)
            paginator = Paginator(NAData, int(Ilimit))
            page = request.GET.get('page', '1')
            dataRows = paginator.page(page)
    except (EmptyPage, InvalidPage):
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0  # idapp,itemcode,goods
    for row in dataRows.object_list:
        i += 1
        datarow = {
            "id": str(row['idapp']) + '_fk_goods', "cell": [
                row['idapp'], i, row['itemcode'], row['goods'], row['serialnumber'],
                row['priceperunit'], row['economiclife'], row['depreciationmethod'],
                row['startdate'], row['startdate'] + datetime.timedelta(
                    days=(float(row['economiclife']) * 365)
                ), row['idapp_detail_receive']
            ]
        }
        rows.append(datarow)
    results = {
        "page": page, "total": paginator.num_pages, "records": totalRecord, "rows": rows
    }
    return HttpResponse(
        json.dumps(results, indent=4, cls=DjangoJSONEncoder),
        content_type='application/json'
    )
