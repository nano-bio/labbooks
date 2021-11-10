from django.http import HttpResponseRedirect
from django.urls import path
from django.views.generic import ListView, RedirectView

import wippi.views
from wippi.models import Measurement, Calibration, JournalEntry

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="wippi-measurements"), name='wippihome'),
    path('view/', ListView.as_view(model=Measurement, template_name='wippi/measurement_list.html', paginate_by=100),
         name="wippi-measurements"),
    path('view/<int:id>/', wippi.views.showmeasurement),
    path('view/<int:m_id>/cal/<int:c_id>/', wippi.views.showcalibratedmeasurement),
    path('view/<int:m_id>/calexport/<int:c_id>/', wippi.views.exportcalibratedmeasurement),
    path('view/<int:id>/cal/', ListView.as_view(model=Calibration, template_name='wippi/choosecalibration_list.html')),
    path('cal/', ListView.as_view(model=Calibration, template_name='wippi/calibration_list.html')),
    path('journal/', ListView.as_view(model=JournalEntry, template_name='wippi/journalentry_list.html')),
    path('export/<int:id>/', wippi.views.exportmeasurement),
    path('insight/<parameter1>/<parameter2>/', wippi.views.plot_parameters),
    path('insight/', lambda x: HttpResponseRedirect('lens_1a/lens_1b/')),
    path('insight/<parameter1>/', wippi.views.plot_parameters),
    path('view/<int:m_id>/fit/<int:n_peaks>/', wippi.views.fitmeasurement),
    path('view/<int:m_id>/cal/<int:c_id>/fit/<int:n_peaks>/', wippi.views.fitcalmeasurement),
]
