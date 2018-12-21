from django.db import models, connection, transaction
from django.db.models import Exists, OuterRef, Value, CharField, F
from django.db.models.functions import Concat

from NA_DataLayer.common import CriteriaSearch, DataType, Data, query, ResolveCriteria


class NA_Acc_FA_BR(models.Manager):
    def PopulateQuery(self, columnKey, ValueKey, is_parent, serialnumber=None,
    criteria=CriteriaSearch.Like, typeofData=DataType.VarChar, sidx='idapp', sord='desc'):
        cur = connection.cursor()
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        Query = """
        SELECT ac.idapp, CONCAT(g.goodsname, ' ',g.brandname) as goods, ac.typeapp,
        g.itemcode, g.depreciationmethod, ac.serialnumber, ac.year, ac.startdate,
        ac.datedepreciation, ac.depr_expense, ac.depr_accumulation, ac.bookvalue,
        ac.createddate, ac.createdby FROM n_a_acc_fa ac
        INNER JOIN n_a_goods g ON ac.fk_goods = g.IDApp
        WHERE ac.IsParent = """ + str(is_parent) + " AND "
        if is_parent:
            Query = Query + columnKey + rs.Sql() + " ORDER BY " + sidx + ' ' + sord
        else:
            Query = Query + """ac.serialnumber = '{}'""".format(serialnumber)
        cur.execute(Query)
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

    def data_not_yet_generate(self, q):
        from NA_DataLayer.common import QuerysetHelper
        from NA_Models.models import NA_GoodsReceive_detail
        existed_data = self.get_queryset().filter(
            serialnumber=OuterRef('serialnumber')
        )
        goods_field = 'fk_app__idapp_fk_goods__{}'
        annotate_kwargs = {
            'idapp_detail_receive': F('idapp'),
            'startdate': F('fk_app__datereceived'),
            'fk_goods': F(goods_field.format('idapp')),
            'itemcode': F(goods_field.format('itemcode')),
            'economiclife': F(goods_field.format('economiclife')),
            'depreciationmethod': F(goods_field.format('depreciationmethod')),
            'existed_data': ~Exists(existed_data),
            'goods': Concat(
                goods_field.format('goodsname'),
                Value(' '),
                'brandname',
                Value(' '),
                'typeapp'
            )
        }
        fields = [
            'goods',
            goods_field.format('itemcode'),
            'serialnumber',
            goods_field.format('depreciationmethod')
        ]
        filter_kwargs = QuerysetHelper.filter_like(fields=fields, value=q)

        only_fields = [
            'idapp',
            goods_field.format('itemcode'),
            goods_field.format('goodsname'),
            'brandname',
            'typeapp',
            'serialnumber',
            'fk_app__datereceived',
            goods_field.format('depreciationmethod'),
            'priceperunit',
            goods_field.format('economiclife')
        ]
        result = (NA_GoodsReceive_detail.objects
                  .select_related('fk_app', 'fk_app__idapp_fk_goods')
                  .annotate(**annotate_kwargs)
                  .filter(filter_kwargs, existed_data=True)
                  .only(*only_fields))
        return result


    # search By Form
    def searchAcc_ByForm(self, q=None, idapp=None):
        # TODO: Change it with ORM (Subquery, Exist, When) and move it to models with
        # cache

        cur = connection.cursor()
        query_string = """
        CREATE TEMPORARY TABLE T_search_acc_fa ENGINE=InnoDB AS (
        SELECT gr.idapp,g.itemcode,
        CONCAT(g.goodsname, ' ',grd.brandname, ' ',IFNULL(grd.typeapp, ' ')) as goods,
        grd.serialnumber, gr.datereceived AS startdate, grd.idapp AS idapp_detail_receive,
        g.depreciationmethod, grd.priceperunit, g.economiclife, g.idapp AS fk_goods, grd.typeapp
        FROM n_a_goods g INNER JOIN n_a_goods_receive gr
        ON g.idapp = gr.fk_goods INNER JOIN n_a_goods_receive_detail grd
        ON gr.idapp = grd.fk_app WHERE NOT EXISTS (SELECT ac.fk_goods FROM n_a_acc_fa ac
        WHERE ac.serialnumber = grd.serialnumber)"""

        query_param = {}
        if q is not None:
            query_string = """
            CREATE TEMPORARY TABLE T_search_acc_fa ENGINE=InnoDB AS (
            SELECT gr.idapp,g.itemcode,
            CONCAT(g.goodsname, ' ',grd.brandname, ' ',IFNULL(grd.typeapp, 
            ' ')) as goods,
            grd.serialnumber, gr.datereceived AS startdate, grd.idapp AS 
            idapp_detail_receive,
            g.depreciationmethod, grd.priceperunit, g.economiclife, g.idapp AS 
            fk_goods, grd.typeapp
            FROM n_a_goods g INNER JOIN n_a_goods_receive gr
            ON g.idapp = gr.fk_goods INNER JOIN n_a_goods_receive_detail grd
            ON gr.idapp = grd.fk_app WHERE NOT EXISTS (SELECT ac.fk_goods FROM 
            n_a_acc_fa ac
            WHERE ac.serialnumber = grd.serialnumber) AND 
            CONCAT(g.goodsname, ' ',grd.brandname, ' ',IFNULL(grd.typeapp, ' '))
            LIKE %(q)s OR g.itemcode LIKE %(q)s OR grd.serialnumber LIKE %(q)s
            OR g.depreciationmethod LIKE %(q)s)"""

            query_param.update({
                'q': '%' + q + '%'
            })
            cur.execute(query_string, query_param)
            query_string = """
            SELECT * FROM T_search_acc_fa
            """
            query_param.clear()
        elif idapp is not None:
            if isinstance(idapp, list):
                idapp = ','.join(idapp)
                query_string += """
                 AND grd.idapp IN ({idapp})
                """.format(
                    idapp=idapp
                )
            else:
                query_string += """
                 AND grd.idapp = %(idapp_detail_receive)s
                """
                query_param.update({
                    'idapp_detail_receive': idapp
                })
            query_string += ")"
            cur.execute(query_string, query_param)  # create temporary table
            query_string = """SELECT * FROM T_search_acc_fa"""
            query_param.clear()

        cur.execute(query_string, query_param)
        result = query.dictfetchall(cur)
        query_string = """
        DROP TEMPORARY TABLE T_search_acc_fa
        """
        cur.execute(query_string)
        cur.close()
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

    def delete_data(self, **kwargs):
        super(NA_Acc_FA_BR, self).filter(**kwargs).delete()
        return (Data.Success, )
