from django.db import models, connection
from NA_DataLayer.common import (CriteriaSearch, DataType, StatusForm,
                                 ResolveCriteria, Data, Message, query)


class NABRGoodsOutwardsGA(models.Manager):

    def populate_query(self, columnKey, ValueKey, criteria=CriteriaSearch.Like,
                       typeofData=DataType.VarChar):
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        cur = connection.cursor()

        query_string = """
        SELECT eq.nameapp, equipment.nagaoutwards_id
        FROM n_a_equipment AS eq INNER JOIN n_a_ga_outwards_equipment
        AS equipment ON eq.idapp = equipment.nagoodsequipment_id
        """

        # query_string = """
        # SELECT eq.nameapp, add_equipment.nagaoutwards_id
        # FROM n_a_equipment AS eq INNER JOIN n_a_ga_outwards_add_equipment
        # AS add_equipment ON eq.idapp = add_equipment.nagoodsequipment_id
        # """

        query_string = """
        CREATE TEMPORARY TABLE IF NOT EXISTS T_Outwards_GA ENGINE=InnoDB AS(
        SELECT ngo.idapp, ngo.typeapp, ngo.isnew, ngo.daterequest,
        ngo.datereleased, ngo.lastinfo, ngo.descriptions, g.goodsname,
        emp1.employee_name, emp2.employee_name AS used_employee,
        emp3.employee_name AS resp_employee, emp4.employee_name AS sender,
        eq.nameapp AS equipment
        FROM n_a_ga_outwards AS ngo
        LEFT OUTER JOIN
        (SELECT idapp, goodsname FROM n_a_goods) AS g ON ngo.fk_goods = g.idapp
        LEFT OUTER JOIN
        (SELECT idapp, employee_name FROM employee) AS emp1
        ON ngo.fk_employee = emp1.idapp
        LEFT OUTER JOIN
        (SELECT idapp, employee_name FROM employee) AS emp2
        ON ngo.fk_usedemployee = emp2.idapp
        LEFT OUTER JOIN
        (SELECT idapp, employee_name FROM employee) AS emp3
        ON ngo.fk_responsibleperson = emp3.idapp
        LEFT OUTER JOIN
        (SELECT idapp, employee_name FROM employee) AS emp4
        ON ngo.fk_sender = emp4.idapp
         """ + ")"

        cur.execute(query_string)
        query_string = """
        SELECT * FROM T_Outwards_GA
        """
        cur.execute(query_string)
        result = query.dictfetchall(cur)
        cur.execute('DROP TEMPORARY TABLE T_Outwards_GA')
        return result

    def search_ga_by_form(self, q):
        cur = connection.cursor()
        query_string = """
        SELECT g.idapp, CONCAT(g.goodsname, ' ', ngr.brand, ' ', ngr.model) AS goods,
        g.itemcode, ngh.reg_no, ngh.expired_reg, ngh.bpkb_expired, ngr.descriptions,
        ngr.idapp AS fk_receive, ngh.idapp AS fk_app, ngr.typeapp, ngr.invoice_no,
        DATE_FORMAT(ngr.year_made,'%%Y') AS year_made, ngr.colour,
        CASE
            WHEN(
                SELECT EXISTS(
                    SELECT ngo.idapp FROM n_a_ga_outwards ngo WHERE ngo.fk_app = ngh.idapp
                )
            )
            THEN '0'
            ELSE '1'
            END AS info_is_new
        FROM n_a_ga_receive ngr INNER JOIN
        n_a_goods g ON ngr.fk_goods = g.idapp INNER JOIN n_a_ga_vn_history ngh
        ON ngr.idapp = ngh.fk_app
        WHERE """

        query_string += query.like(
            query_param='q',
            fields=[
                'g.itemcode',
                'g.goodsname',
                'ngr.brand',
                'ngr.model',
                'ngh.reg_no',
                'ngr.typeapp',
                'ngr.invoice_no'
            ]
        )

        cur.execute(query_string, {
            'q': ('%' + q + '%')
        })
        return query.dictfetchall(cur)
