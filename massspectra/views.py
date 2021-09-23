import numpy as np
from django.contrib.admin import ModelAdmin
from django.core import serializers
from django.db.models import Model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
        data = np.genfromtxt(file_path, delimiter='\t')
        return data[:, 0], data[:, 1]
    except:
        data = np.genfromtxt(file_path, delimiter=',')
        return data[:, 0], data[:, 1]


def bin_array(arr, binning):
    return arr[:int(arr.shape[0] / binning) * binning].reshape(-1, binning).mean(axis=1)


def slice_data(x_data, y_data, x_min, x_max):
    # returns part of the x and y data as a function of
    # x min and x max
    def find_index_of_nearest(array, value):
        array = np.asarray(array)
        return (np.abs(array - value)).argmin()

    x_min_index = find_index_of_nearest(x_data, x_min)
    x_max_index = find_index_of_nearest(x_data, x_max)

    x_data = x_data[x_min_index:x_max_index]
    y_data = y_data[x_min_index:x_max_index]

    return x_data, y_data


def interpolate_data(x1, y1, x2, y2):
    x_min = max(min(x1), min(x2))
    x_max = min(max(x1), max(x2))
    x_new = np.linspace(x_min, x_max, max(len(x1), len(x2)))
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

        if not np.array_equal(x_data1, x_data2):
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


class MassSpectraListView(ListView):
    model: Model = None  # define the Measurement Model from an experiment
    model_admin: ModelAdmin = None  # define the corresponding Admin Measurement Model
    experiment_name: str = None  # set the verbose experiment name, which will be shown on the page

    ordering = '-id'
    template_name = 'massspectra/mass_spectra_viewer.html'

    def get_context_data(self, **kwargs):
        context = super(MassSpectraListView, self).get_context_data(**kwargs)
        context['experiment'] = self.experiment_name
        context['admin_measurement_url'] = reverse(f'admin:{self.model._meta.app_label}_measurement_changelist')
        context['url_data'] = reverse(f'{self.model._meta.app_label}-mass-spectra-data')
        context['url_json_file_info'] = reverse(f'{self.model._meta.app_label}-measurement-json', args=('00',))
        context['fields'] = field_names_verbose_names(self.model_admin, self.model)
        return context


@require_POST
def get_toffy_like_mass_spectra_data(request, measurement_model):
    data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)
    file_1 = measurement_model.objects.get(pk=int(data_id_file_1)).data_file.path
    x_data1, y_data1 = get_mass_spectrum_from_csv(file_1)
    if data_id_file_2:
        file_2 = measurement_model.objects.get(pk=int(data_id_file_2)).data_file.path
        x_data2, y_data2 = get_mass_spectrum_from_csv(file_2)
        return mass_spectra_data(request, x_data1, y_data1, x_data2, y_data2)
    else:
        return mass_spectra_data(request, x_data1, y_data1)
