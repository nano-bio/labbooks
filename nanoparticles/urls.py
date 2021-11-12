from django.urls import path

from nanoparticles.views import get_image

urlpatterns = [
    path('image/<int:measurement_id>/<measurement_type>.png',
         get_image,
         name='surftof-journal'),
]
