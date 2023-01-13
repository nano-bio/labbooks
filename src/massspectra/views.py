import datetime
from json import JSONEncoder
from os.path import exists

import h5py
import numpy
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.core import serializers
from django.db.models import Model, F
from django.db.models.functions import Substr
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from scipy.interpolate import interp1d


def reduce_data_by_mean(data, binning, scale=1):
    mean_value = 0
    reduced_date = []
    for i, v in enumerate(data):
        mean_value += v
        if i % binning == binning - 1:
            reduced_date.append(mean_value / binning * scale)
            mean_value = 0
    return reduced_date


def json_export(request, pk, model):
    obj = get_object_or_404(model, pk=pk)
    return HttpResponse(
        serializers.serialize("json", [obj, ]),
        content_type='application/json')


def field_names_verbose_names(model_admin, model):
    field_list = []
    for field_set in model_admin.fieldsets:
        for field in field_set[1]['fields']:
            if isinstance(field, tuple):
                for inline_field in field:
                    field_list.append(inline_field)
            else:
                field_list.append(field)
    return [{
        'name': field,
        'verbose_name': model._meta.get_field(field).verbose_name.title()
    } for field in field_list]


def get_mass_spectrum_from_csv(file_path):
    try:
        data = numpy.genfromtxt(file_path, delimiter='\t')
        return data[:, 0], data[:, 1]
    except:
        data = numpy.genfromtxt(file_path, delimiter=',')
        return data[:, 0], data[:, 1]


def bin_array(arr, binning):
    return arr[:int(arr.shape[0] / binning) * binning].reshape(-1, binning).mean(axis=1)


def slice_data(x_data, y_data, x_min, x_max):
    # returns part of the x and y data as a function of
    # x min and x max
    def find_index_of_nearest(array_in, value):
        array_in = numpy.asarray(array_in)
        return (numpy.abs(array_in - value)).argmin()

    x_min_index = find_index_of_nearest(x_data, x_min)
    x_max_index = find_index_of_nearest(x_data, x_max)

    x_data = x_data[x_min_index:x_max_index]
    y_data = y_data[x_min_index:x_max_index]

    return x_data, y_data


def interpolate_data(x1, y1, x2, y2):
    x_min = max(min(x1), min(x2))
    x_max = min(max(x1), max(x2))
    x_new = numpy.linspace(x_min, x_max, max(len(x1), len(x2)))

    # add zero values to start and end of spectra for working interpolation
    x1 = numpy.insert(x1, 0, [0], axis=0)
    x2 = numpy.insert(x2, 0, [0], axis=0)
    y1 = numpy.insert(y1, 0, [0], axis=0)
    y2 = numpy.insert(y2, 0, [0], axis=0)

    x1 = numpy.append(x1, [x1[-1] + 1])
    x2 = numpy.append(x2, [x2[-1] + 1])
    y1 = numpy.append(y1, [0])
    y2 = numpy.append(y2, [0])

    f1 = interp1d(x1, y1)
    f2 = interp1d(x2, y2)
    y_new_1 = f1(x_new)
    y_new_2 = f2(x_new)

    return x_new, y_new_1, y_new_2


def mass_spectra_data(request, x_data1, y_data1, x_data2=None, y_data2=None):
    # data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)
    scale_data_file_2 = float(request.POST.get('scaleDataFile2', 1))
    diff_plot = request.POST.get('diffPlot', False)
    binned_by = int(request.POST.get('binnedBy', 1))
    max_mass = int(request.POST.get('maxMass'))

    if x_data1[-1] > max_mass:
        x_data1, y_data1 = slice_data(x_data1, y_data1, 0, max_mass)
    x_data1 = bin_array(x_data1, binned_by)
    y_data1 = bin_array(y_data1, binned_by)
    if data_id_file_2:
        if x_data2[-1] > max_mass:
            x_data2, y_data2 = slice_data(x_data2, y_data2, 0, max_mass)
        x_data2 = bin_array(x_data2, binned_by)
        y_data2 = bin_array(y_data2, binned_by)
        if scale_data_file_2 != 1:
            y_data2 *= scale_data_file_2

        if not numpy.array_equal(x_data1, x_data2):
            masses, y_data1, y_data2 = interpolate_data(x_data1, y_data1, x_data2, y_data2)
        else:
            masses = x_data1
    else:
        masses = x_data1

    # create json string from xy-data
    if not data_id_file_2:
        data_str = ",".join([f"[{masses[i]:.3f},{y_data1[i]:.2e}]" for i in range(len(masses))])
    elif diff_plot == 'true':
        data_str = ",".join([f"[{masses[i]:.3f},{(y_data1[i] - y_data2[i]):.2e}]" for i in range(len(masses))])
    else:
        data_str = ",".join([f"[{masses[i]:.3f},{y_data1[i]:.2e},{y_data2[i]:.2e}]" for i in range(len(masses))])
    return HttpResponse("{" + f'"data":[{data_str}]' + "}", content_type="application/json")


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%d.%m.%Y %H:%M")
        return super(DateTimeEncoder, self).default(obj)


