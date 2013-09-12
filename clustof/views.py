from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django import forms
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import Context, Template

import models
from django.db import models as djangomodels

import datetime
from django.utils.timezone import utc

from models import CurrentSetting, Measurement

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
    if request.META.get('REMOTE_ADDR') != '138.232.72.1':
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
                      'electron_energy',
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

#@login_required
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
    return HttpResponseRedirect('/clustof/export/files/' + m.data_filename.replace('D:\\Data\\', ''))
