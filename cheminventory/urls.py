from django.conf.urls import patterns, url, include

import cheminventory.views

urlpatterns = patterns('',
    url(r'^doorsign/(\d+)/$', 'cheminventory.views.print_doorsign'),
    url(r'^chemwaste/(\d+)/$', 'cheminventory.views.print_chemwaste'),
)