class MassSpectraMeasurementListJson(View):
    measurement_model: Model = None

    def get(self, request):
        if self.measurement_model._meta.app_label == 'clustof':
            # clustof uses substance as comment and too much text :-(
            measurements = self.measurement_model.objects \
                .annotate(t=Substr('substance', 1, 150)) \
                .values('id', 'time', 't', 'scantype')
        else:
            measurements = self.measurement_model.objects \
                .annotate(t=F('short_description')) \
                .values('id', 'time', 't')
        return JsonResponse(list(measurements), encoder=DateTimeEncoder, safe=False)


class MassSpectraView(ListView):
    model: Model = None  # define the Measurement Model from an experiment
    model_admin: ModelAdmin = None  # define the corresponding Admin Measurement Model
    experiment_name: str = None  # set the verbose experiment name, which will be shown on the page
    paginate_by = 50  # first paginate_by results will be rendered directly, all results will be loaded by clusterize

    template_name = 'massspectra/mass_spectra_viewer.html'

    def get_context_data(self, **kwargs):
        context = super(MassSpectraView, self).get_context_data(**kwargs)
        context['experiment'] = self.experiment_name
        context['admin_measurement_url'] = reverse(f'admin:{self.model._meta.app_label}_measurement_changelist')
        context['url_data'] = reverse(f'{self.model._meta.app_label}-mass-spectra-data')
        context['url_json_file_info'] = reverse(f'{self.model._meta.app_label}-measurement-json', args=('00',))
        context['fields'] = field_names_verbose_names(self.model_admin, self.model)
        context['mass_spectra_measurements_url'] = reverse(f'{self.model._meta.app_label}-mass-spectra-measurements')
        return context


@require_POST
def get_toffy_like_mass_spectra_data(request, measurement_model):
    data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)
    try:
        file_1 = measurement_model.objects.get(pk=int(data_id_file_1)).data_file.path
        x_data1, y_data1 = get_mass_spectrum_from_csv(file_1)
        if data_id_file_2:
            file_2 = measurement_model.objects.get(pk=int(data_id_file_2)).data_file.path
            x_data2, y_data2 = get_mass_spectrum_from_csv(file_2)
            return mass_spectra_data(request, x_data1, y_data1, x_data2, y_data2)
        else:
            return mass_spectra_data(request, x_data1, y_data1)
    except ValueError as e:
        return JsonResponse({'error': str(e)})


def get_mass_spectrum_tofwerk(file_name_full, mass_max=None):
    with h5py.File(file_name_full, 'r') as f:
        y_data = numpy.array(f['FullSpectra']['SumSpectrum'])
        x_data = numpy.array(f['FullSpectra']['MassAxis'])

    if mass_max is None:
        return x_data, y_data
    return slice_data(x_data, y_data, 0, mass_max)


def laser_scan(request, measurement_id, file_name_full, experiment, url):
    if not exists(file_name_full):
        messages.error(request, f"The file '{file_name_full}' does not exists (ID {measurement_id})")
        return redirect(f'{experiment}-mass-spectra')

    with open(file_name_full, 'rb') as f:
        hf = h5py.File(f, 'r')
        k = hf['PeakData']['PeakTable'][()]
        sections = list(range(len(hf['PeakData']['PeakData'][0, 0])))
        print(sections, hf['PeakData']['PeakData'].shape)
    mass_list = [f"{int(row[1])} ({row[2]:.1f}-{row[3]:.1f})" for row in k]
    return render(request, 'massspectra/laser_scan.html', {
        'measurement_id': measurement_id,
        'mass_list': mass_list,
        'sections': sections,
        'experiment': experiment,
        'url': url
    })


def laser_scan_data(request, file_name_full):
    mass_column = int(request.POST.get('massColumn'))
    x_start = request.POST.get('xStart', None)
    step_width = request.POST.get('stepWidth', None)
    background_mode = request.POST.get('backgroundMode', 'divide')
    try:
        sections_foreground = [int(i) for i in request.POST.get('sectionsForeground').split(',')]
    except ValueError:
        sections_foreground = [0]
    try:
        sections_background = [int(i) for i in request.POST.get('sectionsBackground', '1,2,3,4,5,6,7,8,9').split(',')]
    except ValueError:
        sections_background = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    with open(file_name_full, 'rb') as f:
        hf = h5py.File(f, 'r')
        if len(sections_foreground) == 1:
            laser_on_data = hf['PeakData']['PeakData'][:, 0, sections_foreground[0], mass_column]
        else:
            laser_on_data = numpy.mean(hf['PeakData']['PeakData'][:, 0, sections_foreground, mass_column], axis=1)

        if background_mode == 'none':
            data = laser_on_data
        else:
            if len(sections_background) == 1:
                laser_off_data = hf['PeakData']['PeakData'][:, 0, sections_background[0], mass_column]
            else:
                laser_off_data = numpy.mean(hf['PeakData']['PeakData'][:, 0, sections_background, mass_column], axis=1)

            if background_mode == 'diff':
                data = laser_on_data - laser_off_data
            elif background_mode == 'divide':
                data = laser_on_data / laser_off_data
            else:
                raise Http404('Provide either mode "diff" or mode "divide"')

    try:
        # when wavelength start and end is provided, return a xy array
        if x_start and step_width and float(step_width) != 0:
            x_start = float(x_start)
            step_width = float(step_width)
            xs = numpy.arange(0, len(data)) * step_width + x_start
        else:
            xs = range(len(data))

        return JsonResponse({'data': numpy.stack([xs, data], axis=-1).tolist()})
    except Exception as e:
        raise Http404(f'xs problem: {e}')
