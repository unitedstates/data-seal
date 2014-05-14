from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'authentication.authapp.views.index', name='index'),
    url(r'^upload/$', 'authentication.authapp.views.upload', name='upload'),
    url(r'^search/$', 'authentication.authapp.views.search', name='search'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/$', 'authentication.authapp.views.file_detail', name='file_detail'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/download/$', 'authentication.authapp.views.file_download', name='file_download'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/download/signature/$', 'authentication.authapp.views.file_signature', name='file_signature'),
    url(r'^admin/authapp/document/$', 'authentication.authapp.views.admin_document', name='admin_document'),
    url(r'^admin/login/', 'authentication.authapp.views.admin_login', name='admin_login'),
    url(r'^admin/authapp/$', 'authentication.authapp.views.admin_authapp', name='admin_authapp'),
    url(r'^admin/authapp/document/add/$', 'authentication.authapp.views.add', name='add'),
    url(r'^admin/authapp/document/(?P<file_id>[0-9]+)/$', 'authentication.authapp.views.edit', name='edit'),
    url(r'^admin/logout', 'authentication.authapp.views.admin_logout', name='admin_logout'),
    url(r'^admin/auth/user/$', 'authentication.authapp.views.admin_user', name="admin_user"),
    url(r'^admin/auth/user/add/$', 'authentication.authapp.views.admin_user_add', name="admin_user_add"),
    url(r'^admin/auth/user/(?P<user_id>[0-9]+)/$', 'authentication.authapp.views.admin_user_edit', name="admin_user_edit"),
    url(r'^admin/', include(admin.site.urls)),
)
