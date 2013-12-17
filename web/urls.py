from django.conf.urls import patterns, url
from ProgrammeTV.web import views

urlpatterns = patterns('',
    url(r'^$',views.index),
)
