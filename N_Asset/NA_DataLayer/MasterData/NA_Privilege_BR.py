from django.contrib.auth.models import UserManager
from NA_DataLayer.common import (ResolveCriteria, CriteriaSearch, DataType,
                                 query, Data)
from django.db import connection


class NA_BR_Privilege(UserManager):
    def PopulateQuery(self, columnKey, ValueKey, criteria=CriteriaSearch.Like, typeofData=DataType.VarChar):
        privilegeData = super(NA_BR_Privilege, self).get_queryset()\
            .values('idapp', 'first_name', 'last_name', 'username', 'divisi', 'role',
                    'email', 'password', 'last_login', 'last_form', 'is_active',
                    'date_joined', 'createdby')
        filterfield = columnKey
        if criteria == CriteriaSearch.NotEqual or criteria == CriteriaSearch.NotIn:
            if criteria == CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            privilegeData = privilegeData.exclude(
                **{filterfield: [ValueKey]})
        if criteria == CriteriaSearch.Equal:
            privilegeData = privilegeData.filter(**{filterfield: ValueKey})
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
            filterfield = columnKey + '__contains'
            privilegeData = privilegeData.filter(
                **{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if criteria == CriteriaSearch.Beetween or criteria == CriteriaSearch.BeginWith or criteria == CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria, typeofData, columnKey, ValueKey)
            privilegeData = privilegeData.filter(**rs.DefaultModel())
        return privilegeData

    def Get_Privilege_Sys(self, user_id):
        cur = connection.cursor()
        Query = """SELECT ps.idapp, pf.form_name, ps.permission, ps.inactive, ps.createddate,
        ps.createdby FROM n_a_sys_privilege ps INNER JOIN n_a_privilege_form pf ON
        ps.fk_pform = pf.idapp WHERE ps.user_id=%(User_id)s ORDER BY pf.form_name_ori"""
        cur.execute(Query, {'User_id': user_id})
        return query.dictfetchall(cur)

    def Delete(self, idapp):
        data = super(NA_BR_Privilege, self).get_queryset().filter(idapp=idapp)
        data.delete()
        return (Data.Success,)

    def retrieveData(self, idapp):
        data = super(NA_BR_Privilege, self).get_queryset()\
            .values('idapp', 'first_name', 'last_name', 'username', 'divisi', 'role', 'email')\
            .filter(idapp=idapp)
        return data[0]
