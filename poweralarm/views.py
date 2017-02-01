from django.shortcuts import render, get_object_or_404
from models import Experiment
from django.http import HttpResponse

# Create your views here.

# creates alarm script for experiment
def alarm(request, experiment):
    exp = get_object_or_404(Experiment, name = experiment)

    completecommand = ''
    commandline = 'echo "Power failure alarm on experiment {}!" | gnokii --sendsms {}\n'
    for user in exp.persons.all():
        if user.mobile is not None:
            completecommand += commandline.format(exp.name, user.mobile.replace(' ', '').replace('/', ''))

    return HttpResponse(completecommand)

def clear(request, experiment):
    exp = get_object_or_404(Experiment, name = experiment)

    completecommand = ''
    commandline = 'echo "Power returned on experiment {}!" | gnokii --sendsms {}\n'
    for user in exp.persons.all():
        if user.mobile is not None:
            completecommand += commandline.format(exp.name, user.mobile.replace(' ', '').replace('/', ''))

    return HttpResponse(completecommand)

