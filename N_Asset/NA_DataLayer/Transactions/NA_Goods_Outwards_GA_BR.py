from django.db import models, connection
from NA_DataLayer.common import (CriteriaSearch, DataType, StatusForm,
                                 ResolveCriteria, Data, Message, query)


class NABRGoodsOutwardsGA(models.Manager):

    def populate_query(self, columnKey, ValueKey, criteria=CriteriaSearch.Like,
                       typeofData=DataType.VarChar):
        rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
        cur = connection.cursor()
        employee_temp_list = [
            'employee_temp1',
            'employee_temp2',
            'employee_temp3',
            'employee_temp4'
        ]
        query_string = """
        CREATE TEMPORARY TABLE {table_name} ENGINE=InnoDB AS
        (SELECT idapp, employee_name FROM employee)
        """
        for table_name in employee_temp_list:
            cur.execute(
                query_string.format(table_name=table_name)
            )

        query_string = """
        CREATE TEMPORARY TABLE IF NOT EXISTS T_Outwards_GA ENGINE=InnoDB AS(
        SELECT ngo.idapp, ngo.typeapp, ngo.isnew, ngo.daterequest,
        ngo.datereleased, ngo.lastinfo, ngo.descriptions, ngo.equipment,
        ngo.add_equipment, g.goodsname,
        emp1.employee_name, emp2.employee_name AS used_employee,
        emp3.employee_name AS resp_employee, emp4.employee_name AS sender
        FROM n_a_ga_outwards AS ngo
        LEFT OUTER JOIN
        (SELECT idapp, goodsname FROM n_a_goods) AS g ON ngo.fk_goods = g.idapp
        LEFT OUTER JOIN
        employee_temp1 AS emp1
        ON ngo.fk_employee = emp1.idapp
        LEFT OUTER JOIN
        employee_temp2 AS emp2
        ON ngo.fk_usedemployee = emp2.idapp
        LEFT OUTER JOIN
        employee_temp3 AS emp3
        ON ngo.fk_responsibleperson = emp3.idapp
        LEFT OUTER JOIN
        employee_temp4 AS emp4
        ON ngo.fk_sender = emp4.idapp
         """ + ")"

        cur.execute(query_string)
        query_string = """
        SELECT * FROM T_Outwards_GA
        """
        result = query.dictfetchall(cur)
        employee_temp_list = ",".join(employee_temp_list)
        query_string = """
        DROP TEMPORARY TABLE IF EXISTS
        """ + employee_temp_list
        """
        buat function untuk cek ..!!!
        dicek di log_event, apakah ada yg merubah
        data employee, jika ada: maka delete temporary table
        """
        cur.execute(query_string)
        return result

    def search_ga_by_form(self, q):
        cur = connection.cursor()
        query_string = """
        SELECT ngr.idapp, CONCAT(g.goodsname, ngr.brand, ngr.model) AS goods,
        ngh.reg_no, ngh.expired_reg, ngh.bpkb_expired, ngr.descriptions,
        CASE
            WHEN(
                SELECT EXISTS(
                    SELECT ngo.idapp FROM n_a_ga_outwards ngo WHERE ngo.fk_app = ngh.idapp
                )
            )
            THEN '1'
            ELSE '0'
            END AS info_is_new
        FROM n_a_ga_receive ngr INNER JOIN
        n_a_goods g ON ngr.fk_goods = g.idapp INNER JOIN n_a_ga_vn_history ngh
        ON ngr.idapp = ngh.fk_app
        """

        cur.execute(query_string)
        return query.dictfetchall(cur)
