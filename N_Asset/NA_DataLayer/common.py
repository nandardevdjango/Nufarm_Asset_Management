import errno
import json
import re
from datetime import datetime
from enum import Enum
from functools import wraps
from os import path, makedirs, remove

from dateutil.parser import parse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect


class CriteriaSearch(Enum):
    Equal = 1
    BeginWith = 2
    EndWith = 3
    NotEqual = 4
    Greater = 5
    Less = 6
    LessOrEqual = 7
    GreaterOrEqual = 8
    Like = 9
    In = 10
    NotIn = 11
    Beetween = 12


class StatusForm(Enum):
    Input = 1
    Edit = 2
    InputOrEdit = 3
    View = 4


class DataType(Enum):
    BigInt = 1
    Boolean = 2
    Char = 3
    DateTime = 4
    Decimal = 5
    Float = 6
    Image = 7
    Integer = 8
    Money = 9
    NChar = 10
    NVarChar = 11
    VarChar = 12
    Variant = 13


class Data(Enum):
    Success = 1
    Exists = 2
    Lost = 3
    HasRef = 4
    Empty = 5
    Changed = 6
    ValidationError = 7


class Message(Enum):
    Success = '__success'
    Exists = '__exists'
    Lost = '__lost'
    HasRef_del = '__hasref_del'
    HasRef_edit = '__hasref_edit'
    Empty = '__empty'
    Changed = '__changed'

    @staticmethod
    def get_specific_exists(table, column, data):
        """
        param:
        return message existed data : e.g (Supplier with suppliercode 0012a has existed)
        """
        return '{0} with {1} {2} has existed'.format(table, column, data)

    @classmethod
    def get_time_info(cls, times):
        """
        function get time
        param:
        must instance of datetime
        return (tuple): {digits} {unit} e.g : 1 minute, 2 minutes
        """
        diff = (datetime.now() - times).seconds
        unit = 'seconds'
        result = diff
        if diff >= 60:
            result = result / 60
            unit = 'minute'
            if diff >= 120:
                unit = 'minutes'
        elif diff >= 3600:
            result = result / 3600
            unit = 'hour'
            if diff >= 7200:
                unit = 'hours'
        return (int(result), unit)

    @classmethod
    def get_lost_info(cls, **kwargs):
        """
        get lost info, 
        param:
        pk(Primary Key):idapp or suppliercode
        table:table_name
        """
        obj = commonFunct.get_log_data(
            pk=kwargs['pk'], table=kwargs['table'], action='deleted')
        if obj == []:
            return 'This data doesn\'t lost'
        else:
            obj = obj[0]
            result, unit = cls.get_time_info(obj['createddate'])
            return 'This data has lost or deleted by other user, {0} {1} ago'.format(result, unit)

    @classmethod
    def get_exists_info(cls, createddate):
        """
        function return exists info
        params:
        must instance of datetime
        createddate:from each table
        """
        result, unit = cls.get_time_info(createddate)
        return 'This data has exists or created by other user, {0} {1} ago'.format(result, unit)

    @classmethod
    def has_update_by_other(cls, **kwargs):
        """
        use it , if other user want to edit data .. but the data
        has updated by other user
        param:
        pk(Primary Key):idapp or suppliercode
        table:table_name
        """
        obj = commonFunct.get_log_data(
            pk=kwargs['pk'], table=kwargs['table'], action='updated')
        if obj == []:
            return None
        else:
            obj = obj[0]
            result, unit = cls.get_time_info(obj['createddate'])
            return 'This data has changed or updated by other user, {0} {1}'.format(result, unit)


