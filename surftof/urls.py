from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers
import surftof.views as views

rest_router = routers.DefaultRouter()
rest_router.register(r'counts-per-mass', views.CountsPerMassViewSet)

urlpatterns = [
    # base template
    path('',
         TemplateView.as_view(template_name="surftof/base.html"),
         name="surftof-base-template"),

    # json export
    path('<table>/<int:pk>.json',
         views.json_export,
         name="surftof-json-data"),

    # table export
    path('<table>.html',
         views.TableViewer.as_view(),
         name="surftof-table-data"),

    # preview data
    path('preview/',
         TemplateView.as_view(template_name='surftof/previewData.html'),
         name="surftof-preview"),
    path('preview/file_list/',
         views.preview_file_list,
         name="surftof-preview-file-list"),
    path('preview/data/',
         views.preview_data,
         name="surftof-preview-data"),
    path('preview/file-info/<int:measurement_id>/',
         views.preview_get_file_info,
         name="surftof-preview-file-info"),
    path('preview/trace/',
         views.preview_trace,
         name="surftof-preview-trace"),
    path('preview/wait/',
         views.preview_xkcd,
         name="surftof-preview-xkcd"),

    # update the rating of a measurement
    path('set-rating-of-measurement/<int:measurement_id>/<int:rating>/',
         login_required(views.set_rating_of_measurement),
         name="surftof-set-measurement-rating"),

    # counts per mass
    path('api/', include(rest_router.urls)),
    path('cpm/id-list/',
         views.cpm_filter_ids,
         name="surftof-cpm-id-list"),
    path('cpm/',
         TemplateView.as_view(template_name='surftof/counts_per_mass.html'),
         name="surftof-cpm"),
    path('cpm/plot-data/',
         views.cpm_data,
         name="surftof-cpm-plot-data"),
    path('cpm/export-csv/',
         views.cpm_export_csv,
         name="surftof-cpm-export-csv")
]
