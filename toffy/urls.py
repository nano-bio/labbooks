from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

import toffy.views as views

urlpatterns = [
    # preview of data
    path('preview_file_list/',
         views.preview_file_list,
         name="toffy-preview-file-list"),
    path('preview_data/<int:pk>/',
         views.preview_data,
         name="toffy-preview-data"),
    path('preview/',
         TemplateView.as_view(template_name='toffy/previewData.html'),
         name="toffy-preview"),
    path('preview_measurement_info/<int:measurement_id>/',
         views.preview_measurement_info,
         name="toffy-preview-measurement-info"),

    # Journal
    path('journal/',
         views.JournalListView.as_view(template_name='journal/journal_experiment.html'),
         name='toffy-journal'),
    path('journal/add/',
         login_required(views.JournalEntryCreate.as_view()),
         name='toffy-journal-add'),
    path('journal/<int:pk>/',
         login_required(views.JournalEntryUpdate.as_view()),
         name='toffy-journal-update'),
    path('journal/<int:pk>/delete/',
         login_required(views.JournalEntryDelete.as_view()),
         name='toffy-journal-delete'),

    # mass spectra
    path('mass-spectra/',
         views.MassSpectraListView.as_view(),
         name="toffy-mass-spectra"),
]
