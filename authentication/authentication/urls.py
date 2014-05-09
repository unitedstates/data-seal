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

    url(r'^admin/', include(admin.site.urls)),
)
