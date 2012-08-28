from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'pyconpe.views.home', name='home'),
    url(r'^submissao/', include('submission.urls', namespace='submission')),

    url(r'^admin/', include(admin.site.urls)),
)
