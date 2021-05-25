from django.contrib.auth.decorators import login_required
from django.urls import path

import surftof.views as views

urlpatterns = [
    # overview
    path('',
         views.overview,
         name="surftof-overview"),
    path('journal/<int:year>/<int:month>/',
         views.overview,
         name="surftof-journal-page"),
    path('journal-entry/add/',
         login_required(views.JournalEntryCreate.as_view()),
         name='surftof-journal-entry-add'),
    path('journal-entry/<int:pk>/',
         login_required(views.JournalEntryUpdate.as_view()),
         name='surftof-journal-entry-update'),
    path('journal-entry/<int:pk>/delete/',
         login_required(views.JournalEntryDelete.as_view()),
         name='surftof-journal-entry-delete'),
    path('measurement/add/',
         login_required(views.MeasurementCreate.as_view()),
         name='surftof-measurement-add'),
    path('measurement/<int:pk>/',
         login_required(views.MeasurementUpdate.as_view()),
         name='surftof-measurement-update'),
    path('measurement/<int:pk>/delete/',
         login_required(views.MeasurementDelete.as_view()),
         name='surftof-measurement-delete'),
    path('preview-image/<int:measurement_id>/',
         views.mass_spec_preview_image,
         name="surftof-mass-spec-preview-image"),

    # preview data
    path('preview/',
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
