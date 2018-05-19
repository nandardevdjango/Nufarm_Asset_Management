from django.db import models, connection
from NA_DataLayer.common import (CriteriaSearch,DataType,ResolveCriteria, query,
                                 StatusForm,Data)

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
        result = query.dictfetchall(cur)
        cur.close()
        return result


    def SaveData(self,statusForm=StatusForm.Input,**data):
        cur = connection.cursor()
        Params = {
            'FK_Goods':data['fk_goods'],'DateReturn':data['datereturn'],'Conditions':data['condition'],
            'FK_fromeployee':data['fk_fromemployee'],'FK_usedemployee':data['fk_usedemployee'],
            'IsCompleted':data['iscompleted'],'MinusDesc':data['minusDesc'],'FK_goods_outwards':data['fk_goods_outwards'],
            'FK_goods_lend':data['fk_goods_lend'],'Descriptions':data['descriptions']
            }
        if statusForm == StatusForm.Input:
            Params['CreatedDate'] = data['createddate']
            Params['CreatedBy'] = data['createdby']
            Query = """INSERT INTO n_a_goods_return (fk_goods,datereturn,conditions,fk_fromemployee,fk_usedemployee,iscompleted,minusDesc,fk_goods_outwards,
            fk_goods_lend,descriptions,createddate,createdby) VALUES({})""".format(','.join('%('+i+')s' for i in Params))
        elif statusForm == StatusForm.Edit:
            pass
            Params['ModifiedDate'] = data['modifiedate']
            Params['ModifiedBy'] = data['modifiedby']
            Query = """"UPDATE n_a_goods_return SET"""
        
        cur.execute(Query,Params)
        cur.close()
        return (Data.Success,)


    def SearchGoods_byForm(self,value):
        cur = connection.cursor()
        Query = """
        (SELECT ngo.idapp,CONCAT(g.goodsname,' ',g.brandname,' ',ngo.typeapp) AS goods, ngo.serialnumber,g.itemcode,
        @fromgoods := 'GO' AS fromgoods FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp WHERE NOT EXISTS 
        (SELECT idapp FROM n_a_goods_return WHERE fk_goods_outwards = ngo.idapp))
        UNION
        (SELECT ngl.idapp,CONCAT(g.goodsname,' ',g.brandname,' ',ngl.typeapp) AS goods, ngl.serialnumber,g.itemcode,
        @fromgoods := 'GL' AS fromgoods FROM n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp WHERE NOT EXISTS
        (SELECT idapp FROM n_a_goods_return WHERE fk_goods_lend = ngl.idapp))
        """
        cur.execute(Query)
        result = query.dictfetchall(cur)
        cur.close()
        return result

    def getGoods_data(self,idapp,fromgoods):
        cur = connection.cursor()
        if fromgoods == 'GO':
            Query = """SELECT ngo.idapp,CONCAT(g.goodsname,' ',g.brandname,' ',ngo.typeapp) AS goods, ngo.serialnumber,g.itemcode,
            @fromgoods := 'GO' AS fromgoods FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp WHERE
            ngo.idapp = %(IDApp)s"""
        elif fromgoods == 'GL':
            Query = """SELECT ngl.idapp,CONCAT(g.goodsname,' ',g.brandname,' ',ngl.typeapp) AS goods, ngl.serialnumber,g.itemcode,
            @fromgoods := 'GL' AS fromgoods FROM n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp WHERE 
            ngl.idapp = %(IDApp)s"""
        cur.execute(Query,{'IDApp':idapp})
        result = query.dictfetchall(cur)
        cur.close()
        return (Data.Success,result)