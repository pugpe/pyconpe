from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$',
       direct_to_template, {'template': 'index.html'},
       name='index',
    ),
    url(r'^submissao/', include('submission.urls', namespace='submission')),
    url(r'^emails/', include('emails.urls', namespace='emails')),
    url(r'^resultado/$', 'core.views.results', name='resultado'),
    url(r'^admin/', include(admin.site.urls)),
)
