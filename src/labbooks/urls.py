from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

import cheminventory.urls
import clustof.urls
import journal.urls
import labinventory.urls
import mscpimporter.urls
import nanoparticles.urls
import snowball.urls
import surftof.urls
import toffy.urls
import toffy2.urls
import vg.urls
import wippi.urls
from journal.views import homepage
from labbooks.admin_common import export_tables_csv_view

urlpatterns = [
    path('', homepage, name='homepage'),
    path('journal/', include(journal.urls)),

    path('admin/', admin.site.urls),

    path('cheminventory/', include(cheminventory.urls)),
    path('labinventory/', include(labinventory.urls)),
    path('mscpimporter/', include(mscpimporter.urls)),

    path('clustof/', include(clustof.urls)),
    path('nanoparticles/', include(nanoparticles.urls)),
    path('snowball/', include(snowball.urls)),
    path('surftof/', include(surftof.urls)),
    path('toffy/', include(toffy.urls)),
    path('toffy2/', include(toffy2.urls)),
    path('vg/', include(vg.urls)),
    path('wippi/', include(wippi.urls)),

    # csv export tables to netshare folders
    path('export-csv/',
         login_required(export_tables_csv_view),
         name='export-csv-files'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
