from django.contrib.auth.decorators import login_required
from django.urls import path

import massspectra.views
from clustof.admin import MeasurementAdmin
from clustof.models import Measurement, JournalEntry, Turbopump
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib.flatpages import views as flatpageviews
import clustof.views
import journal.views

urlpatterns = [
    path('newmeasurement/',
         clustof.views.newmeasurement,
         name="clustof-newmeasurement"),
    path('view/',
         ListView.as_view(model=Measurement, template_name='clustof/measurement_list.html', paginate_by=100),
         name="clustof-view-measurements"),
    path('pumps/',
         ListView.as_view(model=Turbopump, template_name='clustof/pump_list.html'),
         name="clustof-view-pumps"),
    path('pumps/<int:pumpnumber>',
         clustof.views.pump,
         name="clustof-view-pump"),
    path('insight/<parameter1>/<parameter2>/',
         clustof.views.plot_parameters,
         name="clustof-insight-parameter1-parameter2"),
    path('insight/',
         lambda x: HttpResponseRedirect('extraction_1/extraction_2/'),
         name="clustof-insight"),
    path('insight/<parameter1>/',
         clustof.views.plot_parameters,
         name="clustof-insight-parameter1"),
    path('',
         flatpageviews.flatpage, {'url': '/clustof/'},
         name='clustof-home'),
    path('export/<int:id>/',
         clustof.views.exportfile,
         name="clustof-exportfile"),
    path('export/<int:id>/filename',
         clustof.views.exportfilename,
         name="clustof-exportfilename"),
    path('json/<int:count>/',
         clustof.views.mjson,
         name="clustof-mjson"),
    path('csv/<int:count>/<int:offset>/',
         clustof.views.mcsv,
         name="clustof-mcsv-count-offset"),
    path('csv/<int:count>/',
         clustof.views.mcsv,
         name="clustof-mcsv-count"),
    path('csv/',
         clustof.views.mcsv,
         name="clustof-mcsv"),
    path('vacuumstatus/input/',
         clustof.views.readvacuumstatus,
         name="clustof-readvacuumstatus"),
    path('vacuumstatus/output/<int:after>/<int:before>/',
         clustof.views.writevacuumstatus,
         name="clustof-writevacuumstatus-after-before"),
    path('vacuumstatus/output/<int:after>/',
         clustof.views.writevacuumstatus,
         name="clustof-writevacuumstatus-after"),
    path('vacuumstatus/output/',
         clustof.views.writevacuumstatus,
         name="clustof-writevacuumstatus"),
    path('filetest/',
         clustof.views.filetest,
         name="clustof-filetest"),
    path('public/',
         clustof.views.PublicMeasurementList.as_view(),
         name="clustof-public-measurements"),
    path('public/<int:pk>/',
         clustof.views.PublicMeasurementDetailView.as_view(),
         name="clustof-public-measurement"),
    path('public/<int:pk>/export/',
         clustof.views.exportfile_public,
         name="clustof-public-exportfile"),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraListView.as_view(
             model=Measurement,
             model_admin=MeasurementAdmin,
             experiment_name='ClusTOF'),
         name="clustof-mass-spectra"),
    path('mass-spectra/data/',
         clustof.views.get_mass_spectra_data,
         name="clustof-mass-spectra-data"),

    # json export measurement
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="clustof-measurement-json"),

    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='ClusTof'),
         name='clustof-journal'),
    path('journal/add/',
         login_required(journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='ClusTof')),
         name='clustof-journal-add'),
    path('journal/<int:pk>/',
         login_required(journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry)),
         name='clustof-journal-update'),
    path('journal/<int:pk>/delete/',
         login_required(journal.views.JournalEntryDelete.as_view(
             model=JournalEntry)),
         name='clustof-journal-delete'),
]
