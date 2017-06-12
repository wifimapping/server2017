# Define URL routing for the wifipulling component

from django.conf.urls import patterns, url
from wifipulling import views

urlpatterns = patterns('',
    # Serve API at index of wifipulling
    url(r'^$', views.index, name='index'),
    # Slippy tile URL for heatmap tiles
    url(r'tile/(\d+)/(\d+)/(\d+)/', views.tile, name='tile'),
    # Slippy tile URL for grey layer tiles
    url(r'greyTile/(\d+)/(\d+)/(\d+)/', views.greyTile)
)
