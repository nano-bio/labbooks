from datetime import timedelta
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from poweralarm.models import Experiment

from labinventory.models import Temperature


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


def temperature_is_critical(request):
    if cache.get('send_temp_alert') is None and Temperature.objects \
            .filter(date_time__gt=now() - timedelta(minutes=30)) \
            .filter(temp_sensor_1__gt=30) \
            .count() > 3:

        commandline_sms = "echo 'Temperature alert for prevacuum room. Check http://138.232.74.41/labinventory/" \
                          "temperature/' | gnokii --sendsms {}"
        commandline_mail = "echo 'Temperature alert for prevacuum room. Check http://138.232.74.41/labinventory/" \
                           "temperature/' | mail -s LabAlert {}"

        commands = []
        exp = get_object_or_404(Experiment, name="TEMPALERT")
        for user in exp.persons.all():
            if user.mobile is not None:
                commands.append(
                    commandline_sms.format(
                        user.mobile.replace(' ', '').replace('/', '')))
            if user.email:
                commands.append(
                    commandline_mail.format(user.email))

        response = {
            'is_critical': True,
            'commands': commands
        }
        cache.set('send_temp_alert', True, 3600 * 24)  # send alert only once in 24h
    else:
        response = {'is_critical': False}

    return JsonResponse(data=response)
