from django.conf.urls import url
from surftof.views import export_iseg_profile

urlpatterns = [
    url(r'^iseg-export/(?P<pk>\d+)/$', export_iseg_profile),
]