class ResolveCriteria:
    __query = ""

    def __init__(self, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar, columnKey='', value=None):
        self.criteria = criteria
        self.typeofData = typeofData
        self.valueData = value
        self.colKey = columnKey

    def DefaultModel(self):
        filterfield = self.colKey + '__istarswith'
        if self.criteria == CriteriaSearch.Beetween:
            if self.typeofData == DataType.Boolean or self.typeofData == DataType.Char or self.typeofData == DataType.NChar or self.typeofData == DataType.NVarChar \
                    or self.typeofData == DataType.VarChar:
                raise ValueError('value type is in valid')
            if self.typeofData == DataType.DateTime:
                if ',' in str(self.valueData):
                    strValueKeys = str(self.valueData).split(',')
                    filterfield = self.colKey + '__range'
                    startDate = datetime.strptime(self.valueData[0], 'Y-m-d')
                    # StartDateRange = (  # The start_date with the minimum possible time
                    #datetime.combine(startDate, datetime.min.time()),
                    # The start_date with the maximum possible time
                    #datetime.combine(StatDateRange, datetime.max.time())
                    # )
                    endDate = datetime.strptime(self.valueData[1], 'Y-m-d')
                    # endDateRange = (  # The start_date with the minimum possible time
                    #datetime.combine(endDate, datetime.min.time()),
                    # The start_date with the maximum possible time
                    #datetime.combine(endDate, datetime.max.time())
                    # )
                    return {filterfield: [startDate, endDate]}
            elif self.typeofData == DataType.BigInt or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Integer or self.typeofData == DataType.Money:
                return {filterfield: [self.valueData[0], self.valueData[1]]}
            else:
                raise ValueError('value type is in valid')
        elif self.criteria == CriteriaSearch.BeginWith:
            if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                return {filterfield: self.valueData}
            else:
                raise ValueError('value type is in valid')
        elif self.criteria == CriteriaSearch.EndWith:
            if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                filterfield = self.colKey + '__iendswith'
            else:
                raise ValueError('value type is in valid')
            return {filterfield: self.valueData}

    def Sql(self):
        if self.criteria == CriteriaSearch.Beetween:
            if self.typeofData == DataType.Boolean or self.typeofData == DataType.Char or self.typeofData == DataType.NChar or self.typeofData == DataType.NVarChar \
                    or self.typeofData == DataType.VarChar:
                raise ValueError('value type is in valid')
            elif self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                values = str(self.valueData).split('-')
                val1 = values[0]
                val2 = ''
                ResolveCriteria.__query = " = " + str(val1)
                if len(values) > 1:
                    val2 = values[1]
                    ResolveCriteria.__query = " BETWEEN " + \
                        str(val1) + " AND " + str(val2)
            if self.typeofData == DataType.DateTime:
                values = str(self.valueData).split('-')
                startDate = values[0]
                strstartDate = str(parse(startDate).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                endDate = strstartDate + " 23:59:59'"
                strEndDate = endDate
                ResolveCriteria.__query = " BETWEEN '" + \
                    strstartDate + "'" + " AND '" + strEndDate
                if len(values) > 1:
                    endDate = values[1]
                    strEndDate = str(parse(endDate).strftime(
                        "%Y-%m-%d"))  # jadinya string datetime
                    # str(parse(self.valueData).strftime("%Y-%m-%d"))#jadinya string datetime
                    ResolveCriteria.__query = """ >=  STR_TO_DATE('""" + strstartDate + """','%Y-%m-%d') AND  """ + \
                        self.colKey + \
                        """ <= STR_TO_DATE('""" + strEndDate + \
                        """','%Y-%m-%d')"""

        elif self.criteria == CriteriaSearch.BeginWith:
            ResolveCriteria.__query = " LIKE '{0!s}%'".format(
                str(self.valueData))
        elif self.criteria == CriteriaSearch.EndWith:
            ResolveCriteria.__query = " LIKE '%{0!s}'".format(
                str(self.valueData))
        elif self.criteria == CriteriaSearch.Equal:
            if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                ResolveCriteria.__query = " = '{0}'".format(self.valueData)
            elif self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                ResolveCriteria.__query = ' = {0}'.format(self.valueData)
            elif self.typeofData == DataType.DateTime:
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = " BETWEEN '" + strDate + \
                    "'" + " AND '" + strDate + " 23:59:59'"
            elif self.typeofData == DataType.Boolean:
                ResolveCriteria.__query = ' = {0}'.format(
                    1 if self.valueData == 1 or self.valueData == '1' or self.valueData == True or self.valueData == 'true' or self.valueData == 'True' else 0)
                #ResolveCriteria.__query = """ = STR_TO_DATE('""" + str(self.valueData) + """','%Y-%m-%d')"""
        elif self.criteria == CriteriaSearch.Greater:
            if self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                ResolveCriteria.__query = ' > {0}'.format(
                    float(self.valueData))
            elif self.typeofData == DataType.DateTime:
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = """ > STR_TO_DATE('""" + \
                    strDate + """','%Y-%m-%d')"""
        elif self.criteria == CriteriaSearch.GreaterOrEqual:
            if self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                ResolveCriteria.__query = ' > {0}'.format(
                    float(self.valueData))
            elif self.typeofData == DataType.DateTime:
                # format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = """ >= STR_TO_DATE('""" + \
                    strDate + """','%Y-%m-%d')"""
        elif self.criteria == CriteriaSearch.In:
            rowFilter = " IN('"
            if ',' in str(self.valueData):
                if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                    strValueKeys = str(self.valueData).split(',')
                    for i in range(len(strValueKeys)):
                        rowFilter += strValueKeys[i] + "'"
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                    ResolveCriteria.__query = rowFilter
                elif self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                        or self.typeofData == DataType.BigInt:
                    rowFilter = " IN("
                    strValueKeys = str(self.valueData).split(',')
                    for i in range(len(strValueKeys)):
                        rowFilter += strValueKeys[i] + ""
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                elif self.typeofData == DataType.DateTime:
                    rowFilter = " IN("
                    strValueKeys = str(self.valueData).split(',')
                    for i in range(len(strValueKeys)):
                        strDate = str(parse(strValueKeys[i]).strftime(
                            "%Y-%m-%d"))  # jadinya string datetime
                        rowFilter += """STR_TO_DATE('""" + \
                            strDate + """','%Y-%m-%d')"""
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                    ResolveCriteria.__query = rowFilter
            elif self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                ResolveCriteria.__query = " IN ('{0!s}')".format(
                    str(self.valueData))
            elif self.typeofData == DataType.DateTime:
                # format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses
                ResolveCriteria.__query = parse(
                    self.valueData).strftime("""' IN('%Y-%m-%d')""")
        elif self.criteria == CriteriaSearch.NotIn:
            rowFilter = " NOT IN('"
            if ',' in str(self.valueData):
                if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                    strValueKeys = str(self.valueData).split(',')
                    for i in range(len(strValueKeys)):
                        rowFilter += strValueKeys[i] + "'"
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                    ResolveCriteria.__query = rowFilter
                elif self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                        or self.typeofData == DataType.BigInt:
                    rowFilter = " NOT IN("
                    strValueKeys = str(self.valueData).split(',')
                    for i in range(len(strValueKeys)):
                        rowFilter += strValueKeys[i] + ""
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                elif self.typeofData == DataType.DateTime:
                    rowFilter = """ NOT IN("""
                    strValueKeys = str(self.valueData).split(',')

                    for i in range(len(strValueKeys)):
                            #"""STR_TO_DATE('""" + strValueKeys + """','%Y-%m-%d')"""
                        strDate = str(parse(strValueKeys[i]).strftime(
                            "%Y-%m-%d"))  # jadinya string datetime
                        rowFilter += """STR_TO_DATE('""" + \
                            strDate + """','%Y-%m-%d')"""
                        if i < len(strValueKeys) - 1:
                            rowFilter += ","
                    rowFilter += ")"
                    ResolveCriteria.__query = rowFilter
            elif self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                ResolveCriteria.__query = " NOT IN ('{0!s}')".format(
                    str(self.valueData))
            elif self.typeofData == DataType.DateTime:
                # format data yang di masukan di valueData mesti dijadikan tahun-bulan-tanggal sebelum di proses
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = """ NOT IN(STR_TO_DATE('""" + \
                    strDate + """','%Y-%m-%d'))"""
        elif self.criteria == CriteriaSearch.Less:
            if self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                ResolveCriteria.__query = ' < {0}'.format(
                    float(self.valueData))
            elif self.typeofData == DataType.DateTime:
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = """ < STR_TO_DATE('""" + \
                    strDate + """','%Y-%m-%d')"""
        elif self.criteria == CriteriaSearch.LessOrEqual:
            if self.typeofData == DataType.Integer or self.typeofData == DataType.Decimal or self.typeofData == DataType.Float or self.typeofData == DataType.Money \
                    or self.typeofData == DataType.BigInt:
                ResolveCriteria.__query = ' <= {0}'.format(
                    float(self.valueData))
            elif self.typeofData == DataType.DateTime:
                strDate = str(parse(self.valueData).strftime(
                    "%Y-%m-%d"))  # jadinya string datetime
                ResolveCriteria.__query = """ <= STR_TO_DATE('""" + \
                    strDate + """','%Y-%m-%d')"""
                #ResolveCriteria.__query = ' <= {%Y-%m-%d}'.format(datetime((str(self.valueData)[0:3]),str(self.valueData)[5:6],str(self.valueData)[7:8]))
        elif self.criteria == CriteriaSearch.Like:
            ResolveCriteria.__query = " LIKE '%{0!s}%'".format(
                str(self.valueData))
        elif self.criteria == CriteriaSearch.NotEqual:
            if self.typeofData == DataType.Char or self.typeofData == DataType.VarChar or self.typeofData == DataType.NVarChar:
                ResolveCriteria.__query = " <> '{0}'".format(
                    str(self.valueData))
            elif self.typeofData == DataType.Integer:
                ResolveCriteria.__query = ' <> {0}'.format(self.valueData)
            elif self.typeofData == DataType.Boolean:
                ResolveCriteria.__query = ' <> {0}'.format(
                    1 if self.valueData == 1 or self.valueData == '1' or self.valueData == True or self.valueData == 'True' or self.valueData == 'true' else 0)
        return ResolveCriteria.__query

    def getDataType(strDataType):
        if strDataType == 'int':
            return DataType.Integer
        elif strDataType == 'varchar':
            return DataType.VarChar
        elif strDataType == 'bigint':
            return DataType.BigInt
        elif strDataType == 'boolean':
            return DataType.Boolean
        elif strDataType == 'char':
            return DataType.Char
        elif strDataType == 'datetime':
            return DataType.DateTime
        elif strDataType == 'decimal':
            return DataType.Decimal
        elif strDataType == 'float':
            return DataType.Float
        elif strDataType == 'image':
            return DataType.Image
        elif strDataType == 'money':
            return DataType.Money
        elif strDataType == 'nchar':
            return DataType.Char
        elif strDataType == 'nvarchar':
            return DataType.NVarChar
        else:
            return DataType.VarChar

    def getCriteriaSearch(strCriteria):
        if strCriteria == 'equal':
            return CriteriaSearch.Equal
        elif strCriteria == 'beginwith':
            return CriteriaSearch.BeginWith
        elif strCriteria == 'endwith':
            return CriteriaSearch.EndWith
        elif strCriteria == 'notequal':
            return CriteriaSearch.NotEqual
        elif strCriteria == 'greater':
            return CriteriaSearch.Greater
        elif strCriteria == 'less':
            return CriteriaSearch.Less
        elif strCriteria == 'lessorequal':
            return CriteriaSearch.LessOrEqual
        elif strCriteria == 'greaterorequal':
            return CriteriaSearch.GreaterOrEqual
        elif strCriteria == 'like':
            return CriteriaSearch.Like
        elif strCriteria == 'in':
            return CriteriaSearch.In
        elif strCriteria == 'notin':
            return CriteriaSearch.NotIn
        elif strCriteria == 'between':
            return CriteriaSearch.Beetween
        else:
            return CriteriaSearch.Like


class decorators:

    def ajax_required(func):
        """
        to ensure if request is ajax
        and request Header must set X-Requested-With : XMLHttpRequest
        """
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.is_ajax():
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied()
        return wrapper

    def detail_request_method(arguments):
        """
        usage @detail_request_method('POST')
        return status 405(Method not allowed) if request method did not same as your specific method
        """
        def real_decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                if arguments == 'POST':
                    if request.method == 'POST':
                        return func(request, *args, **kwargs)
                elif arguments == 'GET':
                    if request.method == 'GET':
                        return func(request, *args, **kwargs)
                return HttpResponse(
                    json.dumps({'message': 'Method Not Allowed'}),
                    status=405, content_type='application/json'
                )
            return wrapper
        return real_decorator

    def admin_required_action(arguments):
        """
        there are some actions that only the admin can do it
        usage @admin_required_action('Add')
        param/argument is only for message
        """
        def real_decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                if request.user.is_superuser:
                    return func(request, *args, **kwargs)
                else:
                    return HttpResponse(
                        json.dumps(
                            {'message': 'You don\'t have permission for %s this data' % arguments}
                        ),
                        status=403,
                        content_type='application/json'
                    )
            return wrapper
        return real_decorator

    def read_permission(form_name, action=None):
        """
        (backend security)
        to ensure if user who don't have permission
        cannot manipulate or access resource(url),
        if user is crazy.. they will be request manually to server.
        prevent it with this decorators
        """
        def real_decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                if request.method == 'POST':
                    user = request.user
                    permission_denied = commonFunct.permision_denied
                    if action:
                        _action = action
                    else:
                        _action = request.POST.get('statusForm') \
                            or request.POST.get('mode') \
                            or request.POST.get('status')
                    if _action == 'Open':
                        return HttpResponse('cannot edit data with status open', status=403)
                    masterdata_form = [
                        'employee', 'n_a_supplier', 'goods', 'n_a_privilege'
                    ]
                    transaction_form = ['n_a_goods_receive']
                    all_form = masterdata_form + transaction_form
                    form_action = ['Open', 'Add', 'Edit']
                    other_action = ['View', 'Delete']
                    all_action = form_action + other_action
                    if _action not in all_action:
                        raise ValueError(
                            'uncategorize cannot resolve %s action' % _action
                        )
                    if action == 'View':
                        _action = 'Allow View'
                    elif _action == 'Add':
                        _action = 'Allow Add'
                    elif _action == 'Edit':
                        _action = 'Allow Edit'
                    elif _action == 'Delete' or action == 'Delete':
                        _action = 'Allow Delete'
                    if not user.has_permission(_action, form_name):
                        return permission_denied()
                return func(request, *args, **kwargs)
            return wrapper
        return real_decorator

    def ensure_authorization(func):
        """
        to ensure if user is authorize/login ..
        if user have 2 tab in browser but in other tab he/she was logouted
        prevent it and show the dialog in browser to information if he/she
        was logouted and must be login again
        """
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                return func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    return HttpResponse(
                        json.dumps({'message': 'unauthorized'}),
                        status=401,  # 401 = unauthorized
                        content_type='application/json'
                    )
                else:
                    return redirect('/login/?next=' + request.get_full_path())
        return wrapper


class query:
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        fetchall = cursor.fetchall()
        if fetchall == ():
            return []  # don't loop if no result
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in fetchall
        ]
    
    def like(query_param, fields):
        query_string = ' LIKE {query_param} OR '.join(fields)
        query_string += ' LIKE {query_param}'
        query_string = query_string.format(
            query_param=('%(' + query_param + ')s')
        )
        return query_string


