from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin

from django_yubico.views import login, password

urlpatterns = patterns(
    '',
    url(r'^login', login, name='yubico_django_login'),
    url(r'^password', password, name='yubico_django_password'),
)


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'authentication.authapp.views.index', name='index'),
    url(r'^upload/$', 'authentication.authapp.views.upload', name='upload'),
    url(r'^view/$', 'authentication.authapp.views.documents', name='documents'),
    url(r'^search/$', 'authentication.authapp.views.search', name='search'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/$', 'authentication.authapp.views.file_detail', name='file_detail'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/download/$', 'authentication.authapp.views.file_download', name='file_download'),
    url(r'^document/(?P<file_sha256>[0-9a-f]{64})/(?P<file_name>.*)\.sig$', 'authentication.authapp.views.file_signature', name='file_signature'),
    url(r'^admin/authapp/document/$', 'authentication.authapp.views.admin_document', name='admin_document'),
    url(r'^admin/login/', 'authentication.authapp.views.admin_login', name='admin_login'),
    #url(r'^admin/login', login, name='yubico_django_login'),
    url(r'^admin/password', password, name='yubico_django_password'),
    url(r'^admin/authapp/$', 'authentication.authapp.views.admin_authapp', name='admin_authapp'),
    url(r'^admin/authapp/document/add/$', 'authentication.authapp.views.add', name='add'),
    url(r'^admin/authapp/document/(?P<file_id>[0-9]+)/$', 'authentication.authapp.views.edit', name='edit'),
    url(r'^admin/logout', 'authentication.authapp.views.admin_logout', name='admin_logout'),
    url(r'^admin/auth/user/$', 'authentication.authapp.views.admin_user', name="admin_user"),
    url(r'^admin/auth/user/add/$', 'authentication.authapp.views.admin_user_add', name="admin_user_add"),
    url(r'^admin/auth/user/(?P<user_id>[0-9]+)/$', 'authentication.authapp.views.admin_user_edit', name="admin_user_edit"),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
