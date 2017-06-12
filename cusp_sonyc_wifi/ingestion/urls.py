from django.conf.urls import patterns, url
from ingestion import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'))