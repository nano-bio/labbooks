from django.urls import path
from django.views.generic import ListView
from django.contrib.flatpages import views as flatpageviews

from snowball.models import Measurement, JournalEntry, Turbopump

import snowball.views

urlpatterns = [
    path('',
         flatpageviews.flatpage, {'url': '/snowball/'},
         name='snowball-home'),
    path('view/',
         ListView.as_view(model=Measurement, template_name='snowball/measurement_list.html', paginate_by=100),
         name="snowball-view-measurements"),
    path('view/<int:id>/',
         snowball.views.showmeasurement,
         name="snowball-view-measurement"),
    path('journal/',
         ListView.as_view(model=JournalEntry, template_name='snowball/journalentry_list.html'),
         name="snowball-view-journals"),
    path('export/<int:id>/',
         snowball.views.exportmeasurement,
         name="snowball-view-journal"),
    path('pumps/',
         ListView.as_view(model=Turbopump, template_name='snowball/pump_list.html'),
         name="snowball-view-pumps"),
    path('pumps/<int:pumpnumber>',
         snowball.views.pump,
         name="snowball-view-pump"),
]
