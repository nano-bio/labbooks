import logging
from datetime import timedelta

from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from labinventory.models import Temperature

logger = logging.getLogger('django')


@csrf_exempt
def add_temperature(request):
    if request.method == "POST" and request.POST.get("passphrase") == 'K+4BP6JdySD%dpc-w58Wp?qnHmdQ=&RuuL47Wt+A':

        try:
            temp_sensor_1 = float(request.POST.get("temp_sensor_1"))
        except:
            temp_sensor_1 = None

        try:
            temp_sensor_2 = float(request.POST.get("temp_sensor_2"))
        except:
            temp_sensor_2 = None

        if type(temp_sensor_1) == float or type(temp_sensor_2) == float:
            temp = Temperature(
                temp_sensor_1=temp_sensor_1,
                temp_sensor_2=temp_sensor_2)
            temp.save()

            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400, content="no floats")
    else:
        return HttpResponse(
            status=400, content="no POST request or wrong passphrase. POST Keys:\n{}".format(request.POST.keys()))


def get_temp_data(request):
    if request.method == "POST":
        last_hours = int(request.POST.get("lastHours"))
    else:
        last_hours = 5
    data = Temperature.objects.filter(date_time__gt=now() - timedelta(hours=last_hours))
    response = {'data': []}
    for point in data:
        response['data'].append([
            point.date_time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            point.temp_sensor_1,
            point.temp_sensor_2])

    return JsonResponse(response)
