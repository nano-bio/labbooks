import traceback
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
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from requests import get

from massspectra.views import mass_spectra_data
from surftof.admin import PotentialSettingsAdmin, MeasurementsAdmin
from surftof.helper import get_mass_spectrum_preview_image, get_mass_spectrum
from surftof.models import PotentialSettings, Measurement


# ------------
# Mass Spectra
# ------------
@require_POST
def get_mass_spectra_data(request):
    data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)

    x_data1, y_data1 = get_mass_spectrum(data_id_file_1)

    if data_id_file_2:
        x_data2, y_data2 = get_mass_spectrum(data_id_file_2)
        return mass_spectra_data(request, x_data1, y_data1, x_data2, y_data2)

    else:
        return mass_spectra_data(request, x_data1, y_data1)


# -------------------
# Mass Spectra Traces
# -------------------
def mass_spectra_trace(request):
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


def mass_spectra_xkcd(request):
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


# update the rating of a measurement
def set_rating_of_measurement(request, measurement_id, rating):
    if request.user.has_perm('surftof.add_measurement'):
        obj = get_object_or_404(Measurement, pk=measurement_id)
        obj.rating = int(rating)
        obj.save()
        return redirect('/admin/surftof/measurement/')


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


def mass_spec_preview_image(request, measurement_id):
    try:
        mass_max = float(request.COOKIES['previewMassMax'])
    except (KeyError, ValueError):  # use defaults
        mass_max = 80
    try:
        use_log = request.COOKIES['previewShowLog'].lower() in ['true', '1', 't']
    except (KeyError, ValueError):  # use defaults
        use_log = False
    try:
        pixel_width = int(request.COOKIES['previewWidth'])
    except (KeyError, ValueError):  # use defaults
        pixel_width = 400
    try:
        pixel_height = int(request.COOKIES['previewHeight'])
    except (KeyError, ValueError):  # use defaults
        pixel_height = 150
    try:
        show_x_axis = request.COOKIES['previewShowMassAxis'].lower() in ['true', '1', 't']
    except (KeyError, ValueError):  # use defaults
        show_x_axis = True

    try:
        content = get_mass_spectrum_preview_image(
            measurement_id,
            mass_max,
            use_log,
            pixel_height,
            pixel_width,
            show_x_axis)

        html = HttpResponse(content, content_type="image/png")

    except:
        traceback.print_exc()
        html = HttpResponse(status=404, content="could not create image preview")

    html.set_cookie('previewMassMax', f'{mass_max}', max_age=None)
    html.set_cookie('previewShowLog', f"{use_log}", max_age=None)
    html.set_cookie('previewWidth', f"{pixel_width}", max_age=None)
    html.set_cookie('previewHeight', f"{pixel_height}", max_age=None)
    html.set_cookie('previewShowMassAxis', f"{show_x_axis}", max_age=None)
    return html
