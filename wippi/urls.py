from django.conf.urls import patterns, url, include
#from django.views.generic.date_based import archive_index
from django.contrib import admin
from django.views.generic import ListView
from django.http import HttpResponseRedirect

from models import Measurement, Calibration, JournalEntry

import wippi.views

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.flatpages.views.flatpage', {'url': '/wippi/'}, name='wippihome'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'wippi/measurement_list.html', paginate_by = 100)),
    url(r'^view/(\d+)/$', 'wippi.views.showmeasurement'),
    url(r'^view/(\d+)/cal/(\d+)/$', 'wippi.views.showcalibratedmeasurement'),
    url(r'^view/(\d+)/calexport/(\d+)/$', 'wippi.views.exportcalibratedmeasurement'),
    url(r'^view/(\d+)/cal/$', ListView.as_view(model = Calibration, template_name = 'wippi/choosecalibration_list.html')),
    #url(r'^view/$', archive_index, {'queryset': Measurement.objects.all(), 'date_field': 'time', 'num_latest': 50, 'template_name': 'measurement_list.html'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cal/$', ListView.as_view(model = Calibration, template_name = 'wippi/calibration_list.html')),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'wippi/journalentry_list.html')),
    url(r'^export/(\d+)/', 'wippi.views.exportmeasurement'),
    url(r'^insight/(?P<parameter1>\w+)/(?P<parameter2>\w+)/$', 'wippi.views.plot_parameters'),
    url(r'^insight/$', lambda x: HttpResponseRedirect('lens_1a/lens_1b/')),
    url(r'^insight/(?P<parameter1>\w+)/$', 'wippi.views.plot_parameters'),
    url(r'^view/(\d+)/fit/(\d+)/$', 'wippi.views.fitmeasurement'),
    url(r'^view/(\d+)/cal/(\d+)/fit/(\d+)/$', 'wippi.views.fitcalmeasurement'),
)
