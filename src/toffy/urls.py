from django.urls import path

import journal.views
import massspectra.views
from toffy.admin import MeasurementAdmin
from toffy.models import Measurement, JournalEntry

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='Toffy'),
         name='toffy-journal'),
    path('journal/add/',
         journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='Toffy'),
         name='toffy-journal-add'),
    path('journal/<int:pk>/',
         journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry),
         name='toffy-journal-update'),
    path('journal/<int:pk>/delete/',
         journal.views.JournalEntryDelete.as_view(
             model=JournalEntry),
         name='toffy-journal-delete'),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraView.as_view(
             model=Measurement,
             model_admin=MeasurementAdmin),
         name="toffy-mass-spectra"),
    path('mass-spectra/measurements/',
         massspectra.views.MassSpectraMeasurementListJson.as_view(
             measurement_model=Measurement),
         name="toffy-mass-spectra-measurements"),
    path('mass-spectra/data/',
         massspectra.views.get_toffy_like_mass_spectra_data,
         {'measurement_model': Measurement},
         name="toffy-mass-spectra-data"),

    # json export
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="toffy-measurement-json"),
]
