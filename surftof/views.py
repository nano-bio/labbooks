from datetime import datetime
from glob import glob
from json import loads
from os.path import basename
from random import randint

import h5py
import numpy as np
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView
from requests import get
from rest_framework.permissions import BasePermission

from surftof.admin import PotentialSettingsAdmin, MeasurementsAdmin
from surftof.helper import get_measurements_and_journal_entries_per_month
from surftof.helper import import_pressure, get_temp_from_file, masses_from_file
from surftof.models import PotentialSettings, Measurement


def json_export(request, table, pk):
    try:
        table = str(table).lower()
        pk = int(pk)
    except ValueError:
        raise Http404("Table or pk format invalid!")
    if table == "measurement":
        obj = get_object_or_404(Measurement, pk=pk)
    elif table == 'potentials' or table == 'potentialsettings':
        obj = get_object_or_404(PotentialSettings, pk=pk)
    else:
        raise Http404("Table unknown!")
    serialized_obj = serializers.serialize('json', [obj, ])
    return HttpResponse(serialized_obj, content_type='application/json')


def preview(request):
    return render(request, 'surftof/previewData.html', {
        'measurements': preview_list_of_measurements(10)})


def preview_data(request):
    MASS_SPEC_TIME_BIN_MAX = 60000

    if request.method == 'POST':
        time_bin_or_mass = request.POST.get('timeBinOrMass')
        data_id_file_1 = request.POST.get('dataIdFile1')
        data_id_file_2 = request.POST.get('dataIdFile2')
        scale_data_file_2 = request.POST.get('scaleDataFile2')
        diff_plot = request.POST.get('diffPlot')
        binned_by = int(request.POST.get('binnedBy'))
        max_time_bin = int(request.POST.get('maxTimeBin'))
    else:
        return HttpResponse('This is a post only view')

    # get y-axis data from h5 file
    file = glob("{}{}/*h5".format(settings.SURFTOF_BIGSHARE_DATA_ROOT, int(data_id_file_1)))[-1]
    with h5py.File(file, 'r')as f:
        y_data1 = np.array(f['SPECdata']['AverageSpec'])[:MASS_SPEC_TIME_BIN_MAX]
        y_data1 = reduce_data_by_mean(y_data1, binned_by, 1)

        # x-axis
        if time_bin_or_mass == 'mass':
            xlabel = "m/z"
            x_data = masses_from_file(f, len(y_data1), binned_by)[:MASS_SPEC_TIME_BIN_MAX]
            # x_data = reduce_data_by_mean(x_data, binned_by, 1)

        else:
            x_data = range(binned_by - 1, max_time_bin, binned_by)
            xlabel = "time bins"

    if data_id_file_2:
        file = glob("{}{}/*h5".format(settings.SURFTOF_BIGSHARE_DATA_ROOT, int(data_id_file_2)))[-1]
        with h5py.File(file, 'r')as f:
            y_data2 = np.array(f['SPECdata']['AverageSpec'])[:MASS_SPEC_TIME_BIN_MAX]
            y_data2 = reduce_data_by_mean(y_data2, binned_by, float(scale_data_file_2))

    # create json string from y-axis data
    response = '{"data":['
    for i in range(min([len(y_data1), len(x_data)])):
        if not data_id_file_2:
            response += "[{},{:.2e}],".format(x_data[i], y_data1[i])
        elif diff_plot == 'true':
            response += "[{},{:.2e}],".format(x_data[i], y_data1[i] - y_data2[i])
        else:
            response += "[{},{:.2e},{:.2e}],".format(x_data[i], y_data1[i], y_data2[i])
    response = response[:-1]  # remove last ','

    # append labels to json string
    if not data_id_file_2:
        labels = '["time bin","cps ID {}"]'.format(data_id_file_1)
    elif diff_plot == 'true':
        labels = '["time bin","cps ID {} - cps ID {}"]'.format(data_id_file_1, data_id_file_2)
    else:
        labels = '["time bin","cps ID {}","cps ID {}"]'.format(data_id_file_1, data_id_file_2)

    response += '],"xlabel":"{}","labels":{}}}'.format(xlabel, labels)

    return HttpResponse(response, content_type='application/json')


def preview_trace(request):
    if request.method != "POST":
        raise Http404("Wrong method")

    mass_min = int(request.POST.get('massMin'))
    mass_max = int(request.POST.get('massMax'))
    measurement_id = int(request.POST.get('measurementId'))

    file = glob("{}{}/*h5".format(settings.SURFTOF_BIGSHARE_DATA_ROOT, int(measurement_id)))[-1]
    infile = h5py.File(file, 'r')
    data = infile[u'SPECdata/Intensities']
    trace_points = data.shape[0]

    norm_factor = infile.attrs["Single Spec Duration (ms)"][0] / 1000

    integrated_intervals = np.zeros([trace_points])

    for b in range(trace_points):
        integrated_intervals[b] = np.sum(data[b, mass_min:mass_max])

    times = np.round(np.arange(trace_points) * norm_factor + norm_factor / 2, 1)

    return JsonResponse({'data': np.column_stack((times, integrated_intervals)).tolist()}, safe=False)


