from django.urls import path

import journal.views
import massspectra.views
from toffy2.admin import MeasurementAdmin
from toffy2.models import Measurement, JournalEntry

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='Toffy2'),
         name='toffy2-journal'),
    path('journal/add/',
         journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='Toffy2'),
         name='toffy2-journal-add'),
    path('journal/<int:pk>/',
         journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry),
         name='toffy2-journal-update'),
    path('journal/<int:pk>/delete/',
         journal.views.JournalEntryDelete.as_view(
             model=JournalEntry),
         name='toffy2-journal-delete'),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraListView.as_view(
             model=Measurement,
             model_admin=MeasurementAdmin),
         name="toffy2-mass-spectra"),
    path('mass-spectra/data/',
         massspectra.views.get_toffy_like_mass_spectra_data,
         {'measurement_model': Measurement},
         name="toffy2-mass-spectra-data"),

    # json export
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="toffy2-measurement-json"),
]
