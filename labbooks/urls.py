from django.conf.urls import include, url

import vg.urls
import clustof.urls
import surftof.urls
import wippi.urls
import cheminventory.urls
import snowball.urls
from django.contrib.flatpages import views as flatpageviews

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
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
    url(r'^surftof/', include(surftof.urls)),
    url(r'^snowball/', include(snowball.urls)),
    url(r'^cheminventory/', include(cheminventory.urls)),
    url(r'^$', flatpageviews.flatpage, {'url': '/'}, name='home'),
]
