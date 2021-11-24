from django.urls import path

import journal.views
from nanoparticles.models import JournalEntry
from nanoparticles.views import image_data, TableViewer

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='NanoParticles'),
         name='nanoparticles-journal'),
    path('journal/add/',
         journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='NanoParticles'),
         name='nanoparticles-journal-add'),
    path('journal/<int:pk>/',
         journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry),
         name='nanoparticles-journal-update'),
    path('journal/<int:pk>/delete/',
         journal.views.JournalEntryDelete.as_view(
             model=JournalEntry,
             experiment='NanoParticles'),
         name='nanoparticles-journal-delete'),

    # Measurement List
    path('measurements/', TableViewer.as_view(), name='nanoparticles-measurements'),

    # Image DATA
    path('image-data/<int:measurement_id>/<direction>/<measurement_type>/<int:smoothing>/',
         image_data,
         name='nanoparticles-image-data'),
]
