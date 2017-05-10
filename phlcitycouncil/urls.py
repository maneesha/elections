from django.conf.urls import url

from . import views
# . means from current folder

urlpatterns = [
    url(r'^$', views.index),
    url(r'^pcc/$', views.candidate_list),
    url(r'^about/$', views.about),
    # url(r'^vote_count/$', views.vote_count),
    url(r'^pcc/(?P<user_id>\d+)/$', views.candidate_bios),
    url(r'^vote_count/(?P<election_year>[0-9]{4})/$', views.vote_count),
]