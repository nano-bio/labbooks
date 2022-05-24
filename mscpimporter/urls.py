from django.contrib.auth.decorators import login_required
from django.urls import path

import mscpimporter.views

urlpatterns = [
    path('',
         login_required(
             mscpimporter.views.start_import),
         name="mscpimporter-start"),
]
