from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework import routers
import surftof.views as views

rest_router = routers.DefaultRouter()
rest_router.register(r'counts-per-mass', views.CountsPerMassViewSet)

urlpatterns = [
    # base template
    url(r'^$',
        TemplateView.as_view(template_name="surftof/base.html"),
        name="surftof-base-template"),

    # json export
    url(r'^(?P<table>\w+)/(?P<pk>\d+).json$',
        views.json_export,
        name="surftof-json-data"),

    # table export
    url(r'^(?P<table>\w+).html$',
        views.TableViewer.as_view(),
        name="surftof-table-data"),

    # preview data
    url(r'^preview/$',
        TemplateView.as_view(template_name='surftof/previewData.html'),
        name="surftof-preview"),
    url(r'^preview/file_list/$',
        views.preview_file_list,
        name="surftof-preview-file-list"),
    url(r'^preview/data/$',
        views.preview_data,
        name="surftof-preview-data"),
    url(r'^preview/file-info/(?P<measurement_id>\d+)/$',
        views.preview_get_file_info,
        name="surftof-preview-file-info"),
    url(r'^preview/trace/',
        views.preview_trace,
        name="surftof-preview-trace"),
    url(r'^preview/wait/',
        views.preview_xkcd,
        name="surftof-preview-xkcd"),

    # update the rating of a measurement
    url(r'^set-rating-of-measurement/(?P<id>\d+)/(?P<rating>[1-5])/$',
        login_required(views.set_rating_of_measurement),
        name="surftof-set-measurement-rating"),

    # counts per mass
    url(r'api', include(rest_router.urls)),
    url(r'^cpm/id-list/$',
        views.cpm_filter_ids,
        name="surftof-cpm-id-list"),
    url(r'^cpm/$',
        TemplateView.as_view(template_name='surftof/counts_per_mass.html'),
        name="surftof-cpm"),
    url(r'^cpm/plot-data/$',
        views.cpm_data,
        name="surftof-cpm-plot-data"),
]
