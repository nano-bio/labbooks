from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render
import wippi.models as models
from django.db import models as djangomodels
import sys
import os

sys.path.append('/var/opt')

MPLCONFIGDIR = '/var/opt/labbooks/.matplotlib/'
os.environ['HOME'] = '/var/opt/labbooks/'
import fitlib


def retrieve_plotable_parameters():
    # show all fields that are numbers and can be plotted
    m = models.Measurement._meta.fields
    fieldlist = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(
                parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist.append(parameter.name)

    return fieldlist


def list_plotable_parameters(request):
    fieldlist = retrieve_plotable_parameters()

    t = get_template('wippi/plotable_parameters_list.html')
    c = Context({'fieldlist': fieldlist})
    html = t.render(c)
    return HttpResponse(html)


def plot_parameters(request, parameter1='lens_1a', parameter2='lens_1b'):
    # first we check whether the parameters are allowed
    m = models.Measurement._meta.fields
    fieldlist_allowed = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(
                parameter, djangomodels.fields.PositiveIntegerField):
            fieldlist_allowed.append(parameter.name)

    # if either is not allowed we send back an error 400 (bad request)
    if parameter1 not in fieldlist_allowed or parameter2 not in fieldlist_allowed:
        return HttpResponseBadRequest('Parameters not allowed!')

    # browse through all measurements
    measurements = models.Measurement.objects.all()

    # create list of values
    values = []
    for m in measurements:
        values.append('[' + str(getattr(m, parameter1)) + ', ' + str(getattr(m, parameter2)) + ']')

    # double points don't have any use
    valuepairs = set(values)
    # we need a string anyway
    values = ', '.join(valuepairs)

    # get all the possible parameters
    fieldlist = retrieve_plotable_parameters()

    t = 'wippi/plot_parameters.html'
    c = {'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist}

    return HttpResponse(render(request, t, c))


def showmeasurement(request, id):
    """ Generic display page for all measurements """
    # fetch from db
    m = models.Measurement.objects.get(id=id)

    # fetch file with fitlib
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + m.datafile.name, tolerate_spaces=True)

    # data needs to be in the right format for flot library to plot
    m.data = []

    for datapoint in data:
        m.data.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    m.data = ' ,'.join(m.data)

    # get next and last scan for convenient switching
    try:
        m.nextid = models.Measurement.objects.filter(time__gt=m.time).order_by('time')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.nextid = m.id

    try:
        m.lastid = models.Measurement.objects.filter(time__lt=m.time).order_by('-time')[0:1].get().id
    except models.Measurement.DoesNotExist:
        m.lastid = m.id

    # ready to render
    t = 'wippi/showmeasurement.html'
    c = {'m': m}
    return HttpResponse(render(request, t, c))


def exportmeasurement(request, id):
    """Export file as it was uploaded, but add measurement id in the first line"""
    m = models.Measurement.objects.get(id=id)
    # read file contents
    contents = ''
    f = open(settings.MEDIA_ROOT + m.datafile.name)
    for line in f:
        contents += line

    # assign the read lines to the context for the template
    m.filecontents = contents

    t = 'wippi/export.txt'
    c = {'m': m}

    html = render(request, t, c)
    # make it download
    resp = HttpResponse(html, content_type='text/plain')
    # we need to encode the filename in ascii. replace weird characters with closest approx.
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name.encode('ascii', 'replace')
    return resp


def format_for_plot(data):
    # data needs to be in the right format for flot library to plot
    tempdata = []

    for datapoint in data:
        tempdata.append('[%s, %s]' % (str(datapoint[0]), str(datapoint[1])))

    tempdata = ' ,'.join(tempdata)

    return tempdata


def calibrate(measurement, calibration):
    # takes a measurement object and a calibration object and calibrates the data
    tempdata = fitlib.helplib.readfile(settings.MEDIA_ROOT + measurement.datafile.name, tolerate_spaces=True)

    for datapoint in tempdata:
        datapoint[0] = datapoint[0] - calibration.p0

    return tempdata


def showcalibratedmeasurement(request, m_id, c_id):
    """calibrates a measurement (m_id) with a calibration (c_id) and shows it"""
    # fetch from db
    m = models.Measurement.objects.get(id=m_id)
    c = models.Calibration.objects.get(id=c_id)

    # calibrate
    m.data = calibrate(m, c)
    m.data = format_for_plot(m.data)

    # ready to render
    t = 'wippi/showcalmeasurement.html'
    c = {'m': m, 'c': c}
    return HttpResponse(render(request, t, c))


def home(request):
    return render(request, 'wippi/home.html', {})


def exportcalibratedmeasurement(request, m_id, c_id):
    """calibrates a measurement (m_id) with a calibration (c_id) and exports it"""
    # fetch from db
    m = models.Measurement.objects.get(id=m_id)
    c = models.Calibration.objects.get(id=c_id)

    # calibrate
    m.data = calibrate(m, c)
    tempdata = []

    # two tab-separated columns
    for datapoint in m.data:
        tempdata.append('%s\t%s' % (str(datapoint[0]), str(datapoint[1])))

    # assign the read lines to the context for the template
    m.filecontents = '\r\n'.join(tempdata)

    t = 'wippi/exportcalibrated.txt'
    c = {'m': m, 'c': c}

    # make it download
    resp = HttpResponse(render(request, t, c), content_type='text/plain')
    # we need to encode the filename in ascii. replace weird characters with closest approx.
    resp['Content-Disposition'] = 'attachment; filename=%s' % m.datafile.name.encode('ascii', 'replace')
    return resp


def fit_data(data, n_peaks):
    # guess where the peaks could be -> offset is a 50th of the length to avoid
    # artefacts in the beginning of the file
    guesses = fitlib.fitlib.guess_ES_peaks(data, n_peaks, data[:, 0].max() / 50)

    # fit
    fitted_peaks, parameters = fitlib.fitlib.fitES(data, guesses)

    # create a new array of datapoints for plotting
    fitfunc = fitlib.fitlib.gaussfunctions(n_peaks)
    fitteddata = fitlib.fitlib.data_from_fit_and_parameters(data, fitfunc, parameters)

    return fitteddata, parameters


def fitmeasurement(request, m_id, n_peaks):
    """fits a measurement (m_id) with n_peaks peaks and shows it"""
    # fetch from db
    m = models.Measurement.objects.get(id=m_id)

    # we want an integer
    n_peaks = int(n_peaks)

    # fetch file with fitlib
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + m.datafile.name, tolerate_spaces=True)

    fitteddata, parameters = fit_data(data, n_peaks)

    m.peaks = []
    # feed the template with peak information
    for i in range(0, n_peaks):
        m.peaks.append([parameters[i * 3], parameters[i * 3 + 1], parameters[i * 3 + 2]])

    # data needs to be in the right format for flot library to plot
    m.data = format_for_plot(data)

    # data needs to be in the right format for flot library to plot
    m.fitteddata = format_for_plot(fitteddata)

    # ready to render
    t = 'wippi/fitmeasurement.html'
    c = {'m': m}
    return HttpResponse(render(request, t, c))


def fitcalmeasurement(request, m_id, c_id, n_peaks):
    """fits a measurement (m_id) with n_peaks peaks and shows it"""
    # fetch from db
    m = models.Measurement.objects.get(id=m_id)
    c = models.Calibration.objects.get(id=c_id)

    # calibrate
    data = calibrate(m, c)

    # we want an integer
    n_peaks = int(n_peaks)

    fitteddata, parameters = fit_data(data, n_peaks)

    m.peaks = []
    # feed the template with peak information
    for i in range(0, n_peaks):
        m.peaks.append([parameters[i * 3], parameters[i * 3 + 1], parameters[i * 3 + 2]])

    # data needs to be in the right format for flot library to plot
    m.data = format_for_plot(data)

    # data needs to be in the right format for flot library to plot
    m.fitteddata = format_for_plot(fitteddata)

    # ready to render
    t = 'wippi/fitcalmeasurement.html'
    c = {'m': m, 'c': c}
    return HttpResponse(render(request, t, c))
