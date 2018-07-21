from django.db import models, connection
from django.db.models import F

from NA_DataLayer.common import (StatusForm, CriteriaSearch, query, ResolveCriteria,
                                 DataType, Data, Message)


class NA_BR_Goods_Receive_GA(models.Manager):

    def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
        gaData = super(NA_BR_Goods_Receive_GA, self).get_queryset()\
            .annotate(
                goodsname=F('fk_goods__goodsname'),
                supliername=F('fk_suplier__supliername'),
                received_by=F('fk_receivedby__employee_name'),
                pr_by=F('fk_p_r_by__employee_name')
        )\
            .values('idapp', 'goodsname', 'typeapp', 'price', 'received_by', 'pr_by', 'supliername',
                    'datereceived', 'brand', 'invoice_no', 'machine_no', 'chassis_no', 'year_made',
                    'colour', 'model', 'kind', 'cylinder', 'fuel', 'descriptions',
                    'createddate', 'createdby')
        filterfield = columnKey
        if criteria == CriteriaSearch.NotEqual or criteria == CriteriaSearch.NotIn:
            if criteria == CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            gaData = gaData.exclude(**{filterfield: [ValueKey]})
        if criteria == CriteriaSearch.Equal:
            gaData = gaData.filter(**{filterfield: ValueKey})
        elif criteria == CriteriaSearch.Greater:
            filterfield = columnKey + '__gt'
        elif criteria == CriteriaSearch.GreaterOrEqual:
            filterfield = columnKey + '__gte'
        elif criteria == CriteriaSearch.In:
            filterfield = columnKey + '__in'
        elif criteria == CriteriaSearch.Less:
            filterfield = columnKey + '__lt'
        elif criteria == CriteriaSearch.LessOrEqual:
            filterfield = columnKey + '__lte'
        elif criteria == CriteriaSearch.Like:
            filterfield = columnKey + '__icontains'
            gaData = gaData.filter(
                **{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if (criteria == CriteriaSearch.Beetween or criteria == CriteriaSearch.BeginWith or
                criteria == CriteriaSearch.EndWith):
            rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
            gaData = gaData.filter(**rs.DefaultModel())
        return gaData.order_by('idapp')

    def SaveData(self, statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Params = {
            'FK_goods': data['fk_goods'],
            'FK_ReceivedBy': data['received_by'],
            'FK_P_R_By': data['pr_by'],
            'FK_Suplier': data['supliercode'],
            'DateReceived': data['datereceived'],
            'brand': data['brand'],
            'invoice_no': data['invoice_no'],
            'typeapp': data['typeapp'],
            'machine_no': data['machine_no'],
            'chassis_no': data['chassis_no'],
            'year_made': data['year_made'] + '-1-1',
            'colour': data['colour'],
            'model': data['model'],
            'kind': data['kind'],
            'cylinder': data['cylinder'],
            'fuel': data['fuel'],
            'price': data['price'],
            'Descriptions': data['descriptions']
        }
        if statusForm == StatusForm.Input:
            Params['CreatedDate'] = data['createddate']
            Params['CreatedBy'] = data['createdby']
            Query = """INSERT INTO n_a_ga_receive
            (FK_goods, FK_ReceivedBy, FK_P_R_By, FK_Suplier, DateReceived, Brand, Invoice_no,
            TypeApp, Machine_no, Chassis_no, Year_made, Colour, Model,Kind, Cylinder, Fuel,
            Price, Descriptions,CreatedDate, CreatedBy) 
            VALUES ({})""".format(','.join('%(' + i + ')s' for i in Params))
            cur.execute(Query, Params)
            return (Data.Success, Message.Success.value)
        elif statusForm == StatusForm.Edit:
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Query = """UPDATE n_a_ga_receive SET 
            FK_Goods = %(FK_goods)s,
            DateReceived = %(DateReceived)s,
            FK_Suplier = %(FK_Suplier)s,
            FK_ReceivedBy = %(FK_ReceivedBy)s,
            FK_P_R_By = %(FK_P_R_By)s,
            brand = %(brand)s,invoice_no = %(invoice_no)s,
            typeapp = %(typeapp)s,
            machine_no = %(machine_no)s,
            chassis_no = %(chassis_no)s,
            year_made = %(year_made)s,
            colour = %(colour)s,
            model = %(model)s,
            kind = %(kind)s,
            cylinder = %(cylinder)s,
            fuel = %(fuel)s,
            Price = %(price)s,
            ModifiedDate = %(ModifiedDate)s,
            ModifiedBy = %(ModifiedBy)s,
            Descriptions = %(Descriptions)s"""
            cur.execute(Query, Params)
            return (Data.Success, Message.Success.value)

    def DeleteData(self, idapp):
        if self.dataExists(idapp=idapp):
            if self.hasRef(idapp):
                return (Data.HasRef, Message.HasRef_del.value)
            else:
                cur = connection.cursor()
                Query = """DELETE FROM n_a_goods_receive_other WHERE idapp=%(IDApp)s"""
                cur.execute(Query, {'IDApp': idapp})
                return (Data.Success,)
        else:
            return (Data.Lost,)

    def retrieveData(self, idapp):
        if self.dataExists(idapp=idapp):
            if self.hasRef(idapp):
                return (Data.HasRef, Message.HasRef_edit)
            data = super(NA_BR_Goods_Receive_GA, self).get_queryset()\
                .filter(idapp=idapp)\
                .annotate(
                goodsname=F('fk_goods__goodsname'),
                itemcode=F('fk_goods__itemcode'),
                supliercode=F('fk_suplier'),
                supliername=F('fk_suplier__supliername'),
                received_by=F('fk_receivedby'),
                received_by_nik=F('fk_receivedby__nik'),
                received_by_name=F('fk_receivedby__employee_name'),
                pr_by=F('fk_p_r_by'),
                pr_by_nik=F('fk_p_r_by__nik'),
                pr_by_name=F('fk_p_r_by__employee_name'))\
                .values('idapp', 'fk_goods', 'itemcode', 'goodsname', 'supliercode', 'supliername', 'pr_by',
                        'pr_by_nik', 'pr_by_name', 'received_by', 'received_by_nik', 'received_by_name', 'datereceived',
                        'brand', 'invoice_no', 'typeapp', 'machine_no', 'chassis_no', 'year_made', 'colour',
                        'model', 'kind', 'cylinder', 'fuel', 'price','descriptions')

            return (Data.Success, data)
        else:
            return (Data.Lost, Message.get_lost_info(pk=idapp, table='n_a_goods_receive_other'))

    def dataExists(self, **kwargs):
        idapp = kwargs.get('idapp')
        if idapp is not None:
            return super(NA_BR_Goods_Receive_GA, self).get_queryset()\
                .filter(idapp=idapp).exists()

    def hasRef(self, idapp):
        return False
