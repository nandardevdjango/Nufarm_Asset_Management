from django.db import models, connection
from NA_DataLayer.common import  query, ResolveCriteria, StatusForm, CriteriaSearch, DataType, Data,commonFunct
from django.db.models import F, Value, Case, When, CharField
from django.db.models.functions import Concat
from django.db import transaction
class NA_BR_GoodsLost(models.Manager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar,sidx='idapp',sord='desc'):
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
        elif criteria==CriteriaSearch.Equal:
            filterfield = columnKey + '__exact'
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

      
        cur = connection.cursor()
        cur.execute("DROP TEMPORARY TABLE IF EXISTS T_GoodsLost_Manager")
        rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
        Query = """CREATE TEMPORARY TABLE T_GoodsLost_Manager ENGINE=InnoDB AS(SELECT gls.idapp,
        CASE gls.fromgoods WHEN 'GO' then 'Goods Outwards' WHEN 'GL' THEN 'Goods Lending' WHEN 'GM' THEN 'Goods Lending' WHEN 'GR' THEN 'Goods Return' ELSE 'UNKNOWN' END AS fromgoods, gls.serialnumber,
        em.employee_name AS lost_by,gls.datelost, gls.reason,gls.descriptions, gls.createddate, gls.createdby, 
        CONCAT(g.goodsname, ' ',g.brandname, ' ',gls.typeapp) as goods, g.itemcode,emp1.used_by,emp2.resp_person 
        FROM n_a_goods_lost gls INNER JOIN n_a_goods g ON gls.fk_goods = g.idapp LEFT JOIN employee em ON gls.fk_lostby = em.idapp
        LEFT OUTER JOIN (SELECT idapp,employee_name AS used_by FROM employee) AS emp1 ON gls.fk_usedby = emp1.idapp
        LEFT OUTER JOIN (SELECT idapp,employee_name AS resp_person FROM employee) AS emp2 ON gls.fk_responsibleperson = emp2.idapp
        WHERE """
        Query = Query + columnKey + rs.Sql() + " ORDER BY " + sidx + " " + sord + ")"
        cur.execute(Query)
        cur.execute("""SELECT EXISTS(SELECT idapp FROM T_GoodsLost_Manager)""")
        if cur.fetchone()[0] == 0:
            cur.close()
            return []
        Query = """SELECT * FROM T_GoodsLost_Manager"""
        cur.execute(Query)
        result = query.dictfetchall(cur)
        cur.close()
        return result

    def SaveData(self, statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Query = """SELECT IDApp FROM n_a_stock WHERE FK_Goods = %(FK_Goods)s LIMIT 1"""
        cur.execute(Query, {'FK_Goods':data['fk_goods']})
        row = []
        FKApp = 0
        if cur.rowcount > 0:
            row = cur.fetchone()
            fk_stock = row[0]
        who = ''
        param = {}
        Params = {'FK_Goods': data['fk_goods'], 'FK_FromGoods': data['fk_fromgoods'], 'SerialNumber': data['serialnumber'], 'TypeApp': data['typeApp'],'DateLost':data['datelost'],
                    'FK_Goods_Outwards':data['fk_goods_outwards'],'FK_LostBy':data['fk_lostby'],'FK_Goods_Lending':data['fk_goods_lending'],'FK_Goods_Return':data['fk_goods_return'],
                    'FK_Maintenance': data['fk_maintenance'], 'FK_UsedBy': data['fk_usedby'], 'FK_ResponsiblePerson': data['fk_responsibleperson'], 'Status':data['status'],'Reason': data['reason'], 'Descriptions': data['descriptions']}
        try:
            with transaction.atomic():
                if statusForm == StatusForm.Input:
                    if self.dataExist(serialnumber=data['serialnumber'], status='L'):
                        cur.close()
                        return ('HasExist',)
                    else:
                        who = data['createdby']
                        Params['CreatedDate'] = data['createddate']
                        Params['CreatedBy'] = data['createdby']

                    Query = """INSERT INTO n_a_goods_lost(fk_goods, fromgoods, serialnumber, typeapp, datelost,fk_goods_outwards,fk_goods_lending,fk_goods_return,fk_maintenance,fk_lostby,fk_usedby,fk_responsibleperson,status,reason,descriptions,
                    createddate, createdby) VALUES(%(FK_Goods)s, %(FK_FromGoods)s, %(SerialNumber)s, %(TypeApp)s,%(DateLost)s, %(FK_Goods_Outwards)s, %(FK_Goods_Lending)s,%(FK_Goods_Return)s, %(FK_Maintenance)s, %(FK_LostBy)s,%(FK_UsedBy)s,%(FK_ResponsiblePerson)s,%(Status)s,
                    %(Reason)s,%(Descriptions)s, %(CreatedDate)s, %(CreatedBy)s)"""
                    cur.execute(Query, Params)
                    FKApp = cur.lastrowid
                    Query = """INSERT INTO n_a_goods_history(FK_Goods, TypeApp, SerialNumber, FK_Lending, FK_Outwards, FK_RETURN, FK_Maintenance, FK_Disposal, FK_LOST, CreatedDate, CreatedBy) 
							 VALUES (%(FK_Goods)s,%(TypeApp)s, %(SerialNumber)s, NULL,NULL, NULL, NULL, NULL, %(fk_lost)s, NOW(), %(CreatedBy)s )"""
					
                    param = {'FK_Goods': data['fk_goods'], 'TypeApp': data['typeApp'],
                             'SerialNumber': data['serialnumber'], 'fk_lost': FKApp, 'CreatedBy': data['createdby']}
                    cur.execute(Query, param)
                elif statusForm == StatusForm.Edit:
                    Params['IDApp'] = data['idapp']
                    Params['ModifiedDate'] = data['modifieddate']
                    Params['ModifiedBy'] = data['modifiedby']
                    Params['Status'] = data['status_goods']
                    who = data['modifiedby']
                    Query = """UPDATE n_a_goods_lost SET fk_goods=%(FK_Goods)s, fromgoods=%(FK_FromGoods)s, serialnumber=%(SerialNumber)s,typeapp=%(TypeApp)s,
                    fk_goods_outwards=%(FK_Goods_Outwards)s, fk_goods_lending=%(FK_Goods_Lending)s, fk_goods_return = %(FK_Goods_Return)s,fk_maintenance=%(FK_Maintenance)s,fk_lostby=%(FK_LostBy)s,fk_usedby = %(FK_UsedBy)s,fk_responsiblepersoon=%(FK_ResponsiblePerson)s,
                    status=%(Status)s,descriptions=%(Descriptions)s, modifieddate=%(ModifiedDate)s,modifiedby=%(ModifiedBy)s
                    WHERE idapp = %(IDApp)s"""
                    cur.execute(Query,Params)
                    FKApp = cur.lastrowid
                #update stock
                #return(totalNew, totalReceived, totalUsed, totalReturn, totalRenew, totalMaintenance, TotalSpare,totalBroken,totalDisposal,totalLost)
                TStock = commonFunct.getTotalGoods(data['fk_goods'], cur, who)
                totalLost = TStock[9]
                #Update n_a_stock
                Query = """UPDATE n_a_stock SET TIslost=%(T_Lost)s,ModifiedDate=NOW(),ModifiedBy=%(ModifiedBy)s WHERE IDApp = %(fk_stock)s"""
                param = {'T_Lost': totalLost, 'fk_stock':fk_stock,  'ModifiedBy': who}
                cur.execute(Query, param)
                cur.close()
                return ('success', FKApp)
        except Exception as e:
            cur.close()
            return repr(e)
    #Rimba pinjam laptop dell KN7841, sudah dikembalikan

    """DROP TEMPORARY TABLE IF EXISTS T_GoodsLost_Manager;
CREATE TEMPORARY TABLE T_GoodsLost_Manager ENGINE=InnoDB AS (SELECT gls.idapp, gls.fk_goods, gls.fk_fromgoods, gls.serialnumber,gls.fk_goods_outwards,gls.fk_goods_lending,empl1.fk_employee,
        gls.datelost, gls.reason, gls.descriptions, gls.createddate, gls.createdby, CONCAT(g.goodsname, ' ',g.brandname, ' ',gls.typeapp) as goods, g.itemcode FROM
        n_a_goods_lost gls INNER JOIN n_a_goods g ON gls.fk_goods = g.idapp INNER JOIN n_a_goods_lending ngl ON gls.FK_Goods_Lending = ngl.idapp LEFT OUTER JOIN (SELECT idapp,employee_name AS fk_employee FROM employee) AS empl1 ON ngl.FK_Employee=empl1.idapp);
SELECT * FROM T_GoodsLost_Manager;"""


    #Query_old = """CREATE TEMPORARY TABLE T_goods_byForm ENGINE=InnoDB AS (SELECT * FROM (SELECT ngo.idapp, g.itemcode,@table_name := 'GO' AS tbl_name,
    #    CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,grd.serialnumber,empl1.idapp as used_idapp, empl2.fk_responsibleperson,empl1.used_by,
    #    empl2.empl_resp, empl1.used_nik, empl2.resp_nik FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr 
    #    ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngo.serialnumber = grd.serialnumber LEFT OUTER JOIN 
    #    (SELECT idapp,nik AS used_nik, employee_name AS used_by FROM employee) as empl1 ON empl1.idapp = ngo.fk_employee LEFT OUTER JOIN 
    #    (SELECT idapp AS fk_responsibleperson,nik as resp_nik , employee_name AS empl_resp FROM employee) AS empl2 ON empl2.fk_responsibleperson = ngo.fk_responsibleperson 
    #    WHERE (SELECT COUNT(ngo.idapp))UNION SELECT ngl.idapp, g.itemcode,@table_name := 'GL' AS tbl_name, CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,
    #    grd.serialnumber,empl1.idapp as used_idapp, empl2.fk_responsibleperson,empl1.used_by, empl2.empl_resp, empl1.used_nik, empl2.resp_nik FROM 
    #    n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN 
    #    n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngl.serialnumber = grd.serialnumber LEFT OUTER JOIN (SELECT idapp,nik AS used_nik,
    #    employee_name AS used_by FROM employee) as empl1 ON empl1.idapp = ngl.fk_employee LEFT OUTER JOIN (SELECT idapp AS fk_responsibleperson,nik as resp_nik , employee_name AS empl_resp FROM employee) 
    #    AS empl2 ON empl2.fk_responsibleperson = ngl.fk_responsibleperson WHERE ngl.status='L') Inner_Tbl)"""
    def searchGoods_byForm(self,data):
        cur = connection.cursor()
        if data['tab_section'] == 'g_outwards':
            Query = """SELECT ngo.idapp,ngo.fk_goods, g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,@table_name := 'GO' AS tbl_name, ngo.serialnumber,
                        empl1.fk_employee,empl1.nik_employee,empl1.employee_name as used_employee,empl2.fk_resp,empl2.nik_resp,empl2.employee_name AS employee_responsible FROM n_a_goods_outwards ngo INNER JOIN n_a_goods g ON ngo.fk_goods = g.idapp INNER JOIN n_a_goods_receive ngr 
                        ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND ngo.serialnumber = grd.serialnumber
                        LEFT OUTER JOIN (SELECT idapp AS fk_employee, nik AS nik_employee,employee_name FROM employee) 
                        AS empl1 ON ngo.fk_employee = empl1.fk_employee LEFT OUTER JOIN (SELECT idapp AS fk_resp, nik AS nik_resp,employee_name  FROM employee) AS empl2 ON ngo.fk_responsibleperson = empl2.fk_resp
                        WHERE NOT EXISTS(SELECT m.serialnumber FROM n_a_maintenance m WHERE m.serialnumber=ngo.serialnumber AND m.isfinished=0) AND 
                        NOT EXISTS(SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=ngo.serialnumber)
                        AND ((CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) LIKE \'{0}\') OR(ngo.serialnumber LIKE \'{1}\'))
                    """
            result = 'g_outwards'
        elif data['tab_section'] == 'g_lending':
            Query = """SELECT ngl.idapp,ngl.fk_goods, g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,ngl.serialnumber,@table_name := 'GL' AS tbl_name,
                        empl1.fk_employee,empl1.nik_employee,empl1.employee_name as used_employee,empl2.fk_resp,empl2.nik_resp,empl2.employee_name AS employee_responsible FROM n_a_goods_lending ngl INNER JOIN n_a_goods g ON ngl.fk_goods = g.idapp INNER JOIN 
                        n_a_goods_receive ngr ON g.idapp = ngr.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ngr.idapp = grd.fk_app AND 
                        ngl.serialnumber = grd.serialnumber LEFT OUTER JOIN (SELECT idapp AS fk_employee, nik AS nik_employee,employee_name FROM employee) 
                        AS empl1 ON ngl.fk_employee = empl1.fk_employee LEFT OUTER JOIN (SELECT idapp AS fk_resp, nik AS nik_resp,employee_name  FROM employee) AS empl2 ON ngl.fk_responsibleperson = empl2.fk_resp
                        WHERE NOT EXISTS(SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=ngl.serialnumber) AND ((CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) LIKE \'{0}\') OR(ngl.serialnumber LIKE \'{1}\'))
                        AND ngl.status = 0
                    """
            result = 'g_lending'
        elif data['tab_section'] == 'g_return':
            Query = """SELECT ngr.idapp,ngr.fk_goods, g.itemcode,CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) as goods,ngr.serialnumber,@table_name := 'GR' AS tbl_name,
                        empl1.fk_employee,empl1.nik_employee,empl1.employee_name as from_employee,empl2.fk_usedemployee,empl2.nik_used,empl2.employee_name AS used_employee,ngr.datereturn,ngr.iscompleted,ngr.minusdesc FROM n_a_goods_return ngr INNER JOIN n_a_goods g ON ngr.fk_goods = g.idapp INNER JOIN 
                        n_a_goods_receive ng ON g.idapp = ng.fk_goods INNER JOIN n_a_goods_receive_detail grd ON ng.idapp = grd.fk_app AND 
                        ngr.serialnumber = grd.serialnumber LEFT OUTER JOIN (SELECT idapp AS fk_employee, nik AS nik_employee,employee_name FROM employee) 
                        AS empl1 ON ngr.fk_fromemployee = empl1.fk_employee LEFT OUTER JOIN (SELECT idapp AS fk_usedemployee, nik AS nik_used,employee_name FROM employee) AS empl2 ON ngr.fk_usedemployee = empl2.fk_usedemployee
                        WHERE NOT EXISTS(SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=ngr.serialnumber) AND ((CONCAT(g.goodsname, ' ',g.brandname, ' ',grd.typeapp) LIKE \'{0}\') OR(ngr.serialnumber LIKE \'{1}\'))
                        AND ngr.IsAccepted = 0
                    """
            result = 'g_return'
        elif data['tab_section'] == 'g_maintenance':
            Query = """SELECT m.idapp, m.fk_goods, g.itemcode, m.fk_goods, m.typeapp, m.serialnumber, @table_name := 'GM' AS tbl_name,
                        CONCAT(g.goodsname, ' ', g.brandname, ' ', m.typeapp) AS goods FROM n_a_maintenance m INNER JOIN n_a_goods g ON
                        m.fk_goods = g.idapp WHERE NOT EXISTS (SELECT gls.idapp FROM n_a_goods_lost gls WHERE gls.serialnumber=m.serialnumber) AND
                        ((m.isfinished=0 AND CONCAT(g.goodsname, ' ',g.brandname, ' ',m.typeapp) LIKE \'{0}\') OR(m.serialnumber LIKE \'{1}\'))
                    """
            result = 'g_maintenance'
        cur.execute(Query.format(
            '%'+data['goods_filter']+'%', '%'+data['goods_filter']+'%'))
        result = (result,query.dictfetchall(cur))
        connection.close()
        return result

    def retriveData(self,idapp):
        cur = connection.cursor()
        if self.dataExist(idapp=idapp):
            Query = """SELECT gls.idapp, gls.fk_goods,g.itemcode, CONCAT(g.goodsname, ' ',grd.brandname) AS goods, grd.typeApp, gls.serialNumber,gls.datelost,empl1.fk_usedby, empl1.nik_used, empl1.empl_used,empl2.fk_responsibleperson,empl2.nik_resp,
                    empl2.empl_resp,empl3.fk_lostby,empl3.nik_lostby, empl3.empl_lostby,gls.fromgoods AS fk_fromgoods,gls.status AS status_goods,gls.reason,gls.fk_goods_lending,gls.fk_goods_outwards,gls.fk_goods_return,gls.fk_maintenance, gls.descriptions FROM n_a_goods_lost gls INNER JOIN n_a_goods g ON 
                    gls.fk_goods = g.idapp INNER JOIN n_a_goods_receive_detail grd ON gls.serialnumber=grd.serialnumber  LEFT OUTER JOIN (SELECT idapp AS fk_usedby,nik AS nik_used,employee_name as empl_used FROM employee) AS empl1 ON gls.fk_usedby = empl1.fk_usedby
                    LEFT OUTER JOIN (SELECT idapp AS fk_responsibleperson, nik AS nik_resp, employee_name AS empl_resp FROM employee) AS empl2 ON gls.fk_responsibleperson = empl2.fk_responsibleperson 
                    LEFT OUTER JOIN (SELECT idapp AS fk_lostby, nik AS nik_lostby, employee_name AS empl_lostby FROM employee) AS empl3 ON gls.fk_lostby = empl3.fk_lostby
                    WHERE gls.idapp = %s"""
            cur.execute(Query, [idapp])
            if cur.rowcount > 0:
                result = query.dictfetchall(cur)[0]
                return ('success', result)
            else:
                return ('unknown result',)
        else:
            return ('Lost',)

    def dataExist(self,**kwargs):
        data = super(NA_BR_GoodsLost, self).get_queryset()
        if 'idapp' in kwargs:
            data = data.filter(idapp=kwargs['idapp']).values('idapp')
        if 'serialnumber' in kwargs:
            data = data.filter(serialnumber=kwargs['serialnumber'])
        if 'status' in kwargs:
            data = data.filter(status=kwargs['status'])
        return data.exists()
