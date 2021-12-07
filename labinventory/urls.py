from django.urls.conf import path
from django.views.generic import TemplateView
from labinventory import views

urlpatterns = [
    path('temperature/data/',
         views.get_temp_data,
         name='labinventory-temp-data'),
    path('temperature/put/',
         views.add_temperature),
    path('temperature/is-critical/',
         views.temperature_is_critical),
    path('temperature/',
         TemplateView.as_view(template_name='labinventory/viewTemperature.html'),
         name="labinventory-temp"),
    path('power-alarm/<fail_clear>/',
         views.power_alarm,
         name="labinventory-power-alarm"),
]
