from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

import massspectra.views
import journal.views
import surftof.views as views
from surftof.admin import MeasurementsAdmin
from surftof.models import Measurement, JournalEntry

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='SurfTOF'),
         name='surftof-journal'),
    path('journal/add/',
         login_required(journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='SurfTOF')),
         name='surftof-journal-add'),
    path('journal/<int:pk>/',
         login_required(journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry,
         )),
         name='surftof-journal-update'),
    path('journal/<int:pk>/delete/',
         login_required(journal.views.JournalEntryDelete.as_view(
             model=JournalEntry,
             experiment='SurfTOF')),
         name='surftof-journal-delete'),

    # Journal Preview Images of Mass Spectra
    path('preview-image/<int:measurement_id>.png',
         views.mass_spec_preview_image,
         name="surftof-mass-spec-preview-image"),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraListView.as_view(
             model=Measurement,
             model_admin=MeasurementsAdmin,
             experiment_name='SurfTOF'),
         name="surftof-mass-spectra"),
    path('mass-spectra/data/',
         views.get_mass_spectra_data,
         name="surftof-mass-spectra-data"),

    # mass spectra traces
    path('mass-spectra/trace/',
         views.mass_spectra_trace,
         name="surftof-mass-spectra-trace"),
    path('mass-spectra/wait/',
         views.mass_spectra_xkcd,
         name="surftof-mass-spectra-xkcd"),

    # json export
    path('<table>/<int:pk>.json',
         views.json_export,
         name="surftof-json-data"),

    # json export measurement
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="surftof-measurement-json"),

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

    # pressures
    path('pressures/',
         TemplateView.as_view(
             template_name='surftof/pressure.html',
             extra_context={'labels': ['IS', 'SURF', 'TOF', 'BOST', 'PIS', 'PTOF']}),
         name="surftof-pressures"),
]
