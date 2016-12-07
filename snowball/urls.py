from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.flatpages import views as flatpageviews

from models import Measurement, JournalEntry, Turbopump

import snowball.views

urlpatterns = [
    url(r'^$', flatpageviews.flatpage, {'url': '/snowball/'}, name='snowballhome'),
    url(r'^view/$', ListView.as_view(model = Measurement, template_name = 'snowball/measurement_list.html', paginate_by = 100)),
    url(r'^view/(\d+)/$', snowball.views.showmeasurement),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^journal/$', ListView.as_view(model = JournalEntry, template_name = 'snowball/journalentry_list.html')),
    url(r'^export/(\d+)/', snowball.views.exportmeasurement),
    url(r'^pumps/$', ListView.as_view(model = Turbopump, template_name = 'snowball/pump_list.html')),
    url(r'^pumps/(?P<pumpnumber>\d+)$', snowball.views.pump),
]
