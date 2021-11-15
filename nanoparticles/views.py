from time import time

from django.http import HttpResponse

from nanoparticles.helper import get_data_from_measurement_data_object, make_image


def get_image(request, measurement_id, measurement_type):
    start = time()
    data = get_data_from_measurement_data_object(measurement_id, measurement_type)
    print(time()-start)
    return HttpResponse(make_image(data), content_type="image/png")
