from django.urls import path

import journal.views
import massspectra.views
from MRTOF.admin import MeasurementAdmin
from MRTOF.models import Measurement, JournalEntry

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='MRTOF'),
         name='MRTOF-journal'),
    path('journal/add/',
         journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='MRTOF'),
         name='MRTOF-journal-add'),
    path('journal/<int:pk>/',
         journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry),
         name='MRTOF-journal-update'),
    path('journal/<int:pk>/delete/',
         journal.views.JournalEntryDelete.as_view(
             model=JournalEntry),
         name='MRTOF-journal-delete'),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraView.as_view(
             model=Measurement,
             model_admin=MeasurementAdmin),
         name="MRTOF-mass-spectra"),
    path('mass-spectra/measurements/',
         massspectra.views.MassSpectraMeasurementListJson.as_view(
             measurement_model=Measurement),
         name="MRTOF-mass-spectra-measurements"),
    path('mass-spectra/data/',
         massspectra.views.get_toffy_like_mass_spectra_data,
         {'measurement_model': Measurement},
         name="MRTOF-mass-spectra-data"),

    # json export
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="MRTOF-measurement-json"),
]
