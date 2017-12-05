from django.conf import settings
from django.http import HttpResponse
from django.template import Context, Template
from django.template.loader import get_template
from django.shortcuts import render_to_response, get_object_or_404
import models
import time

def showmeasurement(request, id):
    """ Generic display page for all measurements """
    #fetch from db
    m = models.Measurement.objects.get(id = id)

    #fetch file with fitlib
    data = Admin.PlotAdmin.readfile(settings.MEDIA_ROOT + m.datafile.name)

    #data needs to be in the right format for flot library to plot
    m.data = []

    for datapoint in data:
        m.data.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    m.data = ' ,'.join(m.data)

    #get next and last scan for convenient switching
    try:
        m.nextid = models.Measurement.objects.filter(time__gt = m.time).order_by('-starttime')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.nextid = m.id

    try:
        m.lastid = models.Measurement.objects.filter(time__lt = m.time).order_by('-starttime')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.lastid = m.id

    #ready to render
    t = 'snowball/showmeasurement.html'
    c = {'m' : m}
    return HttpResponse(render(request, t, c))

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

    t = 'snowball/export.txt'
    c = {'m' : m}

    #make it download
    resp = HttpResponse(render(request, t, c), content_type='text/plain')
    #we need to encode the filename in ascii. replace weird characters with closest approx.
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name.encode('ascii', 'replace')
    return resp

def format_for_plot(data):
    #data needs to be in the right format for flot library to plot
    tempdata = []

    for datapoint in data:
        tempdata.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    tempdata = ' ,'.join(tempdata)

    return tempdata

def home(request):
    return render_to_response('home.html')

def pump(request, pumpnumber):
    pump = get_object_or_404(models.Turbopump, id = pumpnumber)
    datasets = models.TurbopumpStatus.objects.filter(pump = pump.id).all()
    values = []
    for dataset in datasets:
        # time 1000 because flot wants milliseconds
        timestamp = time.mktime(dataset.date.timetuple())*1000
        values.append('[' + str(timestamp)  + ', ' + str(dataset.current) + ']')

    values = ', '.join(values)

    t = 'snowball/pump.html'
    c = {'values': values, 'pump': pump}

    return HttpResponse(render(request, t, c))
