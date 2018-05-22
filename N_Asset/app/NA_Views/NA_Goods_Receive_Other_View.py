from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator,EmptyPage
from django.shortcuts import render
from NA_DataLayer.common import ResolveCriteria,commonFunct
from NA_Models.models import NAGoodsReceive_other,goods,NASuplier


def NA_Goods_Receive_other(request):
    return render(request,'Transactions/NA_F_Goods_Receive_other.html')

def NA_Goods_Receive_otherGetData(request):
    IcolumnName = request.GET.get('columnName')
    IvalueKey =  request.GET.get('valueKey')
    IdataType =  request.GET.get('dataType')
    Icriteria =  request.GET.get('criteria')
    Ilimit = request.GET.get('rows', '')
    Isidx = request.GET.get('sidx', '')
    Isord = request.GET.get('sord', '')
    Ipage = request.GET.get('page')
    criteria = ResolveCriteria.getCriteriaSearch(Icriteria)
    dataType = ResolveCriteria.getDataType(IdataType)
    getColumn = commonFunct.retriveColumn(
        table=[NAGoodsReceive_other,goods],
        resolve=IcolumnName,
        initial_name=['ngr','g','emp1','emp2','sp'],
        custom_fields=[['receivedby'],['pr_by'],['supliername']]
    )
    maintenanceData = NAGoodsReceive_other.objects.PopulateQuery(getColumn,IvalueKey,criteria,dataType)
    totalRecords = len(maintenanceData)
    paginator = Paginator(maintenanceData,Ilimit)
    try:
        dataRows = paginator.page(Ipage)
    except EmptyPage:
        dataRows = paginator.page(paginator.num_pages)
    rows = []
    i = 0
    for row in dataRows.object_list:
        i+=1
        datarow = {
            "id" :row['idapp'], "cell" :[
                row['idapp'],i,row['goods'],row['serialnumber'],row['fromemployee'],row['usedemployee'],row['datereturn'],
                row['conditions'],row['minusDesc'],row['iscompleted'],row['descriptions'],row['createddate'],row['createdby']
                ]
            }
        rows.append(datarow)
    results = {"page": Ipage,"total": paginator.num_pages ,"records": totalRecords,"rows": rows }
    return HttpResponse(json.dumps(results,cls=DjangoJSONEncoder),content_type='application/json')