class commonFunct:
    def str2bool(v):
        if isinstance(v, int):
            v = str(v)
        v = v.lower()
        if v in ("yes", "true", "t", "1"):
            return True
        elif v in ("no", "false", "f", "0"):
            return False
        else:
            raise ValueError("Please enter correct value")

    # buat function yang bisa menghasilkan TIsNew,T_Goods_Receive,T_GoodsReturn,T_IsRenew,TIsUsed,TMaintenance,TotalSpare
    # untuk mendapatkan jumlah yang benar dengan barang yang masuk kategory bekas(used)
    # maka harus di cari dulu berapa yang bekasnya, bekas --->barang yang sudah masuk ke table goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost,maentenance

    # TIsNew diperoleh Total goods receive detail - Count (group by fk_goods(union goods_Outwards,goods_return,goods_lending, goods_disposal,goods_lost)
    # buat query union untuk mendapatkan barang mana saja yang sudah di pakai
    def getTotalGoods(FKGoods, cur, username, closeCursor=False):
        """FUNCTION untuk mengambil total-total data berdasarkan FK_goods yang di parameter, function ini akan mereturn value
        :param int FKGoods: idapp_fk_goods
        :param object cur: cursor active
        totalNew,totalReceived,totalUsed,totalReturn,totalRenew,totalMaintenance,TotalSpare dalam bentuk tuples
        totalNew adalah total barang yang baru yang belum pernah di pakai
        totalUsed adalah total barang yang sudah di keluarkan/terpakai
        totalReceived adalah total barang yang di terima
        totalReturn adalah total barang yang di kembalikan pakai query count distinct
        totalRenew adalah ketersedian barang yang sudah di maintain/perbaiki dan bisa di ambil untuk baik di pinjam atau inventaris
        totalMaintenance adalah total barang yang sedang di perbaiki
        totalSpare adalah total cadangan barang yang akan di pakai untuk peminjaman barang
        totalSpare akan terjadi bila ada transaksi di n_a_goods_lending dan status sudah R(returned)
        totalBroken akan terjadi  kondisi barang yang di kembalikan dari user rusak atau dari maintenance tidak bisa di perbaiki lagi
        totalDisposal total barang yang sudah di hapus
        totalLost total barang yang hilang
        """
        totalNew = 0
        totalUsed = 0
        totalReceived = 0
        totalReturn = 0
        totalRenew = 0
        totalMaintenance = 0
        totalSpare = 0
        totalBroken = 0
        totalLost = 0
        totalDisposal = 0
        GoodsCat = "IT"

        if(cur is None):
            cur = connection.cursor()
        #check apakah barang categorynya
        Query = """SELECT TypeApp FROM n_a_goods WHERE IDApp = %s"""
        cur.execute(Query,[FKGoods])
        row = cur.fetchone()
        if cur.rowcount <= 0:
            raise Exception('this goods is unknown category')
        GoodCat = str(row[0])

        Query = "DROP TEMPORARY TABLE IF EXISTS Temp_Goods_Used_" + username
        cur.execute(Query)

        if GoodCat == "IT":
            Query = """CREATE TEMPORARY TABLE Temp_Goods_Used_""" + username + """
                        (INDEX cmpd_key (SerialNumber, FK_Goods))ENGINE=MyISAM AS 
                        (SELECT FK_goods,TypeApp,SerialNumber FROM n_a_goods_outwards WHERE FK_goods = %(FK_Goods)s)
                        UNION 	
                        (SELECT FK_Goods,TypeApp,SerialNumber FROM n_a_goods_Lending WHERE FK_goods = %(FK_Goods)s)		
                        UNION 	
                        (SELECT FK_Goods,TypeApp,SerialNumber FROM n_a_goods_return WHERE FK_goods = %(FK_Goods)s)
                        UNION 	
                        (SELECT FK_Goods,TypeApp,SerialNumber FROM n_a_maintenance WHERE FK_goods = %(FK_Goods)s)	
                        UNION 	
                        (SELECT FK_Goods,TypeApp,SerialNumber FROM n_a_disposal WHERE FK_goods = %(FK_Goods)s ) """
        elif GoodCat == "GA":
            Query = """CREATE TEMPORARY TABLE Temp_Goods_Used_""" + username + """
                    (INDEX cmpd_key (SerialNumber, FK_Goods))ENGINE=MyISAM AS 
                    (SELECT gr.FK_Goods,gr.TypeApp,gr.Machine_No FROM n_a_ga_receive gr INNER JOIN n_a_ga_outwards go ON gr.IDApp = go.FK_Receive WHERE gr.FK_Goods = %(FK_Goods)s)"""
        elif GoodCat == "O":
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})

        # get totalused and totalReceived
        if GoodCat == "IT":
            Query = """SELECT Rec.Total AS TotalReceived,Rec.Total - IFNULL(T_Used.Total,0) AS TotalNew,IFNULL(T_Used.Total,0) AS TotalUsed FROM (SELECT ngr.FK_Goods,COUNT(ngr.FK_goods) AS Total FROM n_a_goods_receive ngr INNER JOIN n_a_goods_receive_detail ngd 
                        ON ngr.IDApp = ngd.FK_App WHERE ngr.FK_goods = %(FK_Goods)s GROUP BY ngr.FK_Goods)Rec LEFT OUTER JOIN (SELECT FK_Goods,COUNT(FK_Goods) AS Total FROM Temp_Goods_Used_""" + username + """ GROUP BY  FK_Goods)T_Used 
                        ON Rec.FK_Goods = T_Used.FK_Goods """
        elif(GoodCat == "GA"):
            Query = """SELECT Rec.Total AS TotalReceived,Rec.Total - IFNULL(T_Used.Total,0) AS TotalNew,IFNULL(T_Used.Total,0) AS TotalUsed FROM (SELECT FK_Goods,COUNT(FK_goods) AS Total FROM n_a_ga_receive WHERE FK_goods = %(FK_Goods)s GROUP BY ngr.FK_Goods)Rec
            LEFT OUTER JOIN (SELECT FK_Goods,COUNT(FK_Goods) AS Total FROM Temp_Goods_Used_""" + username + """ GROUP BY FK_Goods)T_Used 
                ON Rec.FK_Goods = T_Used.FK_Goods """
        elif(GoodCat == "O"):
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})
        if cur.rowcount > 0:
            row = cur.fetchone()
            totalNew = int(row[1])
            totalReceived = int(row[0])
            totalUsed = int(row[2])
        # totalReturn
        if GoodCat == "IT":
            Query = """SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_goods_return WHERE FK_Goods = %(FK_Goods)s )C """
        elif GoodCat == "GA":
            Query = """SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_ga_return WHERE FK_Goods = %(FK_Goods)s )C """
        elif(GoodCat == "O"):
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})
        if cur.rowcount > 0:
            row = cur.fetchone()
            totalReturn = int(row[0])
        #totalBroken
        #total broken di peroleh dari kondisi barang yang di kembalikan dari user(na goods_return/na_ga_return,na_maintenance,ga_maintenance)

        if GoodsCat == "IT":
            Query = """SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_goods_return WHERE FK_Goods = %(FK_Goods)s AND `Conditions` = 'B' \
                                                    UNION 
                                                    SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_maintenance WHERE FK_Goods = %(FK_Goods)s AND IsSucced = 0 AND IsFinished = 1 \
                                                    )C """
        elif GoodCat == "GA":
            Query = """SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_ga_return WHERE FK_Goods = %(FK_Goods)s AND `Conditions` = 'B' \
                                                    UNION 
                                                    SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_ga_maintenance WHERE FK_Goods = %(FK_Goods)s AND IsSucced = 0 AND IsFinished = 1 \
                                                    )C """
        elif(GoodCat == "O"):
            raise Exception('Can di gawean')

        cur.execute(Query, {'FK_Goods': FKGoods})
        # totalRenew
        # TotalRenew diperoleh di n_a_maintenance kondisi IsSucced = 1, dan belum ada di n_a_goods_lending dan n_a_goods_outwards,dan  n_a_disposal
        if GoodCat == "IT":
            Query = """SELECT COUNT(c.FK_Goods) FROM (SELECT DISTINCT mt.FK_Goods,mt.TypeApp,mt.SerialNumber FROM n_a_maintenance mt WHERE mt.IsSucced = 1 AND mt.IsFinished = 1
                    AND NOT EXISTS(SELECT IDApp FROM n_a_goods_lending WHERE FK_Maintenance = mt.IDApp)
                    AND NOT EXISTS(SELECT IDApp FROM n_a_goods_outwards WHERE FK_FromMaintenance = mt.IDApp)
                    AND NOT EXISTS(SELECT IDApp FROM n_a_disposal WHERE FK_Maintenance = mt.IDApp)
                    AND mt.FK_Goods = %(FK_Goods)s)C """
        elif GoodCat == "GA":
            Query = """SELECT COUNT(c.FK_Goods) FROM (SELECT DISTINCT mt.FK_Goods,mt.TypeApp,mt.SerialNumber FROM n_a_ga_maintenance mt WHERE mt.IsSucced = 1 AND mt.IsFinished = 1
                    AND NOT EXISTS(SELECT IDApp FROM n_a_ga_outwards_outwards WHERE FK_FromMaintenance = mt.IDApp)
                    AND NOT EXISTS(SELECT IDApp FROM n_a_disposal WHERE FK_Maintenance = mt.IDApp)
                    AND mt.FK_Goods = %(FK_Goods)s)C """
        elif Goodcat == "O":
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})

        if cur.rowcount > 0:
            row = cur.fetchone()
            totalRenew = int(row[0])

        # TMaintenance
        # TMaintenance diperoleh di n_a_maintenance kondisi  IsFinished = 0
        if GoodCat == "IT":
            Query = " SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_maintenance WHERE IsFinished = 0 AND FK_Goods = %(FK_Goods)s)C "
        elif GoodCat == "GA":
            Query = " SELECT COUNT(FK_Goods) FROM (SELECT DISTINCT FK_Goods,TypeApp,SerialNumber FROM n_a_ga_maintenance WHERE IsFinished = 0 AND FK_Goods = %(FK_Goods)s)C "
        elif GoodCat == "O":
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})
        if cur.rowcount > 0:
            row = cur.fetchone()
            totalMaintenance = int(row[0])
        # TotalSpare
        # TotalSpare diperoleh di n_a_goods_lending dengan kondisi status = L dan tidak ada di n_a_goods_lost
        if GoodCat == "IT":
            Query = """SELECT COUNT(FK_goods) FROM (SELECT DISTINCT nl.FK_goods,nl.TypeApp,nl.SerialNumber FROM n_a_goods_lending nl WHERE nl.Status = 'R'
                    AND NOT EXISTS(SELECT FK_Goods FROM n_a_maintenance WHERE SerialNumber = nl.SerialNumber AND IsFinished = 0)
                    AND NOT EXISTS(SELECT FK_Goods FROM n_a_goods_outwards WHERE FK_Lending = nl.IDApp)
                    AND NOT EXISTS(SELECT FK_Goods FROM n_a_disposal WHERE SerialNumber = nl.SerialNumber) AND nl.FK_Goods =  %(FK_Goods)s)C """
        elif GoodCat == "O":
            raise Exception('Can di gawean')
        cur.execute(Query, {'FK_Goods': FKGoods})

        if cur.rowcount > 0:
            row = cur.fetchone()
            TotalSpare = int(row[0])
        #total disposed
        Query = "SELECT COUNT(FK_Goods) FROM n_a_disposal WHERE FK_Goods =  %(FK_Goods)s"
        cur.execute(Query, {'FK_Goods': FKGoods})
        if cur.rowcount > 0:
            row = cur.fetchone()
            totalDisposal = int(row[0])
        #totalLost
        Query = "SELECT COUNT(FK_Goods) FROM n_a_goods_lost WHERE FK_Goods =  %(FK_Goods)s"
        cur.execute(Query, {'FK_Goods': FKGoods})
        if cur.rowcount > 0:
            row = cur.fetchone()
            totalLost = int(row[0])
        # drop table temporary
        Query = "DROP TEMPORARY TABLE IF EXISTS Temp_Goods_Used_" + username
        cur.execute(Query)
        if closeCursor:
            cur.close()
        return(totalNew, totalReceived, totalUsed, totalReturn, totalRenew, totalMaintenance, TotalSpare,totalBroken,totalDisposal,totalLost)


    def retriveColumn(**kwargs):
        table = kwargs['table']
        resolve = kwargs['resolve'].lower()
        initialname = kwargs['initial_name']
        fields = []
        if isinstance(table, list):
            for i in range(len(table)):
                fields.append([j.name.lower()
                               for j in table[i]._meta.local_fields])
        else:
            fields = [i.name.lower() for i in table._meta.local_fields]

        result = None
        custom_fields = kwargs.get('custom_fields')
        if custom_fields:
            if isinstance(custom_fields, list):
                for field in custom_fields:
                    fields.append(field)
            else:
                fields.append([custom_fields])
        for i in range(len(fields)):
            if resolve in fields[i]:
                result = str(initialname[i] + "." + resolve)
                if kwargs.get('exclude'):
                    if result in kwargs.get('exclude'):
                        continue
                break
        if result:
            return result
        raise ValueError('cannot resolve \'%s\' column' % resolve)

    def get_log_data(**kwargs):
        """
        to get log event data, use it to get date informations if data has deleted, existed or updated
        param
        action: e.g (deleted,updated)
        action for getting type of log event

        PK: primary key e.g (IDApp,SupplierCode)
        table: to determine , which table to get
        usage :: get_log_data(action='deleted',pk=2,table='employee')
        """

        cur = connection.cursor()
        action = kwargs['action']
        Query = """SELECT createddate FROM logevent WHERE JSON_EXTRACT(descriptions,$.""" + \
            action + \
                """[0])=%(PK)s AND nameapp LIKE %(NameApp)%"""  # PK (Primary Key)
        if action == 'updated':
            Query = Query + """ AND idapp = (SELECT Max(idapp) FROM logevent WHERE JSON_EXTRACT(descriptions,$.""" + \
                action+"""[0])=%(PK)s AND nameapp LIKE %(NameApp)%)"""
        cur.execute(Query, {'PK': kwargs['pk'], 'NameApp': kwargs['table']})
        return query.dictfetchall(cur)

    def response_default(data):
        """
        this is default HttpResponse, use it to correct and neat response
        param
        must instance of tuple
        e.g (Data.Success,Message.Success) or (Data.Exists,Message.get_exists_info)
        """
        statusResp = 200
        if isinstance(data, tuple):
            message = None
            if data[0] == Data.Success:
                if len(data) > 1:
                    message = data[1]
                else:
                    message = Message.Success.value
            if data[0] in [Data.Exists, Data.HasRef, Data.ValidationError]:
                statusResp = 400
                message = data[1]
            elif data[0] == Data.Lost:
                statusResp = 404
                message = data[1]
            elif data[0] == Data.Empty:
                statusResp = 404
                if len(data) > 1:
                    message = data[1]
                else:
                    message = Message.Empty.value
            return HttpResponse(
                json.dumps({'message': message}),
                status=statusResp,
                content_type='application/json'
            )

    def multi_sort_queryset(queryset, Isidx, Isord):
        """
        param:
        queryset:must be queryset instance,
        Isidx: which column you want to order_by
        Isord: asc/desc
        """

        if (Isord is not None and Isord != '') \
                and (Isidx is not None and Isidx != ''):
            if ',' in Isidx:
                multi_sort = []
                Isidx = Isidx.split(',')
                sorts = []
                for i in Isidx:
                    sorts.append(i.lstrip())  # trim left whitespace

                for i in sorts:
                    # simpan di variable bila sering digunakan, kamar boleh acak2 an ,tapi coding harus rapi :D
                    i_split = i.split(' ')
                    i_len_split = len(i_split)
                    if i_len_split > 1:
                        if i_split[1] == 'desc':
                            sort_by = '-'
                        elif i_split[1] == 'asc':
                            sort_by = ''
                    elif i_len_split == 1:
                        if Isord == 'desc':
                            sort_by = '-'
                        elif Isord == 'asc':
                            sort_by = ''
                    multi_sort.append(sort_by+i.split(' ')[0])
                return queryset.order_by(*multi_sort)
            else:
                sort = str(Isidx)
                if Isord == 'desc':
                    sort = '-' + sort
                    return queryset.order_by(sort)
                return queryset
        else:
            raise ValueError(
                'Cannot assign "None" type object \n make sure if arguments/parameter is not None')

    def EmptyGrid():
        return {"page": "1", "total": 0, "records": 0, "rows": []}

    def permision_denied(message=None):
        _message = 'You don\'t have permission for this action'
        if message:
            _message = message
        return HttpResponse(_message, status=403)

    def check_file_exists(file_dir):
        return path.exists(file_dir)

    def check_dir_exists(dirr):
        if path.isdir(dirr):
            return path.exists(dirr)
        else:
            raise IsADirectoryError('this %s is not a directory' % dirr)

    def create_dir(dirr):
        try:
            makedirs(dirr, exist_ok=True)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

    @classmethod
    def handle_image_upload(cls, username, image_name):
        dir_user_image = settings.STATIC_ROOT + '/NA_User_Image/UploadImg/' + username
        cls.create_dir(dir_user_image)
        if cls.check_dir_exists(dir_user_image + image_name):
            remove(dir_user_image)
        # this is manually, but for good idea look at this is reference https://stackoverflow.com/questions/15885201/django-uploads-discard-uploaded-duplicates-use-existing-file-md5-based-check

    def serialize_queryset(queryset):
        try:
            data = serialize('json', queryset)
        except AttributeError:
            data = [i for i in queryset]
        return data

    def cache_queryset(queryset):
        return [i for i in queryset]

    @classmethod
    def search_data_by_form(cls, request, data, fields):
        """get goods data for grid searching, retusn idapp,itemcode,goods criteria = icontains"""
        Isidx = request.GET.get('sidx', '')
        Isord = request.GET.get('sord', '')

        searchText = request.GET.get('goods_desc')
        Type = request.GET.get('type')
        Ilimit = request.GET.get('rows', '')
        if data == Data.Empty:
            results = {"page": "1", "total": 0, "records": 0, "rows": []}
            return HttpResponse(
                json.dumps(results, indent=4, cls=DjangoJSONEncoder),
                content_type='application/json'
            )
        if isinstance(data, QuerySet):
            try:
                multi_sort = cls.multi_sort_queryset(data, Isidx, Isord)
            except ValueError:
                multi_sort = data
            else:
                data = multi_sort
            totalRecord = data.count()
        else:
            totalRecord = len(data)
        paginator = Paginator(data, int(Ilimit))
        try:
            page = request.GET.get('page', '1')
        except ValueError:
            page = 1
        try:
            dataRows = paginator.page(page)
        except (EmptyPage, InvalidPage):
            dataRows = paginator.page(paginator.num_pages)

        rows = []
        i = 0
        fields.remove('idapp')
        for row in dataRows.object_list:
            i += 1
            cell = [row['idapp'], i]
            for field in fields:
                cell.append(row.get(field))
            datarow = {
                "id": row['idapp'], "cell": cell
            }
            rows.append(datarow)
        results = {"page": page, "total": paginator.num_pages,
                   "records": totalRecord, "rows": rows}
        return HttpResponse(
            json.dumps(results, indent=4, cls=DjangoJSONEncoder),
            content_type='application/json'
        )
