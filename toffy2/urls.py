from django.urls import path
from django.views.generic import TemplateView
import toffy2.views

urlpatterns = [
    # preview of data
    path('preview_file_list/',
         toffy2.views.preview_file_list,
         name="toffy2-preview-file-list"),
    path('preview_data/<int:pk>/',
         toffy2.views.preview_data,
         name="toffy2-preview-data"),
    path('preview/',
         TemplateView.as_view(template_name='toffy2/previewData.html'),
         name="toffy2-preview"),
    path('preview_measurement_info/<int:measurement_id>/',
         toffy2.views.preview_measurement_info,
         name="toffy2-preview-measurement-info"),
]
