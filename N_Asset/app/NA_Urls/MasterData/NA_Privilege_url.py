from django.conf.urls import url
from app.NA_Views.MasterData import NA_Privilege_View

patterns_email = '(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})'

urlpatterns = [
    url(r'^$', NA_Privilege_View.NA_Privilege, name='NA_Privilege'),
    url(r'^getData/$', NA_Privilege_View.NA_PrivilegeGetData),
    url(r'^sys/$', NA_Privilege_View.NA_Privilege_sys),
    url(r'^ShowEntry/$', NA_Privilege_View.Entry_Privilege),
    url(r'^delete/$', NA_Privilege_View.Delete_user),
    url(r'^customFilter/$', NA_Privilege_View.ShowCustomFilter),
    url(r'^change_role/' + patterns_email +
        '/$', NA_Privilege_View.ChangeRole),
    url(
        r'^permission/(?P<idapp>\d+)/setInActive/$',
        NA_Privilege_View.NA_Sys_Privilege_setInactive
    ),
    url(r'^permission/(?P<idapp>\d+)/delete/$',
        NA_Privilege_View.NA_Sys_Privilege_delete),
    url(r'^permission/' + patterns_email + '/add/$',
        NA_Privilege_View.NA_Sys_Privilege_add),
    url(
        r'^permission/' + patterns_email + '/set_default/',
        NA_Privilege_View.NA_Sys_Privilege_SetDefaultPermission
    ),
    url(
        r'^permission/(?P<user_id>\d+)/check_permission/$',
        NA_Privilege_View.NA_Sys_Privilege_check_permission
    ),
    url(
        r'^permission/' + patterns_email + '/get_permission/$',
        NA_Privilege_View.NA_Sys_Privilege_get_permission
    ),
    url(r'^change_picture/' + patterns_email + '/',
        NA_Privilege_View.NA_Privilege_change_picture)
]
