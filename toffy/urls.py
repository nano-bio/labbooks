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
]
