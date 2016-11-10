from django.conf.urls import url

from . import views
# . means from current folder

urlpatterns = [
    url(r'^$', views.index),
    url(r'^pcc/$', views.phlcitycouncil),
    url(r'^about/$', views.about),
    url(r'^vote_count/$', views.vote_count),
]