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

    #var mydata = [
    #    { id: "1", state: "Texas",      city: "Houston",       attraction: "NASA",               zip: "77058", attr: {country: {rowspan: "5"},    state: {rowspan: "5"}} },
    #    { id: "2", state: "Texas",      city: "Austin",        attraction: "6th street",         zip: "78704", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "3", state: "Texas",      city: "Arlinton",      attraction: "Cowboys Stadium",    zip: "76011", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "4", state: "Texas",      city: "Plano",         attraction: "XYZ place",          zip: "54643", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "5", state: "Texas",      city: "Dallas",        attraction: "Reunion tower",      zip: "12323", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "6", state: "California", city: "Los Angeles",   attraction: "Hollywood",          zip: "65456", attr: {country: {rowspan: "4"},    state: {rowspan: "4"}} },
    #    { id: "7", state: "California", city: "San Francisco", attraction: "Golden Gate bridge", zip: "94129", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "8", state: "California", city: "San Diego",     attraction: "See world",          zip: "56653", attr: {country: {display: "none"}, state: {display: "none"}} },
    #    { id: "9", state: "California", city: "Anaheim",       attraction: "Disneyworld",        zip: "92802", attr: {country: {display: "none"}, state: {display: "none"}} }
    #]

    #{idapp:1,form_name:goods,permission:allow add,user_id:1,attr:{form_name:{rowspan:"3"}}
    #{idapp:2,form_name:goods,permission:allow edit,user_id:1}
    #{idapp:3,form_name:goods,permission:allow view,user_id:1}

    def Get_Priviledge_Sys(self,user_id):
        cur = connection.cursor()
        Query = """SELECT ps.idapp,pf.form_name,ps.permission FROM n_a_sys_priviledge ps INNER JOIN n_a_priviledge_form pf ON ps.fk_pform = pf.idapp
        WHERE ps.user_id=%(User_id)s"""
        cur.execute(Query,{'User_id':user_id})
        return query.dictfetchall(cur)