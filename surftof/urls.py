from django.conf.urls import url
from surftof.views import export_iseg_profile, measurement_json_export, potential_settings_json_export

urlpatterns = [
    url(r'^iseg-export/(?P<pk>\d+)/$', export_iseg_profile),
    url(r'^measurement-json/(?P<pk>\d+)/$', measurement_json_export),
    url(r'^potentialsettings-json/(?P<pk>\d+)/$', potential_settings_json_export),
]
