from django.db import models, connection
from django.db.models import F

from NA_DataLayer.common import (StatusForm, CriteriaSearch, query, ResolveCriteria,
                                 DataType, Data, Message)


class NA_BR_Goods_Receive_GA(models.Manager):

    def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
        gaData = super(NA_BR_Goods_Receive_GA, self).get_queryset()\
            .annotate(
                goodsname=F('fk_goods__goodsname'),
                suppliername=F('fk_supplier__suppliername'),
                received_by=F('fk_receivedby__employee_name'),
                pr_by=F('fk_p_r_by__employee_name')
        )\
            .values('idapp', 'goodsname', 'typeapp', 'price', 'received_by', 'pr_by', 'suppliername',
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
            'FK_Supplier': data['suppliercode'],
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
            (FK_goods, FK_ReceivedBy, FK_P_R_By, FK_Supplier, DateReceived, Brand, Invoice_no,
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
            FK_Supplier = %(FK_Supplier)s,
            FK_ReceivedBy = %(FK_ReceivedBy)s,
            FK_P_R_By = %(FK_P_R_By)s,
            brand = %(brand)s,
            invoice_no = %(invoice_no)s,
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
            Descriptions = %(Descriptions)s
            WHERE idapp = %(idapp)s"""
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
            cur = connection.cursor()
            query_string = """
            CREATE TEMPORARY TABLE T_form_ga_receive ENGINE=InnoDB AS(
                SELECT ngr.idapp, ngr.fk_goods, g.itemcode, g.goodsname, s.suppliercode,
                s.suppliername, ngr.fk_p_r_by AS pr_by, emp1.pr_by_nik, emp1.pr_by_name,
                ngr.fk_receivedby AS received_by, emp2.received_by_nik, emp2.received_by_name,
                DATE_FORMAT(ngr.datereceived, \'%%d/%%m/%%Y\') AS datereceived, ngr.brand,
                ngr.invoice_no, ngr.typeapp, ngr.machine_no,
                ngr.chassis_no, DATE_FORMAT(ngr.year_made, \'%%Y\') AS year_made, ngr.colour,
                ngr.model, ngr.kind, ngr.cylinder,
                ngr.fuel, ngr.price, ngr.descriptions, ngh.reg_no, 
                DATE_FORMAT(ngh.date_reg, \'%%d/%%m/%%Y\') AS date_reg,
                DATE_FORMAT(ngh.expired_reg, \'%%d/%%m/%%Y\') AS expired_reg, 
                DATE_FORMAT(ngh.bpkb_expired, \'%%d/%%m/%%Y\') AS bpkb_expired,
                ngh.descriptions AS remark
                FROM n_a_ga_receive AS ngr
                INNER JOIN n_a_goods AS g ON ngr.fk_goods = g.idapp
                INNER JOIN n_a_supplier AS s ON ngr.fk_supplier = s.suppliercode
                LEFT OUTER JOIN (
                    SELECT idapp, nik AS pr_by_nik, employee_name AS pr_by_name
                    FROM employee
                ) AS emp1 ON ngr.fk_p_r_by = emp1.idapp
                LEFT OUTER JOIN (
                    SELECT idapp, nik AS received_by_nik, employee_name AS received_by_name
                    FROM employee
                ) AS emp2 ON ngr.fk_receivedby = emp2.idapp
                LEFT JOIN n_a_ga_vn_history AS ngh ON ngr.idapp = ngh.fk_app
                WHERE ngr.idapp = %(idapp)s
            )
            """
            cur.execute(query_string, {'idapp': idapp})
            query_string = """
            SELECT * FROM T_form_ga_receive
            """
            cur.execute(query_string)
            result = query.dictfetchall(cur)[0]
            return (Data.Success, result)
        else:
            return (Data.Lost, Message.get_lost_info(pk=idapp, table='n_a_goods_receive_other'))

    def dataExists(self, **kwargs):
        idapp = kwargs.get('idapp')
        if idapp is not None:
            return super(NA_BR_Goods_Receive_GA, self).get_queryset()\
                .filter(idapp=idapp).exists()

    def hasRef(self, idapp):
        return False
