from django.http import HttpResponseRedirect
from django.urls import path
from django.views.generic import ListView, RedirectView

import vg.views
from vg.models import Measurement, Calibration, JournalEntry, Turbopump

urlpatterns = [
    path('', RedirectView.as_view(pattern_name="vg-measurements"), name='vghome'),
    path('view/', ListView.as_view(model=Measurement, template_name='vg/measurement_list.html', paginate_by=100),
         name="vg-measurements"),
    path('view/<int:id>/', vg.views.showmeasurement),
    path('view/<int:m_id>/cal/<int:c_id>/', vg.views.showcalibratedmeasurement),
    path('view/<int:m_id>/calexport/<int:c_id>/', vg.views.exportcalibratedmeasurement),
    path('view/<int:id>/cal/', ListView.as_view(model=Calibration, template_name='vg/choosecalibration_list.html')),
    path('cal/', ListView.as_view(model=Calibration, template_name='vg/calibration_list.html')),
    path('journal/', ListView.as_view(model=JournalEntry, template_name='vg/journalentry_list.html')),
    path('export/<int:id>/', vg.views.exportmeasurement),
    path('insight/<parameter1>/<parameter2>/', vg.views.plot_parameters),
    path('insight/', lambda x: HttpResponseRedirect('ion_repeller/ion_energy/')),
    path('insight/<parameter1>/', vg.views.plot_parameters),
    path('view/<int:m_id>/fit/<int:n_peaks>/', vg.views.fitmeasurement),
    path('view/<int:m_id>/cal/<int:c_id>/fit/<int:n_peaks>/', vg.views.fitcalmeasurement),
    path('export_all_f_urls/', vg.views.export_all_f_urls),
    path('export_all_sf6_urls/', vg.views.export_all_sf6_urls),
    path('export_all_sf5_urls/', vg.views.export_all_sf5_urls),
    path('export_all_f2_urls/', vg.views.export_all_f2_urls),
    path('all_usable_es/', vg.views.all_usable_es),
    path('pumps/', ListView.as_view(model=Turbopump, template_name='vg/pump_list.html')),
    path('pumps/<int:pumpnumber>', vg.views.pump),
]
