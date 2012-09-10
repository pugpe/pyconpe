from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$',
       'django.views.generic.simple.redirect_to',
       {'url': '/submissao/', 'permanent': False},
    ),
    url(r'^submissao/', include('submission.urls', namespace='submission')),
    url(r'^emails/', include('emails.urls', namespace='emails')),
    url(r'^resultado/$', 'core.views.results', name='resultado'),
    url(r'^admin/', include(admin.site.urls)),
)
