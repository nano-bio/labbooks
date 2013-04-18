from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.views.generic.date_based import archive_index
from django.contrib import admin
from django.views.generic import ListView

from models import Measurement, Calibration, JournalEntry

import vg.views

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/vg/'}, name='vghome'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'measurement_list.html')),
    url(r'^view/(\d+)/$', 'vg.views.showmeasurement'),
    url(r'^view/(\d+)/cal/(\d+)/$', 'vg.views.showcalibratedmeasurement'),
    url(r'^view/(\d+)/calexport/(\d+)/$', 'vg.views.exportcalibratedmeasurement'),
    url(r'^view/(\d+)/cal/$', ListView.as_view(model = Calibration, template_name = 'choosecalibration_list.html')),
    url(r'^view/$', archive_index, {'queryset': Measurement.objects.all(), 'date_field': 'time', 'num_latest': 50}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cal/$', ListView.as_view(model = Calibration, template_name = 'calibration_list.html')),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'journalentry_list.html')),
    url(r'export/(\d+)/', 'vg.views.exportmeasurement'),
)
