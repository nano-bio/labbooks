from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.flatpages import views as flatpageviews

from models import Measurement, Calibration, JournalEntry, Turbopump

import vg.views

urlpatterns = [
    url(r'^$', flatpageviews.flatpage, {'url': '/vg/'}, name='vghome'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'vg/measurement_list.html', paginate_by = 100)),
    url(r'^view/(\d+)/$', vg.views.showmeasurement),
    url(r'^view/(\d+)/cal/(\d+)/$', vg.views.showcalibratedmeasurement),
    url(r'^view/(\d+)/calexport/(\d+)/$', vg.views.exportcalibratedmeasurement),
    url(r'^view/(\d+)/cal/$', ListView.as_view(model = Calibration, template_name = 'vg/choosecalibration_list.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cal/$', ListView.as_view(model = Calibration, template_name = 'vg/calibration_list.html')),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'vg/journalentry_list.html')),
    url(r'^export/(\d+)/', vg.views.exportmeasurement),
    url(r'^insight/(?P<parameter1>\w+)/(?P<parameter2>\w+)/$', vg.views.plot_parameters),
    url(r'^insight/$', lambda x: HttpResponseRedirect('ion_repeller/ion_energy/')),
    url(r'^insight/(?P<parameter1>\w+)/$', vg.views.plot_parameters),
    url(r'^view/(\d+)/fit/(\d+)/$', vg.views.fitmeasurement),
    url(r'^view/(\d+)/cal/(\d+)/fit/(\d+)/$', vg.views.fitcalmeasurement),
    url(r'^export_all_f_urls/$', vg.views.export_all_f_urls),
    url(r'^export_all_sf6_urls/$', vg.views.export_all_sf6_urls),
    url(r'^export_all_sf5_urls/$', vg.views.export_all_sf5_urls),
    url(r'^export_all_f2_urls/$', vg.views.export_all_f2_urls),
    url(r'^all_usable_es/$', vg.views.all_usable_es),
    url(r'^pumps/$', ListView.as_view(model = Turbopump, template_name = 'vg/pump_list.html')),
    url(r'^pumps/(?P<pumpnumber>\d+)$', vg.views.pump),
]
