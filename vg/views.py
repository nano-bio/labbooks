from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404

import models
from django.db import models as djangomodels

import sys, os

sys.path.append('/var/opt')

#MPLCONFIGDIR = '/var/opt/labbooks/.matplotlib/'
os.environ['HOME'] = '/home/josi/labbooks/'
import fitlib

def retrieve_plotable_parameters():
    #show all fields that are numbers and can be plotted
    m = models.Measurement._meta.fields
    fieldlist = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist.append(parameter.name)

    return fieldlist

def list_plotable_parameters(request):
    fieldlist = retrieve_plotable_parameters()

    t = get_template('vg/plotable_parameters_list.html')
    c = Context({'fieldlist': fieldlist})
    html = t.render(c)
    return HttpResponse(html)

def plot_parameters(request, parameter1 = 'ion_repeller', parameter2 = 'focus_coarse_1'):
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

    t = get_template('vg/plot_parameters.html')
    c = Context({'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist})

    html = t.render(c)

    return HttpResponse(html)

def showmeasurement(request, id):
    """ Generic display page for all measurements """
    #fetch from db
    m = models.Measurement.objects.get(id = id)

    #fetch file with fitlib
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + m.datafile.name)

    #data needs to be in the right format for flot library to plot
    m.data = []

    for datapoint in data:
        m.data.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    m.data = ' ,'.join(m.data)
    
    #get next and last scan for convenient switching
    try:
        m.nextid = models.Measurement.objects.filter(time__gt = m.time).order_by('time')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.nextid = m.id
    
    try:
        m.lastid = models.Measurement.objects.filter(time__lt = m.time).order_by('-time')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.lastid = m.id

    #ready to render
    t = get_template('vg/showmeasurement.html')
    c = Context({'m' : m})
    html = t.render(c)
    return HttpResponse(html)

def exportmeasurement(request, id):
    """Export file as it was uploaded, but add measurement id in the first line"""
    m = models.Measurement.objects.get(id = id)
    #read file contents
    contents = ''
    f = open(settings.MEDIA_ROOT + m.datafile.name)
    for line in f:
        contents += line

    #assign the read lines to the context for the template
    m.filecontents = contents

    t = get_template('vg/export.txt')
    c = Context({'m' : m})
    html = t.render(c)

    #make it download
    resp = HttpResponse(html, content_type='text/plain')
    #we need to encode the filename in ascii. replace weird characters with closest approx.
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name.encode('ascii', 'replace')
    return resp

def calibratedata(measurement, calibration, formatstring = '[%s, %s]'):
    #fetch file with fitlib
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + measurement.datafile.name)

    #data needs to be in the right format for flot library to plot
    tempdata = []

    for datapoint in data:
        if calibration.p2 == '':
            tempdata.append(formatstring % (str(calibration.p0 + calibration.p1*datapoint[0]), str(datapoint[1])))
        elif calibration.p2 != '':
            tempdata.append(formatstring % (str(calibration.p0 + calibration.p1*datapoint[0] + calibration.p2*datapoint[0]**2), str(datapoint[1])))

    return tempdata

def showcalibratedmeasurement(request, m_id, c_id):
    """calibrates a measurement (m_id) with a calibration (c_id) and shows it"""
    #fetch from db
    m = models.Measurement.objects.get(id = m_id)
    c = models.Calibration.objects.get(id = c_id)

    #calibrate
    m.data = calibratedata(m, c)
    m.data = ' ,'.join(m.data)

    #ready to render
    t = get_template('vg/showcalmeasurement.html')
    c = Context({'m' : m, 'c' : c})
    html = t.render(c)
    return HttpResponse(html)

def home(request):
    return render_to_response('home.html')

def exportcalibratedmeasurement(request, m_id, c_id):
    """calibrates a measurement (m_id) with a calibration (c_id) and exports it"""
    #fetch from db
    m = models.Measurement.objects.get(id = m_id)
    c = models.Calibration.objects.get(id = c_id)

    #calibrate
    m.data = calibratedata(m, c, '%s\t%s')

    #assign the read lines to the context for the template
    m.filecontents = '\r\n'.join(m.data)

    t = get_template('vg/exportcalibrated.txt')
    c = Context({'m' : m, 'c' : c})
    html = t.render(c)

    #make it download
    resp = HttpResponse(html, content_type='text/plain')
    #we need to encode the filename in ascii. replace weird characters with closest approx.
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name.encode('ascii', 'replace')
    return resp

