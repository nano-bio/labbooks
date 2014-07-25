from django.conf.urls import patterns, include, url

import vg.urls
import clustof.urls
import wippi.urls
import cheminventory.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labbooks.views.home', name='home'),
    #url(r'^labbooks/vg/', include('labbooks.vg.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^vg/', include(vg.urls)),
    url(r'^wippi/', include(wippi.urls)),
    url(r'^clustof/', include(clustof.urls)),
    url(r'^cheminventory/', include(cheminventory.urls)),
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/'}, name='home'),
)
