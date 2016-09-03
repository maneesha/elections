# from django.conf.urls import patterns, include, url
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = (#'',
    # Examples:
    # url(r'^$', 'elections.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # 
    # http://127.0.0.1:8000/phlcitycouncil/

    ## This gets you views from phlcitycouncil.urls
    ## Remember the url continues so don't put in the $
    ## at the end of the regex
    url(r'^', include('phlcitycouncil.urls')),

    # url(r'^phlcitycouncil/', include('phlcitycouncil.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
