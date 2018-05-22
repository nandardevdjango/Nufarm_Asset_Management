from django.db import models,transaction,connection
from NA_DataLayer.common import StatusForm,CriteriaSearch,query,ResolveCriteria,DataType

class NA_BR_Receive_other(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        cur = connection.cursor()
        Query = """CREATE TEMPORARY TABLE T_Receive_other ENGINE=InnoDB AS (SELECT ngr.IDApp,ngr.refno,g.goodsname as goods,
	    ngr.datereceived,sp.supliername,ngr.FK_ReceivedBy,emp1.receivedby,ngr.FK_P_R_By ,emp2.pr_by,ngr.totalpurchase,
        ngr.totalreceived,CONCAT(IFNULL(ngr.descriptions,' '),', ITEMS : ', IFNULL(ngr.DescBySystem,' ')) AS descriptions, 
        ngr.CreatedDate,ngr.CreatedBy FROM n_a_goods_receive AS ngr INNER JOIN n_a_suplier AS sp ON sp.SuplierCode = ngr.FK_Suplier 
        LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS receivedby FROM employee) AS emp1 ON emp1.IDApp = ngr.FK_ReceivedBy 
        LEFT OUTER JOIN (SELECT IDApp,Employee_Name AS pr_by FROM employee) AS emp2 ON emp2.IDApp = ngr.FK_P_R_By 
		INNER JOIN n_a_goods as g ON g.IDApp = ngr.FK_goods  WHERE """  + columnKey + rs.Sql() + ")"
        cur.execute(Query)
        Query = """SELECT * FROM T_Receive_other"""
        cur.execute(Query)
        return query.dictfetchall(cur)

    def SaveData(self,statusForm=StatusForm.Input,**data):
        cur = connection.cursor()