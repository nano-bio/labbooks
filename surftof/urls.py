from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers
import surftof.views as views

rest_router = routers.DefaultRouter()
rest_router.register(r'counts-per-mass', views.CountsPerMassViewSet)

urlpatterns = [
    url(r'^iseg-export/(?P<pk>\d+)/$', views.export_iseg_profile),
    url(r'^measurement-json/(?P<pk>\d+)/$', views.measurement_json_export),
    url(r'^potentialsettings-json/(?P<pk>\d+)/$', views.potential_settings_json_export),

    # preview data
    url(r'^preview/$', TemplateView.as_view(template_name='surftof/previewData.html')),
    url(r'^preview_file_list/$', views.preview_file_list),
    url(
        r'preview_data/'
        r'(?P<time_bin_or_mass>timebin|mass|diff)/'
        r'(?P<data_id_file_1>\d+)/'
        r'(?P<data_id_file_2>\d+|null)/'
        r'(?P<scale_data_file_2>\d+\.\d{3})/'
        r'(?P<diff_plot>true|false)/'
        r'(?P<binned_by>\d+)/'
        r'(?P<max_time_bin>\d+)/$',
        views.preview_data),
    url(r'^get-file-info-for-preview/(?P<measurement_id>\d+)/$',
        views.get_file_info_for_preview),
    url(r'preview-trace/',
        login_required(views.preview_trace)),
    url(r'preview-wait/',
        login_required(views.preview_xkcd)),

    # update the rating of a measurement
    url(r'^set-rating-of-measurement/(?P<id>\d+)/(?P<rating>[1-5])/$', views.set_rating_of_measurement),

    # counts per mass
    url(r'', include(rest_router.urls)),
    url(r'cpm-ids/',
        login_required(views.cpm_filter_ids)),
    url(r'cpm/',
        login_required(TemplateView.as_view(template_name='surftof/counts_per_mass.html'))),
    url(r'cpm-plot-data/',
        login_required(views.cpm_data)),
]
