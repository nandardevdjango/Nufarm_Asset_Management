from django.db import models, connection
from NA_DataLayer.common import CriteriaSearch,DataType,ResolveCriteria, query

class NA_BR_Goods_Return(models.Manager):
    def PopulateQuery(self, columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        cur = connection.cursor()
        rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
        Query = """SELECT ngr.idapp,ngr.datereturn,ngr.conditions,ngr.iscompleted,ngr.minusDesc,ngr.typeapp,ngr.serialnumber,
        ngr.descriptions, ngr.createddate, ngr.createdby, CONCAT(g.goodsname, ' ',g.brandname,' ',g.typeapp) AS goods,emp1.fromemployee,
        emp2.usedemployee FROM n_a_goods_return ngr INNER JOIN n_a_goods g ON ngr.fk_goods = g.idapp LEFT OUTER JOIN 
        (SELECT idapp, employee_name AS fromemployee FROM employee) AS emp1 ON ngr.fk_fromemployee = emp1.idapp
        LEFT OUTER JOIN (SELECT idapp,employee_name AS usedemployee FROM employee) AS emp2 ON ngr.fk_usedemployee = emp2.idapp
        WHERE """ + columnKey + rs.Sql()
        cur.execute(Query)
        cur.close()
        result = query.dictfetchall(cur)
        return result