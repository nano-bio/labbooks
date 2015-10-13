from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context, Template
from django.core.files import File
from django.core import serializers

import os
import re
import base64
import models
from django.db import models as djangomodels

import datetime, time
from django.utils.timezone import utc

from models import CurrentSetting, Measurement, Turbopump, TurbopumpStatus, JournalEntry

def retrieve_plotable_parameters():
    #show all fields that are numbers and can be plotted
    m = models.Measurement._meta.fields
    fieldlist = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist.append(parameter.name)

    return fieldlist

def readable_time_ago(datetimeobject):
    #calculate the duration in minutes and return string <minutes>m
    #datetime1 should be the older one
    td = datetime.datetime.utcnow().replace(tzinfo = utc) - datetimeobject
    minutes = int(round(abs(td).total_seconds() / 60, 0))
    if minutes > 60:
        message = 'about ' + str(int(round(minutes / 60, 0))) + ' h ago'
    else:
        message = str(minutes) + ' m ago'
    return message

def readsettings(request):
    #this is only allowed from ClusTOF    
    if request.META.get('HTTP_X_REAL_IP') != settings.CLUSTOFIP:
        return HttpResponseForbidden()

    #we always just edit the first entry
    cs_instance = CurrentSetting.objects.get(id__exact = 1)

    #we only want those values
    values_to_read = ['time', 
                      'tof_settings_file', 
                      'data_filename', 
                      'scantype', 
                      'pressure_cs', 
                      'pressure_pu1', 
                      'pressure_pu2', 
                      'pressure_ion', 
                      'pressure_tof',
                      'temperature_he',
                      'electron_energy_set',
                      'ion_block',
                      'pusher',
                      'wehnelt',
                      'extraction_1',
                      'extraction_2',
                      'deflector_1',
                      'deflector_2',
                      'filament_current',
                      'trap_current',
                      'oven_temperature',
                      'polarity'
                     ]

    #lets see what we got in the request
    for field in request.GET:
        if field in values_to_read:
            #this is a field we want. update it
            cs_instance.__dict__[field] = request.GET[field]
            #also set a timestamp so we know when we last updated it
            cs_instance.__dict__[field + '_time'] = datetime.datetime.utcnow().replace(tzinfo = utc)

    #validate dat shit:
    try:
        cs_instance.clean_fields()
    except ValidationError as errors:
        #somebody gave us a weird value
        #empty error message
        message = ''
        for error in errors.message_dict:
            message += 'failure:' + error + ';'

        return HttpResponse(message)

    #data seems to be fine
    cs_instance.save()

    return HttpResponse('success')


#define a class for a form to enter new measurements
class MeasurementForm(forms.ModelForm):
    #we need to overwrite the __init__ because we want to access the instance object
    def __init__(self, *args, **kwargs):
        super(MeasurementForm, self).__init__(*args, **kwargs)
        #run through all values of our start-instance ...
        for field in self.instance.__dict__:
            #... that are time fields ...
            if '_time' in field:
                #... and take them over in our new form instance
                self.__dict__[field] = self.instance.__dict__[field]

    #in this function we create a timelabel for each field
    #stating how long it has been since its last update
    def update_labels(self):
        for field in self.fields:
            #none time-fields only
            if '_time' not in field:
                #not all fields have a time field (hence the try/except)
                try:
                    self.fields[field].timelabel = readable_time_ago(self.__dict__[field + '_time'])
                except KeyError:
                    pass
    class Meta:
        model = Measurement
        fields = '__all__'

@login_required
def newmeasurement(request):
    #form was already submitted
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            new_measurement = form.save()
            return HttpResponseRedirect('/admin/clustof/measurement/' + str(new_measurement.id))

    #form was not submitted, create a form
    else:
        #latest instance for measurement
        try:
            m = Measurement.objects.latest()
        except:
            return HttpResponse('Bad Error. No latest measurement is available. Create one in the admin interface.')

        #retrieve the values from the machine
        try:
            prefill_values = CurrentSetting.objects.get(id = 1)
        except:
            return HttpResponse('No current settings measurement found. Create one in the admin interface.')

        #overwrite all values available therefore leaving a mix of machine-values and latest-values
        for field in prefill_values.__dict__:
            m.__dict__[field] = prefill_values.__dict__[field]

        #now...
        m.time = datetime.datetime.utcnow().replace(tzinfo = utc)

        #now create a new form for a Measurement
        form = MeasurementForm(instance = m)
        form.update_labels()

    return render(request, 'clustof/newmeasurement.html', {'form': form})

def plot_parameters(request, parameter1 = 'extraction_1', parameter2 = 'extraction_2'):
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

    t = get_template('clustof/plot_parameters.html')
    c = Context({'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist})

    html = t.render(c)

    return HttpResponse(html)

def exportfile(request, id):
    m = get_object_or_404(Measurement, id = id)
    return HttpResponseRedirect('http://' + settings.CLUSTOFIP + '/' + m.data_filename.replace('D:\\Data\\', ''))

#def exportfilesize(request, id):
#    m = get_object_or_404(Measurement, id = id)
#    fs = os.stat('/clustof/' + m.data_filename.replace('D:\\Data\\', '')).st_size
#    return HttpResponse(fs)

def exportfilename(request, id):
    m = get_object_or_404(Measurement, id = id)
    fs = m.data_filename.replace('D:\\Data\\', '')
    return HttpResponse(fs)

def mjson(request, count = 20):
    # takes the last count measurements and exports to JSON
    data = serializers.serialize("json", Measurement.objects.order_by('-time').all()[:count])
    return HttpResponse(data)

def mcsv(request, count = 20, offset = 0):
    # takes the last count measurements and exports to CSV
    response = HttpResponse(content_type='text/csv')
    #response = HttpResponse()

    m = Measurement.objects.order_by('-time').all()[offset:count]
    
    t = get_template('clustof/mcsv.csv')
    c = Context({'m': m})

    response.write(t.render(c))
    return response

def pump(request, pumpnumber):
    pump = get_object_or_404(Turbopump, id = pumpnumber)
    datasets = TurbopumpStatus.objects.filter(pump = pump.id).all()
    values = []
    for dataset in datasets:
        # time 1000 because flot wants milliseconds
        timestamp = time.mktime(dataset.date.timetuple())*1000
        values.append('[' + str(timestamp)  + ', ' + str(dataset.current) + ']')

    values = ', '.join(values)

    t = get_template('clustof/pump.html')
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
        form = TechJournalForm(request.POST, request.FILES)
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        ImageData = request.POST.get('written_notes')
        ImageData = dataUrlPattern.match(ImageData).group(2)

        # If none or len 0, means illegal image data
        if (ImageData == None) or len(ImageData) == 0:
            # PRINT ERROR MESSAGE HERE
            raise ValidationError('Image not OK!')

        tmp_filename_written_notes = '/tmp/output.png'
        output = open(tmp_filename_written_notes, 'wb')
        output.write(ImageData.decode('base64'))
        output.close()

        if form.is_valid():
            new_journal_entry = form.save()
            new_journal_entry.written_notes.save(new_journal_entry.generate_filename(), File(open(tmp_filename_written_notes)))
            return HttpResponseRedirect('/clustof/journal/' + str(new_journal_entry.id))

    #form was not submitted, create a form
    else:
        #now create a new form for a Measurement
        form = TechJournalForm()

    return render(request, 'clustof/newjournalentry.html', {'form': form})

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
    t = get_template('clustof/showjournalentry.html')
    c = Context({'m' : m})
    html = t.render(c)
    return HttpResponse(html)
