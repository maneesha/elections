from django.conf.urls import url

from . import views
# . means from current folder

urlpatterns = [
    url(r'^$', views.index),
    url(r'^pcc/$', views.phlcitycouncil),
    url(r'^about/$', views.about),
    # url(r'^vote_count/$', views.vote_count),
    url(r'^pcc/(?P<user_id>\d+)/$', views.phlcitycouncil),
    url(r'^vote_count/(?P<election_year>\d+)/$', views.vote_count),
]