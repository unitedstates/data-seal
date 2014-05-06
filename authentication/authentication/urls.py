from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'authentication.authapp.views.index', name='index'),
    url(r'^upload/$', 'authentication.authapp.views.upload', name='upload'),
    url(r'^search/$', 'authentication.authapp.views.search', name='search'),
    url(r'^file_detail/(?P<file_slug>\w+)/$', 'authentication.authapp.views.file_detail', name='file_detail'),
    url(r'^file_download/(?P<file_slug>\w+)/$', 'authentication.authapp.views.file_download', name='file_download'),
    url(r'^file_signature/(?P<file_slug>\w+)/signature/$', 'authentication.authapp.views.file_signature', name='file_signature'),

    url(r'^admin/', include(admin.site.urls)),
)
