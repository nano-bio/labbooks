from django.contrib.auth.decorators import login_required
from django.urls import path

import journal.views
import massspectra.views
import toffy2.views
from toffy2.admin import MeasurementAdmin
from toffy2.models import Measurement, JournalEntry

urlpatterns = [
    # Journal
    path('journal/',
         journal.views.JournalListView.as_view(
             model=JournalEntry,
             experiment='Toffy2'),
         name='toffy2-journal'),
    path('journal/add/',
         journal.views.JournalEntryCreate.as_view(
             model=JournalEntry,
             experiment='Toffy2'),
         name='toffy2-journal-add'),
    path('journal/<int:pk>/',
         journal.views.JournalEntryUpdate.as_view(
             model=JournalEntry),
         name='toffy2-journal-update'),
    path('journal/<int:pk>/delete/',
         journal.views.JournalEntryDelete.as_view(
             model=JournalEntry),
         name='toffy2-journal-delete'),

    # mass spectra
    path('mass-spectra/',
         massspectra.views.MassSpectraView.as_view(
             model=Measurement,
             model_admin=MeasurementAdmin,
             extra_context={
                 "custom_clusterize_row": "{values: `${data[i].id}${data[i].time}${data[i].t}`.toLo"
                                          "werCase(), markup: `<li class='list-group-item'><div class='m-1 mt-2'>"
                                          "ID ${data[i].id} - ${dat"
                                          "a[i].time}<br>${data[i].t}</div><button type='button' onclick='show(${data["
                                          "i].id})'class='btn btn-sm btn-outline-secondary m-1'>Show</button><button t"
                                          "ype='button' onclick='compare(${data[i].id})'class='btn btn-sm btn-outline-"
                                          "secondary m-1'>Compare</button><button type='button' onclick='diff(${data[i"
                                          "].id})'class='btn btn-sm btn-outline-secondary m-1'>Diff</button><a href='/"
                                          "admin/toffy2/measurement/${data[i].id}/change/'class='btn btn-sm btn-outli"
                                          "ne-secondary m-1'>Show Measurement</a><a href='/toffy2/laser-scan/${data[i"
                                          "].id}/' class='btn btn-sm btn-outline-secondary m-1'>Laser Scan</a></li>`, "
                                          "active: true}"},
             experiment_name='Toffy2'),
         name="toffy2-mass-spectra"),
    path('mass-spectra/measurements/',
         massspectra.views.MassSpectraMeasurementListJson.as_view(
             measurement_model=Measurement),
         name="toffy2-mass-spectra-measurements"),
    path('mass-spectra/data/',
         toffy2.views.get_mass_spectra_data,
         name="toffy2-mass-spectra-data"),

    # laser scan
    path('laser-scan/<int:measurement_id>/',
         toffy2.views.laser_scan_toffy2,
         name="toffy2-laser-scan"),
    path('laser-scan/data/',
         toffy2.views.laser_scan_data_toffy2,
         name="toffy2-laser-scan-data"),

    # json export
    path('measurement/<int:pk>.json',
         massspectra.views.json_export,
         {'model': Measurement},
         name="toffy2-measurement-json"),

    # admin update rating in measurements
    path('update-measurement-rating',
         login_required(
             toffy2.views.update_measurement_rating),
         name="toffy2-update-measurement-rating"),
]
