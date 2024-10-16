from django.db import models, transaction, connection
from NA_DataLayer.common import (StatusForm, CriteriaSearch, query, ResolveCriteria,
                                 DataType, Data, Message)


class NA_BR_Goods_Receive_other(models.Manager):

    def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
        cur = connection.cursor()
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)

        Query = """CREATE TEMPORARY TABLE T_Receive_other ENGINE=InnoDB AS (SELECT ngr.IDApp,
        ngr.refno,g.goodsname as goods, ngr.datereceived,sp.suppliername,ngr.FK_ReceivedBy,
        emp1.receivedby,ngr.FK_P_R_By ,emp2.pr_by,ngr.totalpurchase, ngr.totalreceived,
        CONCAT(IFNULL(ngr.descriptions,' '),', ITEMS : ', IFNULL(ngr.DescBySystem,' ')) AS
        descriptions,ngr.CreatedDate,ngr.CreatedBy FROM n_a_goods_receive_other AS ngr
        INNER JOIN n_a_supplier AS sp ON sp.SupplierCode = ngr.FK_Supplier LEFT OUTER JOIN
        (SELECT IDApp,Employee_Name AS receivedby FROM employee) AS emp1 ON
        emp1.IDApp = ngr.FK_ReceivedBy LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS
        pr_by FROM employee) AS emp2 ON emp2.IDApp = ngr.FK_P_R_By
        INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods WHERE """ + columnKey + rs.Sql() + ")"
        cur.execute(Query)
        Query = """SELECT * FROM T_Receive_other"""
        cur.execute(Query)
        result = query.dictfetchall(cur)
        cur.execute('DROP TEMPORARY TABLE IF EXISTS T_Receive_other')
        return result

    def SaveData(self, statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Params = {
            'RefNO': data['refno'], 'FK_goods': data['fk_goods'], 'DateReceived': data['datereceived'],
            'FK_Supplier': data['fk_supplier'], 'TotalPurchase': data['totalpurchase'],
            'TotalReceived': data['totalreceived'], 'FK_ReceivedBy': data['fk_receivedby'],
            'FK_P_R_By': data['fk_p_r_by'], 'Descriptions': data['descriptions'],
            # 'descbysystem':data['descbysystem']
        }
        if statusForm == StatusForm.Input:
            Params['CreatedDate'] = data['createddate']
            Params['CreatedBy'] = data['createdby']
            Query = """INSERT INTO n_a_goods_receive_other
            (REFNO,FK_goods, DateReceived, FK_Supplier, TotalPurchase, TotalReceived,
            FK_ReceivedBy, FK_P_R_By, Descriptions,CreatedDate, CreatedBy)
            VALUES ({})""".format(','.join('%(' + i + ')s' for i in Params))
            cur.execute(Query, Params)
            return (Data.Success, Message.Success.value)
        elif statusForm == StatusForm.Edit:
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Query = """UPDATE n_a_goods_receive SET
            RefNO = %(RefNO)s,
            DateReceived = %(DateReceived)s,
            FK_Supplier = %(FK_Supplier)s,
            TotalPurchase = %(TotalPurchase)s, 
            FK_ReceivedBy = %(FK_ReceivedBy)s,
            FK_P_R_By = %(FK_P_R_By)s,
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
            cur = connection.cursor()
            Query = """SELECT ngr.idapp,ngr.refno,ngr.FK_goods AS idapp_fk_goods, g.itemcode
            AS fk_goods, goodsname as goods_desc,g.economiclife,ngr.datereceived,
            ngr.fk_supplier,sp.suppliername,ngr.fk_ReceivedBy as idapp_fk_receivedby,
            emp1.fk_receivedby,emp1.employee_received,ngr.FK_P_R_By AS idapp_fk_p_r_by,
            emp2.fk_p_r_by,emp2.employee_pr,ngr.totalpurchase,ngr.totalreceived,
            ngr.descriptions,ngr.descbysystem FROM n_a_goods_receive_other AS ngr
            INNER JOIN n_a_supplier AS sp ON sp.SupplierCode = ngr.FK_Supplier
            LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_receivedby,employee_name AS
            employee_received FROM employee) AS emp1 ON emp1.IDApp = ngr.FK_ReceivedBy
            LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_p_r_by,employee_name AS employee_pr
            FROM employee) AS emp2 ON emp2.IDApp = ngr.FK_P_R_By
            INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE ngr.IDApp = %(IDApp)s"""

            cur.execute(Query, {'IDApp': idapp})
            result = query.dictfetchall(cur)
            return (Data.Success, result[0])
        else:
            return (Data.Lost, Message.get_lost_info(pk=idapp, table='n_a_goods_receive_other'))

    def dataExists(self, **kwargs):
        idapp = kwargs.get('idapp')
        if idapp is not None:
            return super(NA_BR_Goods_Receive_other, self).get_queryset()\
                .filter(idapp=idapp).exists()

    def hasRef(self, idapp):
        return False
