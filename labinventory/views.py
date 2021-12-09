import logging
import os
from datetime import timedelta

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from labinventory.models import Temperature, Person

logger = logging.getLogger('django')


def power_alarm(request, fail_clear):
    if request.user.username != 'gnooki':
        return HttpResponse(status=403, content=f"Wrong user: '{request.user}', must be 'gnooki'")
    if fail_clear not in ['fail', 'clear']:
        raise Exception("Alarm needs argument 'fail' or 'clear'!")
    users = Person.objects.filter(get_power_alarm=True)

    if fail_clear == "fail":
        message = "Power failure in the lab!"
    else:
        message = "Power returned in the lab!"
    send_sms = 0
    send_mails = 0
    for user in users:
        if user.mobile:
            try:
                command = f'echo "{message}" | gnokii --sendsms {user.mobile}'
                os.system(command)
                send_sms += 1
            except Exception as e:
                logger.error(f"PowerAlarm send sms failed: {e}")
        if user.email:
            try:
                send_mail('LabAlert2', message, 'labbooks-server@uibk.ac.at', [user.email])
                send_mails += 1
            except Exception as e:
                logger.error(f"PowerAlarm send mail failed: {e}")

    return HttpResponse(f"Send {send_sms} SMS and {send_mails} Mails.")


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
        users = Person.objects.filter(get_temperature_alarm=True)
        for user in users:
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
