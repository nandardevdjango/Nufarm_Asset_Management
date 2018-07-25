﻿from django.db import models, connection, transaction
from NA_DataLayer.common import CriteriaSearch, DataType, Data, query, ResolveCriteria
from django.db.models import F


class NA_Acc_FA_BR(models.Manager):
    def PopulateQuery(self, columnKey, ValueKey, is_parent, serialnumber=None,
    criteria=CriteriaSearch.Like, typeofData=DataType.VarChar, sidx='idapp', sord='desc'):
        cur = connection.cursor()
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        Query = """
        SELECT ac.idapp, CONCAT(g.goodsname, ' ',g.brandname, ' ',g.typeapp) as goods,
        g.itemcode, g.depreciationmethod, ac.serialnumber, ac.year, ac.startdate,
        ac.datedepreciation, ac.depr_expense, ac.depr_accumulation, ac.bookvalue,
        ac.createddate, ac.createdby FROM n_a_acc_fa ac
        INNER JOIN n_a_goods g ON ac.fk_goods = g.IDApp
        WHERE ac.IsParent = %(is_parent)s AND """
        query_param = {'is_parent': is_parent}
        if is_parent:
            Query = Query + columnKey + rs.Sql() + " ORDER BY " + sidx + ' ' + sord
        else:
            Query = Query + """ac.serialnumber = %(serial_number)s"""
            query_param.update({
                'serial_number': serialnumber
            })
        print(Query)
        cur.execute(Query, query_param)
        result = query.dictfetchall(cur)
        cur.close()
        return result

    def create_acc_FA(self, data):
        with transaction.atomic():
            cur = connection.cursor()
            cur.execute('''
            INSERT INTO n_a_acc_fa(FK_Goods, SerialNumber, TypeApp, Year, DateDepreciation,
            StartDate, Depr_Expense, Depr_Accumulation, BookValue, IsParent, CreatedDate,
            CreatedBy)
            VALUES {}'''.format(data))
        cur.close()
        return (Data.Success,)

    # retive data from jqGrid / status == Open
    def retriveData(self, IDApp):
        cur = connection.cursor()
        Query = """SELECT ac.fk_goods,g.itemcode,g.brandname,g.goodsname AS goods_name,
        ac.year,ac.startdate,
        DATE_ADD(ac.startdate, INTERVAL SUM(g.economiclife*12) MONTH) as enddate,
        CONCAT('Rp ',FORMAT(ac.depr_expense,2,'de_DE')) AS depr_expense,
        CONCAT('Rp ',FORMAT(ac.depr_accumulation,2,'de_DE')) AS depr_accumulation,
        CONCAT('Rp ',FORMAT(ac.bookvalue,2,'de_DE')) AS bookvalue,
        CONCAT('Rp ',FORMAT(g.priceperunit,2,'de_DE')) AS price,g.economiclife FROM n_a_acc_fa ac
        INNER JOIN n_a_goods g ON ac.fk_goods = g.idapp WHERE ac.idapp = %(IDApp)s"""
        Params = {'IDApp': IDApp}
        cur.execute(Query, Params)
        result = query.dictfetchall(cur)
        connection.close()
        return result

    # search By Form
    def searchAcc_ByForm(self, value):
        cur = connection.cursor()
        Query = """SELECT g.idapp,g.itemcode,
        CONCAT(g.goodsname, ' ',grd.brandname, ' ',IFNULL(g.typeapp, ' ')) as goods,
        grd.serialnumber, gr.datereceived AS startdate,
        g.depreciationmethod, grd.priceperunit, g.economiclife
        FROM n_a_goods g INNER JOIN n_a_goods_receive gr
        ON g.idapp = gr.fk_goods INNER JOIN n_a_goods_receive_detail grd
        ON gr.idapp = grd.fk_app WHERE NOT EXISTS (SELECT ac.fk_goods FROM n_a_acc_fa ac
        WHERE ac.serialnumber = grd.serialnumber) AND
        CONCAT(g.goodsname, ' ',grd.brandname, ' ',IFNULL(g.typeapp, ' ')) LIKE '%{0}%'
        """.format(value)
        cur.execute(Query)
        result = query.dictfetchall(cur)
        connection.close()
        return result

    # get goods data after click (select) data from above (search goods by form)
    def getGoods_data(self, IDApp):
        cur = connection.cursor()
        Query = """SELECT g.IDApp,grd.typeapp,CONCAT(g.goodsname, ' ',grd.brandname) as goods,
        g.economiclife,grd.priceperunit as price_orig,grd.serialnumber,
        CONCAT('Rp ',FORMAT(g.priceperunit,2,'de_DE')) as price_label,g.depreciationmethod
        AS depr_method,g.createddate AS startdate,DATE_ADD(g.createddate,
        INTERVAL SUM(g.economiclife*12) MONTH) as enddate FROM n_a_goods g
        INNER JOIN n_a_goods_receive gr ON g.idapp = gr.fk_goods INNER JOIN
        n_a_goods_receive_detail grd ON gr.idapp = grd.fk_app WHERE NOT EXISTS
        (SELECT ac.FK_Goods FROM n_a_acc_fa ac WHERE ac.serialnumber = grd.serialnumber)
        AND g.IDApp = %s"""
        cur.execute(Query, [IDApp])
        result = query.dictfetchall(cur)
        connection.close()
        return result
