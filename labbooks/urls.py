from django.contrib import admin
from django.urls import path, include
import labinventory.urls
import vg.urls
import clustof.urls
import surftof.urls
import wippi.urls
import cheminventory.urls
import snowball.urls
import toffy.urls
import toffy2.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vg/', include(vg.urls)),
    path('wippi/', include(wippi.urls)),
    path('clustof/', include(clustof.urls)),
    path('surftof/', include(surftof.urls)),
    path('snowball/', include(snowball.urls)),
    path('cheminventory/', include(cheminventory.urls)),
    path('labinventory/', include(labinventory.urls)),
    path('toffy/', include(toffy.urls)),
    path('toffy2/', include(toffy2.urls)),
]
