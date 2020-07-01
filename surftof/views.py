import itertools
from datetime import datetime, timedelta
from glob import glob
import numpy as np
import h5py
from django.db.models import FloatField, Count
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from scipy.optimize import curve_fit

from surftof.admin import PotentialSettingsAdmin, MeasurementsAdmin
from surftof.models import IsegAssignments, PotentialSettings, Measurement, CountsPerMass, Gas, Surface, MeasurementType
from django.core import serializers
from surftof.serializers import CountsPerMassSerializer
from requests import get
from json import loads, dumps
from random import randint

root = "/mnt/bigshare/Experiments/SurfTOF/Measurements/rawDATA/"


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


# for preview_data
def masses_from_file(h5py_file, length_y_data, binned_by):
    def quadratic_fit_function(x, a, t0):
        return a * (x + t0) ** 2

    x_data = np.array(h5py_file['CALdata']['Mapping'])
    masses = []
    times = []
    for row in x_data:
        if row[0] != 0 and row[1] != 0:
            masses.append(row[0])
            times.append(row[1])
    popt, pcov = curve_fit(quadratic_fit_function, times, masses, p0=(1e-8, 10000))
    return quadratic_fit_function(np.array(np.arange(length_y_data) * binned_by), *popt)


def preview_data(request):
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
    file = glob("{}{}/*h5".format(root, int(data_id_file_1)))[-1]
    with h5py.File(file, 'r')as f:
        y_data1 = np.array(f['SPECdata']['AverageSpec'])
        y_data1 = reduce_data_by_mean(y_data1, binned_by, 1)

        # x-axis
        if time_bin_or_mass == 'mass':
            xlabel = "m/z"
            x_data = masses_from_file(f, len(y_data1), binned_by)
            # x_data = reduce_data_by_mean(x_data, binned_by, 1)

        else:
            x_data = range(binned_by - 1, max_time_bin, binned_by)
            xlabel = "time bins"

    if data_id_file_2:
        file = glob("{}{}/*h5".format(root, int(data_id_file_2)))[-1]
        with h5py.File(file, 'r')as f:
            y_data2 = np.array(f['SPECdata']['AverageSpec'])
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

    file = glob("{}{}/*h5".format(root, int(measurement_id)))[-1]
    infile = h5py.File(file, 'r')
    data = infile[u'SPECdata/Intensities']
    trace_points = data.shape[0]

    norm_factor = infile.attrs["Single Spec Duration (ms)"][0] / 1000

    integrated_intervals = np.zeros([trace_points])

    for b in range(trace_points):
        integrated_intervals[b] = np.sum(data[b, mass_min:mass_max])

    integrated_intervals *= norm_factor
    times = np.arange(trace_points) * norm_factor + norm_factor / 2

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


def import_pressure(id):
    pressures = {}
    try:
        pressure_file = glob(root + str(id) + "/*ressure*")[0]
        a = np.loadtxt(pressure_file, delimiter='\t',
                       dtype=[('a', '|S8'), ('b', '<f4'), ('c', '<f4'),
                              ('d', '<f4'), ('e', '<f4'), ('f', '<f4'),
                              ('g', '<f4')], skiprows=1)
        ionsource = []
        surf = []
        tof = []
        for b in a:
            ionsource.append(b[1])
            surf.append(b[2])
            tof.append(b[3])
        pressures['is'] = np.median(ionsource)
        pressures['surf'] = np.median(surf)
        pressures['tof'] = np.median(tof)
    except:
        pressures['is'] = -1
        pressures['surf'] = -1
        pressures['tof'] = -1
    return pressures


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


def get_temp_from_file(measurement_id):
    try:
        h5_file_name = glob("{}{}/*h5".format(root, int(measurement_id)))[-1]
        with h5py.File(h5_file_name, 'r') as f:
            file_start = datetime.strptime(dict(f.attrs.items())['FileCreatedTimeSTR_LOCAL'][0].decode(),
                                           "%d/%m/%Y %Hh %Mm %Ss")
            file_duration = int(
                dict(f.attrs.items())['Single Spec Duration (ms)'][0] / 1000 * len(f['SPECdata']['Intensities']))
            file_end = file_start + timedelta(seconds=file_duration)
            filenames = ["{}_temperaturePT100.csv".format(file_start.strftime("%Y-%m-%d"))]
            if file_end.date() != file_start.date():
                filenames.append("{}_temperaturePT100.csv".format(file_end.strftime("%Y-%m-%d")))

            temps = []
            for filename in filenames:
                with open(root + 'temperature/' + filename, 'r') as g:
                    for line in g:
                        line_time = datetime.strptime(line.strip().split(',')[0][:19], '%Y-%m-%dT%H:%M:%S')
                        if file_start < line_time < file_end:
                            temps.append(float(line.strip().split(',')[1]))
            return "{:.1f} &#176;C".format(np.median(temps))
    except:
        return "-1 &#176;C"


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


