from django.conf.urls import patterns, url
from lisa.plugins.ProgrammeTV.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
