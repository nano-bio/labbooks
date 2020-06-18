from django.conf.urls import url
from django.views.generic import TemplateView

from labinventory import views

urlpatterns = [
    url(r'temperature/data/',
        views.get_temp_data,
        name='lab-temp-data'),
    url(r'temperature/put/',
        views.add_temperature),
    url(r'temperature/is-critical/',
        views.temperature_is_critical),
    url(r'temperature/',
        TemplateView.as_view(
            template_name='labinventory/viewTemperature.html'),
        name="lab-temp"),
]
