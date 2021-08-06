from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import cheminventory.urls
import clustof.urls
import labinventory.urls
import snowball.urls
import surftof.urls
import toffy.urls
import toffy2.urls
import vg.urls
import wippi.urls
from journal.views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
