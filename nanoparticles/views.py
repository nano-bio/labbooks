import base64
import pickle

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.views.generic import ListView

from nanoparticles.admin import MeasurementAdmin
from nanoparticles.models import MeasurementData, Measurement


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


# new_mage()
def image_data(request, measurement_id, measurement_type, smoothing):
    m = MeasurementData.objects.filter(
        measurement_id=measurement_id
    ).values(
        measurement_type + '_data'
    )
    np_bytes = base64.b64decode(m[0].get(measurement_type + '_data'))

    np_array = pickle.loads(np_bytes)
    return JsonResponse({
        'data': rebin(
            np_array,
            (int(1024 / smoothing), int(1024 / smoothing))
        ).tolist()
    })


def redirect_image(request, measurement_id, measurement_type):
    measurement_type += '_image'
    m_data = MeasurementData.objects \
        .filter(measurement_id=measurement_id) \
        .values(measurement_type)

    if len(m_data) != 1:
        url = static('img/worker.png')
    else:
        relative_url = m_data[0][measurement_type]
        if relative_url:
            url = settings.MEDIA_URL + relative_url
        else:
            url = static('img/worker.png')

    return redirect(url)
