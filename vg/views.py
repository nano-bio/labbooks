from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404

import models

import sys, os

sys.path.append('/var/opt')

#MPLCONFIGDIR = '/var/opt/labbooks/.matplotlib/'
os.environ['HOME'] = '/var/opt/labbooks/'
import fitlib

def showmeasurement(request, id):
    """ Generic display page for all measurements """
    #fetch from db
    m = models.Measurement.objects.get(id = id)

    #fetch file with fitlib
    data = fitlib.fitlib.readfile(settings.MEDIA_ROOT + m.datafile.name)

    #data needs to be in the right format for flot library to plot
    m.data = []

    for datapoint in data:
        m.data.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    m.data = ' ,'.join(m.data)

    #ready to render
    t = get_template('showmeasurement.html')
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

    t = get_template('export.txt')
    c = Context({'m' : m})
    html = t.render(c)

    #make it download
    resp = HttpResponse(html, content_type='text/plain')
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name
    return resp

def calibratedata(measurement, calibration, formatstring = '[%s, %s]'):
    #fetch file with fitlib
    data = fitlib.fitlib.readfile(settings.MEDIA_ROOT + measurement.datafile.name)

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
    t = get_template('showcalmeasurement.html')
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

    t = get_template('exportcalibrated.txt')
    c = Context({'m' : m})
    html = t.render(c)

    #make it download
    resp = HttpResponse(html, content_type='text/plain')
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name
    return resp

