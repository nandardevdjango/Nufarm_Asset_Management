from django.db import models,transaction,connection
from NA_DataLayer.common import (StatusForm,CriteriaSearch,query,ResolveCriteria,
                                 DataType,Data,Message)
from django.db.models import F

class NA_BR_Goods_Receive_GA(models.Manager):

    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        gaData = super(NA_BR_Goods_Receive_GA, self).get_queryset()\
            .annotate(
                goodsname=F('fk_goods__goodsname'),
                price=F('fk_goods__priceperunit'),
                supliername=F('fk_suplier__supliername'),
                received_by=F('fk_receivedby__employee_name'),
                pr_by=F('fk_p_r_by__employee_name')
            )\
            .values('idapp','goodsname','typeapp','price','supliername',
                    'datereceived','brand','invoice_no','machine_no','chasis_no', 'year_made',
                    'colour','model','kind', 'cylinder', 'fuel', 'descriptions',
                    'createddate','createdby')
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            gaData = gaData.exclude(**{filterfield:[ValueKey]})
        if criteria==CriteriaSearch.Equal:
            gaData = gaData.filter(**{filterfield: ValueKey})
        elif criteria==CriteriaSearch.Greater:
            filterfield = columnKey + '__gt'
        elif criteria==CriteriaSearch.GreaterOrEqual:
            filterfield = columnKey + '__gte'
        elif criteria==CriteriaSearch.In:
            filterfield = columnKey + '__in'
        elif criteria==CriteriaSearch.Less:
            filterfield = columnKey + '__lt'
        elif criteria==CriteriaSearch.LessOrEqual:
            filterfield = columnKey + '__lte'
        elif criteria==CriteriaSearch.Like:
            filterfield = columnKey + '__icontains'
            gaData = gaData.filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
            gaData = gaData.filter(**rs.DefaultModel())
        return gaData

    def SaveData(self,statusForm=StatusForm.Input,**data):
        cur = connection.cursor()
        Params = {
            'RefNO':data['refno'],'FK_goods':data['fk_goods'], 'DateReceived':data['datereceived'], 
            'FK_Suplier':data['fk_suplier'], 'TotalPurchase':data['totalpurchase'],
            'TotalReceived':data['totalreceived'],'FK_ReceivedBy':data['fk_receivedby'],
            'FK_P_R_By':data['fk_p_r_by'],'Descriptions':data['descriptions'],
            #'descbysystem':data['descbysystem']
            }
        if statusForm == StatusForm.Input:
            Params['CreatedDate'] = data['createddate']
            Params['CreatedBy'] = data['createdby']
            Query = """INSERT INTO n_a_goods_receive_other 
            (REFNO,FK_goods, DateReceived, FK_Suplier, TotalPurchase, TotalReceived, 
            FK_ReceivedBy, FK_P_R_By, Descriptions,CreatedDate, CreatedBy) 
            VALUES ({})""".format(','.join('%('+i+')s' for i in Params))
            cur.execute(Query,Params)
            return (Data.Success,Message.Success.value)
        elif statusForm == StatusForm.Edit:
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Query = """UPDATE n_a_goods_receive SET 
            RefNO = %(RefNO)s,DateReceived = %(DateReceived)s,FK_Suplier = %(FK_Suplier)s,TotalPurchase = %(TotalPurchase)s, 
            FK_ReceivedBy = %(FK_ReceivedBy)s,FK_P_R_By = %(FK_P_R_By)s,ModifiedDate = %(ModifiedDate)s,ModifiedBy = %(ModifiedBy)s,
            Descriptions = %(Descriptions)s"""
            cur.execute(Query,Params)
            return (Data.Success,Message.Success.value)

    def DeleteData(self,idapp):
        if self.dataExists(idapp=idapp):
            if self.hasRef(idapp):
                return (Data.HasRef,Message.HasRef_del.value)
            else:
                cur = connection.cursor()
                Query = """DELETE FROM n_a_goods_receive_other WHERE idapp=%(IDApp)s"""
                cur.execute(Query,{'IDApp':idapp})
                return (Data.Success,)
        else:
            return (Data.Lost,)

    def retrieveData(self,idapp):
        if self.dataExists(idapp=idapp):
            cur = connection.cursor()
            Query = """SELECT ngr.idapp,ngr.refno,ngr.FK_goods AS idapp_fk_goods,g.itemcode AS fk_goods, goodsname as goods_desc,
            g.economiclife,ngr.datereceived,ngr.fk_suplier,sp.supliername,ngr.fk_ReceivedBy as idapp_fk_receivedby,emp1.fk_receivedby,
            emp1.employee_received,ngr.FK_P_R_By AS idapp_fk_p_r_by,emp2.fk_p_r_by,emp2.employee_pr,ngr.totalpurchase,ngr.totalreceived,
            ngr.descriptions,ngr.descbysystem FROM n_a_goods_receive_other AS ngr INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier 
            LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_receivedby,employee_name AS employee_received FROM employee) AS emp1 ON emp1.IDApp = ngr.FK_ReceivedBy 
            LEFT OUTER JOIN (SELECT IDApp,NIK AS fk_p_r_by,employee_name AS employee_pr FROM employee) AS emp2 ON emp2.IDApp = ngr.FK_P_R_By
            INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE ngr.IDApp = %(IDApp)s"""

            cur.execute(Query,{'IDApp':idapp})
            result = query.dictfetchall(cur)
            return (Data.Success,result[0])
        else:
            return (Data.Lost,Message.get_lost_info(pk=idapp,table='n_a_goods_receive_other'))

    def dataExists(self,**kwargs):
        idapp = kwargs.get('idapp')
        if idapp is not None:
            return super(NA_BR_Goods_Receive_GA,self).get_queryset()\
                .filter(idapp=idapp).exists()

    def hasRef(self,idapp):
        return False