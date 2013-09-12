from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.views.generic.date_based import archive_index
from django.contrib import admin
from django.views.generic import ListView
from django.http import HttpResponseRedirect

from models import Measurement, Calibration, JournalEntry

import vg.views

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/vg/'}, name='vghome'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'vg/measurement_list.html', paginate_by = 100)),
    url(r'^view/(\d+)/$', 'vg.views.showmeasurement'),
    url(r'^view/(\d+)/cal/(\d+)/$', 'vg.views.showcalibratedmeasurement'),
    url(r'^view/(\d+)/calexport/(\d+)/$', 'vg.views.exportcalibratedmeasurement'),
    url(r'^view/(\d+)/cal/$', ListView.as_view(model = Calibration, template_name = 'vg/choosecalibration_list.html')),
    #url(r'^view/$', archive_index, {'queryset': Measurement.objects.all(), 'date_field': 'time', 'num_latest': 50, 'template_name': 'measurement_list.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cal/$', ListView.as_view(model = Calibration, template_name = 'vg/calibration_list.html')),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'vg/journalentry_list.html')),
    url(r'^export/(\d+)/', 'vg.views.exportmeasurement'),
    url(r'^insight/(?P<parameter1>\w+)/(?P<parameter2>\w+)/$', 'vg.views.plot_parameters'),
    url(r'^insight/$', lambda x: HttpResponseRedirect('ion_repeller/ion_energy/')),
    url(r'^insight/(?P<parameter1>\w+)/$', 'vg.views.plot_parameters'),
)
