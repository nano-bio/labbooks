# def create_image(request, measurement_id, measurement_type):
#     start = time()
#     data = get_data_from_measurement_data_object(measurement_id, measurement_type)
#     print(time()-start)
#     return HttpResponse(make_image(data), content_type="image/png")
import io

import matplotlib.pyplot as plt
import numpy
from django.core.files.images import ImageFile
from django.http import JsonResponse

from nanoparticles.models import TestM, MeasurementData


def new_mage(request):
    xvalues, yvalues = [1, 2, 3], [4, 6, 5]
    figure = io.BytesIO()
    plt.plot(xvalues, yvalues)
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    m = TestM()
    m.image.save('name_of_image.png', content_file)
    m.save()


def rebin(a, shape):
    sh = shape[0], a.shape[0] // shape[0], shape[1], a.shape[1] // shape[1]
    return a.reshape(sh).mean(-1).mean(1)


# new_mage()
def image_data(request, measurement_id, binning=4):
    shape = (int(1024 / binning), int(1024 / binning))
    m = MeasurementData.objects.get(measurement_id=measurement_id)
    return JsonResponse({'data': [
        rebin(numpy.array(arr), shape).tolist() for arr in [
            m.forward_phase_data,
            m.forward_amplitude_data,
            m.forward_z_axis_data,
            m.backward_phase_data,
            m.backward_amplitude_data,
            m.backward_z_axis_data]
    ]})
