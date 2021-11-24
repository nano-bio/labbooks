import numpy
from NSFopen.read import read as afmreader
from django.http import JsonResponse, Http404
from django.views.generic import ListView

from nanoparticles.admin import MeasurementAdmin
from nanoparticles.models import Measurement


class TableViewer(ListView):
    paginate_by = 20
    model = Measurement
    ordering = '-id'
    model_admin = MeasurementAdmin

    def get_context_data(self, **kwargs):
        context = super(TableViewer, self).get_context_data(**kwargs)
        context['fields'] = [f.name for f in self.model._meta.fields]
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


def rebin(a, shape):
    sh = shape[0], a.shape[0] // shape[0], shape[1], a.shape[1] // shape[1]
    return a.reshape(sh).mean(-1).mean(1)


def image_data(request, measurement_id, direction, measurement_type, smoothing):
    try:
        file_name = Measurement.objects.get(id=measurement_id).nid_file.path
        f = afmreader(file_name, verbose=False)

        np_array = numpy.array(
            f.data['Image'][direction][measurement_type],
            dtype=float)
        return JsonResponse({
            'data': rebin(
                np_array,
                (int(1024 / smoothing), int(1024 / smoothing))
            ).tolist()
        })
    except Exception as e:
        return Http404(f'{e}')
