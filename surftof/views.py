from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context, Template
from django.core.files import File
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import json
import os
import re
import base64
import models
import hashlib
from django.db import models as djangomodels

import datetime, time
from django.utils.timezone import utc

from models import Measurement, Turbopump, TurbopumpStatus, JournalEntry

def retrieve_plotable_parameters():
    #show all fields that are numbers and can be plotted
    m = models.Measurement._meta.fields
    fieldlist = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist.append(parameter.name)

    return fieldlist

def plot_parameters(request, parameter1 = 'u_surf', parameter2 = 'u_is'):
    #first we check whether the parameters are allowed
    m = models.Measurement._meta.fields
    fieldlist_allowed = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist_allowed.append(parameter.name)

    #if either is not allowed we send back an error 400 (bad request)
    if parameter1 not in fieldlist_allowed or parameter2 not in fieldlist_allowed:
        return HttpResponseBadRequest('Parameters not allowed!')

    #browse through all measurements
    measurements = models.Measurement.objects.all()

    #create list of values
    values = []
    for m in measurements:
        values.append('[' + str(getattr(m, parameter1)) + ', ' + str(getattr(m, parameter2)) + ']')

    #double points don't have any use
    valuepairs = set(values)
    #we need a string anyway
    values = ', '.join(valuepairs)

    #get all the possible parameters
    fieldlist = retrieve_plotable_parameters()

    t = get_template('surftof/plot_parameters.html')
    c = Context({'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist})

    html = t.render(c)

    return HttpResponse(html)

def exportfile(request, id):
    m = get_object_or_404(Measurement, id = id)
    return HttpResponseRedirect('http://' + settings.SURFTOFIP + '/' + m.data_filename.replace('D:\\Data\\', ''))

def exportfilename(request, id):
    m = get_object_or_404(Measurement, id = id)
    fs = m.data_filename.replace('D:\\Data\\', '')
    return HttpResponse(fs)

def mjson(request, count = 20):
    # takes the last count measurements and exports to JSON
    data = serializers.serialize("json", Measurement.objects.order_by('-time').all()[:count])
    return HttpResponse(data)

def pump(request, pumpnumber):
    pump = get_object_or_404(Turbopump, id = pumpnumber)
    datasets = TurbopumpStatus.objects.filter(pump = pump.id).all()
    values = []
    for dataset in datasets:
        # time 1000 because flot wants milliseconds
        timestamp = time.mktime(dataset.date.timetuple())*1000
        values.append('[' + str(timestamp)  + ', ' + str(dataset.current) + ']')

    values = ', '.join(values)

    t = get_template('surftof/pump.html')
    c = Context({'values': values, 'pump': pump})

    html = t.render(c)

    return HttpResponse(html)

#define a class for a form to enter new measurements
class TechJournalForm(forms.ModelForm):
    written_notes = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super(TechJournalForm, self).__init__(*args, **kwargs)

    class Meta:
        model = JournalEntry
        exclude = ('written_notes', )

@login_required
def newjournalentry(request):
    #form was already submitted
    if request.method == 'POST':
        emptyimage = False

        form = TechJournalForm(request.POST, request.FILES)
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        ImageData = request.POST.get('written_notes')
        ImageData = dataUrlPattern.match(ImageData).group(2)

        # If none or len 0, means illegal image data
        if (ImageData == None) or len(ImageData) == 0:
            # PRINT ERROR MESSAGE HERE
            raise ValidationError('Image not OK!')
        elif hashlib.md5(ImageData).hexdigest() == 'ce10d4fbd8e265922741742759b06f71':
            # this could a completely blank image... we don't save those...
            emptyimage = True

        if emptyimage is not True:
            tmp_filename_written_notes = '/tmp/output.png'
            output = open(tmp_filename_written_notes, 'wb')
            output.write(ImageData.decode('base64'))
            output.close()

        if form.is_valid():
            new_journal_entry = form.save()
            if emptyimage is not True:
                new_journal_entry.written_notes.save(new_journal_entry.generate_filename(), File(open(tmp_filename_written_notes)))
            return HttpResponseRedirect('/surftof/journal/' + str(new_journal_entry.id))

    #form was not submitted, create a form
    else:
        #now create a new form for a Measurement
        form = TechJournalForm()

    return render(request, 'surftof/newjournalentry.html', {'form': form})

#show journal entries
def showjournalentry(request, id):
    """ Generic display page for all measurements """
    #fetch from db
    m = models.JournalEntry.objects.get(id = id)

    #get next and last scan for convenient switching
    try:
        m.nextid = models.JournalEntry.objects.filter(time__gt = m.time).order_by('time')[0:1].get().id
    except models.JournalEntry.DoesNotExist:
        m.nextid = m.id
    
    try:
        m.lastid = models.JournalEntry.objects.filter(time__lt = m.time).order_by('-time')[0:1].get().id
    except models.JournalEntry.DoesNotExist:
        m.lastid = m.id

    #ready to render
    t = get_template('surftof/showjournalentry.html')
    c = Context({'m' : m})
    html = t.render(c)
    return HttpResponse(html)

@csrf_exempt
def readvacuumstatus(request):
    #this is only allowed from pressure IPs
    if request.META.get('HTTP_X_REAL_IP') not in settings.PRESSUREIPS:
        print(request.META.get('HTTP_X_REAL_IP'))
        return HttpResponseForbidden()

    # has to be a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest()
    else:
        # define pattern to look for in delivered data
        linepattern = r'([0-9]{9,10})\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?'
        lineregex = re.compile(linepattern)

        # get the data and split by line break
        rawinput = request.body
        if rawinput is not "":
            lines = rawinput.split("\r\n")

            # match each line and put to database
            i = 0
            for line in lines:
                values = lineregex.match(line)
                if values:
                    models.VacuumStatus.objects.create(time = values.group(1), g1 = values.group(2), g2 = values.group(3), g3 = values.group(4), g4 = values.group(5), g5 = values.group(6), g6 = values.group(7))
                    i = i + 1

            return HttpResponse('%s entries saved' % (i))
        else:
            return HttpResponseBadRequest()

def writevacuumstatus(request, after = None, before = None):
    # returns all vacuumstatus values before timestamp and after timestamp
    try:
        aftertimestamp = int(after)
    except (ValueError, TypeError) as e:
        now = datetime.datetime.now()
        after = now - datetime.timedelta(days=7)
        aftertimestamp = int(time.mktime(after.timetuple()))

    try:
        beforetimestamp = int(before)
    except (ValueError, TypeError) as e:
        beforetimestamp = int(time.time())

    datasets = models.VacuumStatus.objects.filter(time__lte=beforetimestamp).filter(time__gte=aftertimestamp).all()
    data = json.dumps([{'time': dataset.time, 'g1': dataset.g1, 'g2': dataset.g2, 'g3': dataset.g3, 'g4': dataset.g4, 'g5': dataset.g5, 'g6': dataset.g6} for dataset in datasets])
    return HttpResponse(data)

    
