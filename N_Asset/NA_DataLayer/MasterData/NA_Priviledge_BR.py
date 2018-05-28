from django.contrib.auth.models import UserManager
from NA_DataLayer.common import (ResolveCriteria,CriteriaSearch, DataType,
                                 query)
from django.db import connection



class NA_BR_Priviledge(UserManager):
    def PopulateQuery(self,columnKey,ValueKey,criteria=CriteriaSearch.Like,typeofData=DataType.VarChar):
        priviledgeData = None
        filterfield = columnKey
        if criteria==CriteriaSearch.NotEqual or criteria==CriteriaSearch.NotIn:
            if criteria==CriteriaSearch.NotIn:
                filterfield = columnKey + '__in'
            else:
                filterfield = columnKey + '__iexact'
            priviledgeData = super(NA_BR_Priviledge,self).get_queryset().exclude(**{filterfield:[ValueKey]})
        if criteria==CriteriaSearch.Equal:
            return super(NA_BR_Priviledge,self).get_queryset().filter(**{filterfield: ValueKey})
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
            filterfield = columnKey + '__contains'
            priviledgeData = super(NA_BR_Priviledge,self).get_queryset().filter(**{filterfield: [ValueKey] if filterfield == (columnKey + '__in') else ValueKey})
        if criteria==CriteriaSearch.Beetween or criteria==CriteriaSearch.BeginWith or criteria==CriteriaSearch.EndWith:
            rs = ResolveCriteria(criteria,typeofData,columnKey,ValueKey)
            priviledgeData = super(NA_BR_Priviledge,self).get_queryset().filter(**rs.DefaultModel())

        priviledgeData = priviledgeData.values('idapp','username','email','password','last_login','last_form','is_active','date_joined','createdby')
        return priviledgeData

    def Get_Priviledge_Sys(self,user_id):
        cur = connection.cursor()
        Query = """SELECT ps.idapp,pf.form_name,ps.permission FROM n_a_sys_priviledge ps INNER JOIN n_a_priviledge_form pf ON ps.fk_pform = pf.idapp
        WHERE ps.user_id=%(User_id)s"""
        cur.execute(Query,{'User_id':user_id})
        return query.dictfetchall(cur)