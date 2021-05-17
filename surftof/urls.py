from django.contrib.auth.decorators import login_required
from django.urls import path
import surftof.views as views

urlpatterns = [
    # preview data
    path('',
         views.preview,
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

    # json export
    path('<table>/<int:pk>.json',
         views.json_export,
         name="surftof-json-data"),

    # table export
    path('<table>.html',
         views.TableViewer.as_view(),
         name="surftof-table-data"),

    # update the rating of a measurement
    path('set-rating-of-measurement/<int:measurement_id>/<int:rating>/',
         login_required(views.set_rating_of_measurement),
         name="surftof-set-measurement-rating"),

    # surface temperature
    path('surface-temperature/',
         views.surface_temperature,
         name="surftof-surface-temperature"),
    path('surface-temperature-data/<date>/',
         views.surface_temperature_data,
         name="surftof-surface-temperature-data"),
]
