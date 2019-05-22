from django.conf.urls import url
from django.views.generic import TemplateView
import toffy.views

urlpatterns = [
    # preview of data
    url(r'^preview_file_list/$', toffy.views.preview_file_list),
    url(r'^preview_data/(?P<pk>\d+)/$', toffy.views.preview_data),
    url(r'^preview/$', TemplateView.as_view(template_name='previewData.html')),
]
