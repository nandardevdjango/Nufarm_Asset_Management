from django.db import models
from NA_DataLayer.common import *
from django.db import transaction;
from django.db import connection
from decimal import Decimal
from django.db.models import Q
from NA_DataLayer.common import commonFunct
from distutils.util import strtobool
class NA_BR_Goods_Outwards(models.Manager):
    def PopulateQuery(self,orderFields,sortIndice,pageSize,PageIndex,userName,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        colKey = ''
        rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
        """ ==========CAN di perbaiki =========================
                    SELECT nga.idapp,g.goodsname AS goods,ngd.TypeApp AS goodstype,ngd.serialnumber,nga.daterequest,nga.datereleased,
            nga.isnew,nga.fk_employee,e.employee_name as for_employee,nga.fk_usedemployee,
            CASE 
               WHEN(nga.fk_usedemployee IS NOT NUll) THEN(SELECT employee_name FROM `employee` WHERE idapp = nga.fk_usedemployee LIMIT 1)
	            END AS eks_employee,fk_responsible_person,
            responsible_by,emp1.responsible_by,nga.fk_sender,emp2.senderby,nga.fk_stock,
            ref.refgoodsfrom,nga.createdby,nga.createddate,nga.descriptions
            FROM n_a_goods_outwards nga INNER JOIN n_a_goods g ON g.IDApp = nga.FK_Goods
            INNER JOIN n_a_goods_receive ngr ON ngr.FK_goods = nga.FK_Goods
            INNER JOIN n_a_goods_receive_detail ngd ON ngd.FK_App = ngr.IDApp
            INNER JOIN (SELECT ng.IDApp,CASE
						            WHEN (ng.FK_Receive IS NOT NULL) THEN 'Receive PR (New)'
						            WHEN (ng.FK_RETURN IS NOT NULL) THEN 'RETURN Eks Employee'
						            WHEN (ng.FK_Maintenance IS NOT NULL) THEN 'Service(Maintenance)'
						            WHEN (ng.FK_CurrentApp IS NOT NULL) THEN 'RETURN (After being Lent)'
						            ELSE 'Other (Uncategorized)'
						            END AS refgoodsfrom FROM n_a_goods_lending ngl)ref ON Ref.IDApp = ngl.IDApp"""