def preview_xkcd(request):
    url = "https://xkcd.com/info.0.json"
    data = loads(get(url).content.decode())
    rand_num = randint(1, int(data['num']))

    url = "https://xkcd.com/{}/info.0.json".format(rand_num)
    data = loads(get(url).content.decode())
    return render(request, 'surftof/modal_content.html', {
        'title': data['safe_title'],
        'img_url': data['img'],
        'img_alt': data['alt'],
    })


def preview_get_file_info(request, measurement_id):
    response = []
    measurement = get_object_or_404(Measurement, pk=int(measurement_id))
    pressures = import_pressure(measurement_id)
    response.append({'key': 'ID', 'value': measurement.id})
    response.append({'key': 'Impact Energy', 'value': measurement.get_impact_energy_surface()})
    response.append({'key': 'Temperature', 'value': get_temp_from_file(measurement_id)})
    response.append({'key': 'Projectile', 'value': "{}".format(measurement.projectile)})
    response.append({'key': 'Gas Surf', 'value': "{}".format(measurement.gas_surf.__str__())})
    response.append({'key': 'Pressure IS', 'value': "{:.1e} mbar".format(pressures['is'])})
    response.append({'key': 'Pressure Surf', 'value': "{:.1e} mbar".format(pressures['surf'])})
    response.append({'key': 'Pressure Tof', 'value': "{:.1e} mbar".format(pressures['tof'])})
    return JsonResponse(response, safe=False)


# for preview_data
def reduce_data_by_mean(data, binning, scale):
    mean_value = 0
    reduced_date = []
    for i, v in enumerate(data):
        mean_value += v
        if i % binning == binning - 1:
            reduced_date.append(mean_value / binning * scale)
            mean_value = 0
    return reduced_date


def preview_list_of_measurements(limit=None):
    response = []
    objects = Measurement.objects.order_by('-id')[:limit]
    for measurement in objects:
        name = f"ID {measurement.id}: {measurement.short_description}"
        if measurement.get_impact_energy_surface() != "-":
            name += f", {measurement.get_impact_energy_surface()}"
        if measurement.surface_temperature is not None:
            name += f", {measurement.surface_temperature} C"
        name += "<br>"
        if measurement.projectile is not None:
            name += f"{measurement.projectile}"
        if measurement.surface_material is not None:
            name += f" on {measurement.surface_material}"
        if measurement.gas_surf is not None:
            name += f" with {measurement.gas_surf}"

        response.append({
            'id': measurement.id,
            'name': name
        })
    return response


# for preview data
def preview_file_list(request):
    return JsonResponse(preview_list_of_measurements(), safe=False)


# update the rating of a measurement
def set_rating_of_measurement(request, measurement_id, rating):
    if request.user.has_perm('surftof.add_measurement'):
        obj = get_object_or_404(Measurement, pk=measurement_id)
        obj.rating = int(rating)
        obj.save()
        return redirect('/admin/surftof/measurement/')


class SurfTofPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('surftof.add_measurement')


class TableViewer(ListView):
    paginate_by = 50
    template_name = "surftof/table_list.html"

    def get_queryset(self):
        table = self.kwargs['table']
        if table == "PotentialSettings":
            self.model = PotentialSettings
            self.model_admin = PotentialSettingsAdmin
        elif table == "Measurement":
            self.model = Measurement
            self.model_admin = MeasurementsAdmin
        else:
            raise Http404("No model matches the given query.")
        return self.model.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(TableViewer, self).get_context_data(**kwargs)
        context['fields'] = flat_field_list(self.model_admin)
        return context


def flat_field_list(model_admin):
    field_list = []
    for field_set in model_admin.fieldsets:
        for field in field_set[1]['fields']:
            if isinstance(field, tuple):
                for inline_field in field:
                    field_list.append(inline_field)
            else:
                field_list.append(field)
    return field_list


def surface_temperature(request):
    f = "{}temperature/*.csv".format(settings.SURFTOF_BIGSHARE_DATA_ROOT)
    file_names = glob(f)
    file_names.sort(reverse=True)
    file_names = [basename(f)[:10] for f in file_names]
    newest_date = reverse(surface_temperature_data, args=[file_names[0]])
    return render(request, 'surftof/surfaceTemperature.html', {'files': file_names, 'newest_date': newest_date})


def surface_temperature_data(request, date):
    date = datetime.strptime(date, '%Y-%m-%d')
    with open("{}temperature/{}_temperaturePT100.csv".format(
            settings.SURFTOF_BIGSHARE_DATA_ROOT, date.strftime('%Y-%m-%d'))) as f:
        file_data = f.read()
    return HttpResponse(file_data)


def overview(request):
    return render(
        request=request,
        template_name='surftof/index.html',
        context={
            'month': now().strftime("%B %Y"),
            'entries': get_measurements_and_journal_entries_per_month(now())
        }
    )
