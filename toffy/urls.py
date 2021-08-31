from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

import toffy.views

urlpatterns = [
    # preview of data
    path('preview_file_list/',
         toffy.views.preview_file_list,
         name="toffy-preview-file-list"),
    path('preview_data/<int:pk>/',
         toffy.views.preview_data,
         name="toffy-preview-data"),
    path('preview/',
         TemplateView.as_view(template_name='toffy/previewData.html'),
         name="toffy-preview"),
    path('preview_measurement_info/<int:measurement_id>/',
         toffy.views.preview_measurement_info,
         name="toffy-preview-measurement-info"),
    path('journal/',
         toffy.views.JournalListView.as_view(template_name='journal/journal_experiment.html'),
         name='toffy-journal'),
    path('journal/add/',
         login_required(toffy.views.JournalEntryCreate.as_view()),
         name='toffy-journal-add'),
    path('journal/<int:pk>/',
         login_required(toffy.views.JournalEntryUpdate.as_view()),
         name='toffy-journal-update'),
    path('journal/<int:pk>/delete/',
         login_required(toffy.views.JournalEntryDelete.as_view()),
         name='toffy-journal-delete'),
]
