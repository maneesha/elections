from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elections.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # 
    # http://127.0.0.1:8000/phlcitycouncil/
    url(r'^phlcitycouncil/', include('phlcitycouncil.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
