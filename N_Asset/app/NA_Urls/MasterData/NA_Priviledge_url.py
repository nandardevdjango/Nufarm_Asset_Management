from django.conf.urls import url
from app.NA_Views.MasterData import NA_Priviledge_View

patterns_email = '(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})'

urlpatterns = [
	url(r'^$',NA_Priviledge_View.NA_Priviledge,name='NA_Priviledge'),
    url(r'^getData/$',NA_Priviledge_View.NA_PriviledgeGetData),
    url(r'^sys/$',NA_Priviledge_View.NA_Priviledge_sys),
    url(r'^ShowEntry/$',NA_Priviledge_View.Entry_Priviledge),
    url(r'^delete/$',NA_Priviledge_View.Delete_user),
    url(r'^customFilter/$',NA_Priviledge_View.ShowCustomFilter),
    url(r'^change_role/' + patterns_email + '/$', NA_Priviledge_View.ChangeRole),
    url(
        r'^permission/(?P<idapp>\d+)/setInActive/$',
        NA_Priviledge_View.NA_Sys_Priviledge_setInactive
    ),
    url(r'^permission/(?P<idapp>\d+)/delete/$',NA_Priviledge_View.NA_Sys_Priviledge_delete),
    url(r'^permission/'+ patterns_email +'/add/$',NA_Priviledge_View.NA_Sys_Priviledge_add),
    url(
        r'^permission/'+ patterns_email + '/set_default/',
        NA_Priviledge_View.NA_Sys_Priviledge_SetDefaultPermission
    ),
    url(
        r'^permission/(?P<user_id>\d+)/check_permission/$',
        NA_Priviledge_View.NA_Sys_Priviledge_check_permission
    ),
    url(
        r'^permission/'+ patterns_email +'/get_permission/$',
        NA_Priviledge_View.NA_Sys_Priviledge_get_permission
    )
]