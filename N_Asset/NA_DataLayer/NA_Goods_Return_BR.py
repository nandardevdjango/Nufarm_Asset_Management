from django.db import models, connection

class NA_BR_Goods_Return(models.Manager):
    def PopulateQuery(self):
        cur = connection.cursor()
        Query = """SELECT ngr.idapp,ng.condition,ngr.iscompleted,ngr.minus,g.goodsname,ngr.typeapp,ngr.serialnumber
        FROM n_a_goods_return ngr INNER JOIN n_a_goods g ON ngr.fk_goods = g.idapp"""
        pass