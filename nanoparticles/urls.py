from django.urls import path
from django.views.generic import ListView

from nanoparticles.models import Measurement
from nanoparticles.views import new_mage, image_data

urlpatterns = [
    path('a/', new_mage),
    path('image-data/<int:measurement_id>', image_data, name='nanoparticles-image-data'),
    path('measurements/', ListView.as_view(model=Measurement), name='nanoparticles-measurements'),
]
