from django.conf.urls import url, include
from models import Measurement, JournalEntry, Turbopump
from django.views.generic import ListView
from django.contrib.flatpages import views as flatpageviews
from django.http import HttpResponseRedirect

import surftof.views

urlpatterns = [
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'surftof/measurement_list.html', paginate_by = 100)),
    url(r'^pumps/$', ListView.as_view(model = Turbopump, template_name = 'surftof/pump_list.html')),
    url(r'^pumps/(?P<pumpnumber>\d+)$', surftof.views.pump),
    url(r'^insight/(?P<parameter1>\w+)/(?P<parameter2>\w+)/$', surftof.views.plot_parameters),
    url(r'^insight/$', lambda x: HttpResponseRedirect('u_surf/u_is/')),
    url(r'^insight/(?P<parameter1>\w+)/$', surftof.views.plot_parameters),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'surftof/journalentry_list.html')),
    url(r'^journal/new/$', surftof.views.newjournalentry),
    url(r'^journal/(\d+)/$', surftof.views.showjournalentry),
    url(r'^$', flatpageviews.flatpage, {'url': '/surftof/'}, name='surftofhome'),
    url(r'^export/(\d+)/$', surftof.views.exportfile),
    url(r'^export/(\d+)/filename$', surftof.views.exportfilename),
    url(r'^json/(\d+)/$', surftof.views.mjson),
    url(r'^vacuumstatus/input/$', surftof.views.readvacuumstatus),
    url(r'^vacuumstatus/output/(\d+)/(\d+)/$', surftof.views.writevacuumstatus),
    url(r'^vacuumstatus/output/(\d+)/$', surftof.views.writevacuumstatus),
    url(r'^vacuumstatus/output/$', surftof.views.writevacuumstatus),
]