# for preview data
def preview_file_list(request):
    # get all measurements from DB
    objects = Measurement.objects.order_by('-time')

    response = []
    for key, group in itertools.groupby(objects, key=lambda x: x.time.date()):
        tmp = {'date': key, 'times': []}
        for val in group:
            tmp['times'].append({
                'time': val.time.strftime('%H:%M'),
                'id': val.id,
                'name': "ID {}, {} eV, {} C<br> {} on {} with {}".format(val.id, val.impact_energy_surface,
                                                                         val.surface_temperature, val.projectile,
                                                                         val.surface_material, val.gas_surf)
            })
        response.append(tmp)
    response = []
    for obj in objects:
        response.append({
            'id': obj.id,
            'name': "ID {}, {}, {} C<br> {} on {} with {}".format(obj.id, obj.get_impact_energy_surface(),
                                                                  obj.surface_temperature, obj.projectile,
                                                                  obj.surface_material, obj.gas_surf)
        })
    return JsonResponse(response, safe=False)


# update the rating of a measurement
def set_rating_of_measurement(request, id, rating):
    if request.user.has_perm('surftof.add_measurement'):
        obj = get_object_or_404(Measurement, pk=id)
        obj.rating = int(rating)
        obj.save()
        return redirect('/admin/surftof/measurement/')


class SurfTofPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('surftof.add_measurement')


class CountsPerMassViewSet(viewsets.ModelViewSet):
    permission_classes = [SurfTofPermission]
    queryset = CountsPerMass.objects.all()
    serializer_class = CountsPerMassSerializer


def cpm_filter_ids(request):
    if request.method == 'POST':
        # get POST data
        # get energy
        filter_energy = request.POST.get('filterEnergy', True)
        filter_energy_lower = request.POST.get('filterEnergyLower', -1e20)
        filter_energy_upper = request.POST.get('filterEnergyUpper', 1e20)

        # get temperature
        filter_temp = request.POST.get('filterTemp', True)
        filter_temp_lower = request.POST.get('filterTempLower', 0)
        filter_temp_upper = request.POST.get('filterTempUpper', 1e20)

        # build query
        ids = CountsPerMass.objects.all()
        if filter_energy:
            ids.filter(surface_impact_energy__gte=filter_energy_lower)
            ids.filter(surface_impact_energy__lte=filter_energy_upper)
        if filter_temp:
            ids.filter(surface_temperature__gte=filter_temp_lower)
            ids.filter(surface_temperature__lte=filter_temp_upper)

        measurement_ids = list(dict.fromkeys(  # removes duplicates
            list(ids.values_list('measurement__id', flat=True))))
        measurement_ids.sort(reverse=True)
        masses = list(dict.fromkeys(  # removes duplicates
            list(ids.order_by('mass').values_list('mass', flat=True))))

        return JsonResponse({'measurements': measurement_ids, 'masses': masses}, safe=False)


def cpm_data(request):
    if request.method == 'POST':

        # parse request
        measurement_ids = [int(x) for x in request.POST.getlist('ids[]')]
        masses = [int(x) for x in request.POST.getlist('masses[]')]
        x_axis = request.POST.get('x')
        diff_plots = request.POST.get('diffPlots')

        if x_axis == 'mass':
            x_label = 'm/z'
            order_by = 'mass'

        elif x_axis == 'energy':
            x_label = 'Energy [eV]'
            order_by = 'surface_impact_energy'

        elif x_axis == 'temperature':
            x_label = 'Temperature'
            order_by = 'surface_temperature'

        else:
            return Http404()

        # get objects
        data = CountsPerMass.objects.all()

        # filter measurements
        data = data.filter(measurement_id__in=measurement_ids)

        # filter masses
        data = data.filter(mass__in=masses)

        # order by x axis
        data = data.order_by(order_by)

        response = {
            'data': [],
            'xLabel': x_label
        }
        if diff_plots == 'single':
            response['labels'] = [x_label, 'counts']
            for i in data:
                if i.__getattribute__(order_by):
                    response['data'].append([
                        i.__getattribute__(order_by), [
                            i.counts - i.counts_err,
                            i.counts,
                            i.counts + i.counts_err]
                    ])
        else:
            # group by x axis
            groups = list(dict.fromkeys(
                data.values(diff_plots).annotate(dcount=Count(diff_plots)).values_list(diff_plots, flat=True)))
            groups = [i for i in groups if i]
            groups.sort()
            response['log'] = groups

            data_dict = {}
            response['labels'] = [x_label, ]

            for filter in groups:
                kwargs = {'{0}'.format(diff_plots): filter}

                filtered = data.filter(**kwargs)
                for i in filtered:
                    if i.__getattribute__(order_by) is None:
                        continue
                    elif i.__getattribute__(order_by) in data_dict:
                        data_dict[i.__getattribute__(order_by)][filter] = [
                            i.counts - i.counts_err,
                            i.counts,
                            i.counts + i.counts_err]
                    else:
                        data_dict[i.__getattribute__(order_by)] = {
                            filter: [
                                i.counts - i.counts_err,
                                i.counts,
                                i.counts + i.counts_err]}
                response['labels'].append(str(filter))
            data_list = []
            for k, v in data_dict.items():
                e = [k]
                for i in groups:
                    if i in v:
                        e.append(v[i])
                    else:
                        e.append(None)
                data_list.append(e)
            response['data'] = data_list

        return JsonResponse(response, safe=False)


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
