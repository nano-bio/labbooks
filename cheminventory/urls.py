from django.conf.urls import patterns, url, include

import cheminventory.views

urlpatterns = [
    url(r'^doorsign/(\d+)/$', cheminventory.views.print_doorsign),
    url(r'^chemwaste/(\d+)/$', cheminventory.views.print_chemwaste),
    url(r'^qrcode/(\d+)/$', cheminventory.views.print_gas_cylinder_qr),
]
