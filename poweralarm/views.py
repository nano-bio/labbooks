from django.shortcuts import get_object_or_404
from models import Experiment
from django.http import HttpResponse


# creates alarm script for experiment
def alarm(request, experiment):
    exp = get_object_or_404(Experiment, name=experiment)

    complete_command = ''
    commandline_sms = 'echo "Power failure alarm in the lab!" | gnokii --sendsms {}\n'
    commandline_email = 'echo "Power failure alarm in the lab!" | mail -s LabAlert {}\n'
    for user in exp.persons.all():
        if user.mobile is not None:
            complete_command += commandline_sms.format(user.mobile.replace(' ', '').replace('/', ''))
        if user.email:
            complete_command += commandline_email.format(user.email)

    return HttpResponse(complete_command)


def clear(request, experiment):
    exp = get_object_or_404(Experiment, name=experiment)

    complete_command = ''
    commandline_sms = 'echo "Power returned in the lab!" | gnokii --sendsms {}\n'
    commandline_email = 'echo "Power returned in the lab!" | mail -s LabAlert {}\n'
    for user in exp.persons.all():
        if user.mobile is not None:
            complete_command += commandline_sms.format(user.mobile.replace(' ', '').replace('/', ''))
        if user.email:
            complete_command += commandline_email.format(user.email)

    return HttpResponse(complete_command)
