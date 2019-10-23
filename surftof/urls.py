from django.conf.urls import url
from django.views.generic import TemplateView

from surftof.views import export_iseg_profile, measurement_json_export, potential_settings_json_export, \
    preview_file_list, calibration_list, preview_data

urlpatterns = [
    url(r'^iseg-export/(?P<pk>\d+)/$', export_iseg_profile),
    url(r'^measurement-json/(?P<pk>\d+)/$', measurement_json_export),
    url(r'^potentialsettings-json/(?P<pk>\d+)/$', potential_settings_json_export),

    # preview data
    url(r'^preview/$', TemplateView.as_view(template_name='surftof/previewData.html')),
    url(r'^preview_file_list/$', preview_file_list),
    url(
        r'preview_data/'
        r'(?P<time_bin_or_mass>timebin|mass|diff)/'
        r'(?P<calibration_id>\d+|null)/'
        r'(?P<data_id_file_1>\d+)/'
        r'(?P<data_id_file_2>\d+|null)/'
        r'(?P<scale_data_file_2>\d+\.\d{3})/'
        r'(?P<diff_plot>true|false)/'
        r'(?P<binned_by>\d+)/'
        r'(?P<max_time_bin>\d+)/$',
        preview_data),
    url(r'^calibration-list/$', calibration_list),
]
