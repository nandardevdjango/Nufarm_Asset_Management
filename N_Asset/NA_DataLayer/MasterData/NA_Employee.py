﻿from datetime import datetime
from django.db.models import Q
from django.db import models, connection, transaction
from NA_DataLayer.common import (CriteriaSearch, DataType, StatusForm,
                                 Data, Message, commonFunct, ResolveCriteria)
from ..logging import LogActivity


class NA_BR_Employee(models.Manager):
    def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like,
                      typeofData=DataType.VarChar):
        employeeData = super(NA_BR_Employee, self).get_queryset()\
            .values('idapp', 'nik', 'employee_name', 'typeapp', 'jobtype', 'gender',
                    'status', 'telphp', 'territory', 'descriptions', 'inactive',
                    'createddate', 'createdby')
        filterfield = columnKey
        if criteria == CriteriaSearch.NotEqual or criteria == CriteriaSearch.NotIn:
            if criteria == CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            employeeData = employeeData.exclude(**{filterfield: [ValueKey]})
        if criteria == CriteriaSearch.Equal:
            employeeData = employeeData.filter(**{filterfield: ValueKey})
        elif criteria == CriteriaSearch.Greater:
            filterfield = columnKey + '__gt'
        elif criteria == CriteriaSearch.GreaterOrEqual:
            filterfield = columnKey + '__gte'
        elif criteria == CriteriaSearch.In:
            filterfield = columnKey + '__in'
        elif criteria == CriteriaSearch.Less:
            filterfield = columnKey + '__lt'
        elif criteria == CriteriaSearch.LessOrEqual:
            filterfield = columnKey + '__lte'
        elif criteria == CriteriaSearch.Like:
            filterfield = columnKey + '__icontains'
            employeeData = employeeData.filter(
                **{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if criteria == CriteriaSearch.Beetween or criteria == CriteriaSearch.BeginWith or \
           criteria == CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
            employeeData = employeeData.filter(**rs.DefaultModel())
        return employeeData

    def SaveData(self, statusForm=StatusForm.Input, **data):
        cur = connection.cursor()
        Params = {
            'Nik': data['nik'],
            'Employee_Name': data['employee_name'],
            'TypeApp': data['typeapp'],
            'JobType': data['jobtype'],
            'Gender': data['gender'],
            'Status': data['status'],
            'Telphp': data['telphp'],
            'Territory': data['territory'],
            'Inactive': data['inactive'],
            'Descriptions': data['descriptions']
        }
        if statusForm == StatusForm.Input:
            is_exists = self.dataExist(nik=data['nik'], telphp=data['telphp'])
            if is_exists[0]:
                return (Data.Exists, is_exists[1])
            Params['CreatedDate'] = data['createddate']
            Params['CreatedBy'] = data['createdby']
            Query = """INSERT INTO employee(nik, employee_name, typeapp, jobtype, gender,
			status, telphp, territory, inactive, descriptions,createddate, createdby)
			VALUES({})""".format(','.join('%(' + i + ')s' for i in Params))
        elif statusForm == StatusForm.Edit:
            Params['ModifiedDate'] = data['modifieddate']
            Params['ModifiedBy'] = data['modifiedby']
            Params['IDApp'] = data['idapp']
            Query = """UPDATE employee SET
            nik=%(Nik)s,
            employee_name=%(Employee_Name)s,
            typeapp=%(TypeApp)s,
            jobtype=%(JobType)s,
            gender=%(Gender)s,
            status=%(Status)s,
            telphp=%(Telphp)s,
            territory=%(Territory)s,
            descriptions=%(Descriptions)s,
            inactive=%(Inactive)s,
            modifieddate=%(ModifiedDate)s,
            modifiedby=%(ModifiedBy)s
            WHERE idapp = %(IDApp)s"""
        cur.execute(Query, Params)
        if statusForm == StatusForm.Edit:
            logging = LogActivity(
                models=self.model,
                activity='Updated',
                user=data['modifiedby'],
                data={
                    'Nik': data['nik']
                }
            )
        else:
            logging = LogActivity(
                models=self.model,
                activity='Created',
                user=data['createdby'],
                data={
                    'Nik': data['nik']
                }
            )
        logging.record_activity()
        row = cur.fetchone()
        # connection.close()
        return (Data.Success, row)

    def delete_employee(self, **kwargs):
        get_idapp = kwargs['idapp']
        NA_User = kwargs['NA_User']
        if self.dataExist(idapp=get_idapp):
            if self.hasRef(get_idapp):
                return (Data.HasRef, Message.HasRef_del.value)
            else:
                cur = connection.cursor()
                # ============== INSERT INTO LOG EVENT ================
                data = self.retriveData(get_idapp, False)[1]
                dataPrms = {
                    'Nik': data['nik'],
                    'Employee_Name': data['employee_name'],
                    'Typeapp': data['typeapp'],
                    'Jobtype': data['typeapp'],
                    'Gender': data['gender'],
                    'Status': data['status'],
                    'Telphp': data['telphp'],
                    'Territory': data['territory'],
                    'Descriptions': data['descriptions'],
                    'Inactive': data['inactive']
                }
                createddate = data['createddate']
                modifieddate = data.get('modifieddate')
                if isinstance(createddate, datetime):
                    dataPrms['CreatedDate'] = createddate.strftime(
                        '%d %B %Y %H:%M:%S')
                dataPrms['CreatedBy'] = data['createdby']
                if modifieddate is not None:
                    dataPrms['ModifiedDate'] = modifieddate
                    dataPrms['ModifiedBy'] = data['modifiedby']

                Query = """INSERT INTO logevent (nameapp,descriptions,createddate,createdby)
				VALUES(\'Deleted Employee\',
				JSON_OBJECT(\'deleted\',JSON_ARRAY({})),NOW(),""".format(
                    ','.join('%(' + i + ')s' for i in dataPrms)
                )
                dataPrms['NA_User'] = NA_User
                Query = Query + "%(NA_User)s)"
                with transaction.atomic():
                    cur.execute(Query, dataPrms)
                    # ============= End INSERT INTO LOG EVENT ==============
                    cur.execute(
                        '''DELETE FROM employee WHERE idapp=%s''', [get_idapp])
                    cur.close()
                return (Data.Success, Message.Success.value)
        else:
            return (Data.Lost, Message.get_lost_info(get_idapp))

    def active(self):
        return super(NA_BR_Employee, self).filter(inactive=0)

    def retriveData(self, get_idapp, must_check=True):
        def get_data():
            return super(NA_BR_Employee, self).get_queryset()\
                .filter(idapp__exact=get_idapp)\
                .values('idapp', 'nik', 'employee_name', 'typeapp', 'jobtype', 'gender',
                        'status', 'telphp', 'territory', 'descriptions',
                        'inactive', 'createddate', 'createdby')
        if must_check:
            if self.dataExist(idapp=get_idapp):
                return (Data.Success, get_data()[0])
            else:
                return (Data.Lost, Message.get_lost_info(pk=get_idapp, table='employee'))
        else:
            return (Data.Success, get_data()[0])

    def existByNIK(self, NIK):
        return super(NA_BR_Employee, self).get_queryset().filter(nik=NIK).exists()

    def dataExist(self, **kwargs):
        idapp = kwargs.get('idapp')
        #status_form = kwargs.get('status_form')
        if idapp is not None:
            return super(NA_BR_Employee, self).get_queryset().filter(idapp=idapp).exists()
        nik = kwargs.get('nik')
        if nik is not None:
            is_nik = super(NA_BR_Employee, self).get_queryset().filter(
                nik=nik).exists()
            if is_nik:
                return (True, Message.get_specific_exists('Employee', 'Nik', nik))
        telphp = kwargs.get('telphp')
        if telphp is not None:
            is_telp = super(NA_BR_Employee, self).get_queryset().filter(
                Q(telphp=telphp) & Q(inactive=0)).exists()
            if is_telp:
                return (True, Message.get_specific_exists('Employee', 'Telp/HP', telphp))
        return (False,)

    def hasRef(self, idapp):
        cur = connection.cursor()
        Query = """SELECT EXISTS(SELECT idapp FROM n_a_goods_lending
		WHERE fk_employee=%(IDApp)s
		OR fk_responsibleperson=%(IDApp)s OR fk_sender=%(IDApp)s
		UNION
		SELECT idapp FROM n_a_goods_outwards WHERE fk_employee=%(IDApp)s OR
		fk_responsibleperson=%(IDApp)s
		OR fk_sender=%(IDApp)s OR fk_usedemployee=%(IDApp)s)"""
        cur.execute(Query, {'IDApp': idapp})
        if cur.fetchone()[0] > 0:
            cur.close()
            return True
        else:
            cur.close()
            return False

    def setInActive(self, idapp, inactive):
        if self.dataExist(idapp=idapp):
            data = super(NA_BR_Employee, self).get_queryset().values(
                'inactive').filter(idapp=idapp)
            if commonFunct.str2bool(data[0]['inactive']) == inactive:
                return (Data.Changed, Message.has_update_by_other(pk=idapp, table='employee'))
            else:
                data.update(inactive=inactive)
                return (Data.Success,)
        else:
            return (Data.Lost, Message.get_lost_info(pk=idapp, table='employee'))

    def getEmloyeebyForm(self, q):
        data = self.active()\
            .values('idapp', 'nik', 'employee_name')\
            .filter(
            Q(nik__icontains=q) |
            Q(employee_name__icontains=q)
        )
        if data.exists():
            return data
        else:
            return Data.Empty

    def getJobType(self, search):
        return super(NA_BR_Employee, self).get_queryset().filter(jobtype__icontains=search).values('jobtype').distinct()

    def getTerritories(self, search):
        return super(NA_BR_Employee, self).get_queryset().filter(territory__icontains=search).values('territory').distinct()
