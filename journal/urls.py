from django.urls import path

import journal.views as views

urlpatterns = [
    # Journal Preview Images of Mass Spectra
    path('preview-image/<experiment>/<int:measurement_id>.png',
         views.mass_spec_preview_image,
         name="journal-mass-spec-preview-image"),
]
