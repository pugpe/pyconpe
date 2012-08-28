from django.conf.urls import patterns, include, url

from .views import SubmissionView


urlpatterns = patterns('',
    url(r'^$', SubmissionView.as_view(), name='submission'),
)
