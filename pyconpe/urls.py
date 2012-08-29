from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   url(r'^$', 
        'django.views.generic.simple.redirect_to',
        {'url': 'http://pug-pe.python.org.br/encontro/xix/'},
    ),
    url(r'^submissao/', include('submission.urls', namespace='submission')),

    url(r'^admin/', include(admin.site.urls)),
)
