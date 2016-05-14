from django.conf.urls import url

from . import views
# . means from current folder

urlpatterns = [
    url(r'^$', views.index, name='index')
]