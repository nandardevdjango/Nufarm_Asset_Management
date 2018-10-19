"""
Definition of urls for N_Asset.
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from app.NA_Views.MasterData import NA_Privilege_View
from app.NA_Views import NA_User_View
import app.views
# Uncomment the next lines to enable the admin:
# admin.autodiscover()
from django.contrib import admin
from social_django.urls import *
urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),

    # User's URL
    url(r'^login/$', NA_Privilege_View.na_privilege_login, name='login'),
    url(r'^register/$', NA_Privilege_View.na_privilege_register,
        name='NA_User_Register'),
    url(r'^profile/(?P<username>\w+)/edit/$',
        NA_User_View.user_profile, name='user_profile'),
    url(r'^logout/$', NA_Privilege_View.NA_Privilege_logout, name='logout'),

    # Master Data URL
    url(r'^MasterData/', include('app.NA_Urls.MasterData_url', namespace='MasterData')),

    # Transactions URL
    url(r'^Transactions/',
        include('app.NA_Urls.Transactions_url', namespace='Transactions')),

    # Other Pages URL
    url(r'^OtherPages/', include('app.NA_Urls.OtherPages_url', namespace='OtherPages')),
    
    url(r'^Report/', include('app.NA_Urls.Reports_url', namespace='Report')),

    # Notifications URL
    url(r'^Notifications/', include('NA_Notifications.urls',
                                    namespace='NA_Notifications')),

    # URL Facebook,Google,Twitter Login
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
]

# untuk akses url media(picture) hasil upload User
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
