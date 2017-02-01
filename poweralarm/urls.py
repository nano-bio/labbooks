from django.conf.urls import url

import poweralarm.views

urlpatterns = [
    url(r'^alarm/(\w+)/$', poweralarm.views.alarm),
    url(r'^clear/(\w+)/$', poweralarm.views.clear),
]
