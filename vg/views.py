from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
import vg.models as models
from django.db import models as djangomodels
import time
from django.db.models import Q
import sys, os, re
from chemlib import checkatoms

sys.path.append('/var/opt')

MPLCONFIGDIR = '/var/opt/labbooks/.matplotlib/'
os.environ['HOME'] = '/var/opt/labbooks/'
import fitlib
from fitlib.chemlib import ChemicalObject

atomregex = re.compile('\b(([A-Z]+[a-z]?\d{0,3})+)+\b')


def get_chemical_formula(chemical_formula):
    """ checks chemical formalae for plausibility """

    # first we check if the formula seems like a chemical formula
    m = atomregex.findall(chemical_formula)
    if m is not None:
        for form in m:
            if checkatoms(form[0]):
                return form[0]

    return u''


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

    t = 'vg/plotable_parameters_list.html'
    c = {'fieldlist': fieldlist}
    return HttpResponse(render(request, t, c))


def plot_parameters(request, parameter1='ion_repeller', parameter2='focus_coarse_1'):
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

    t = 'vg/plot_parameters.html'
    c = {'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist}

    return HttpResponse(render(request, t, c))


def showmeasurement(request, id):
    """ Generic display page for all measurements """
    # fetch from db
    m = models.Measurement.objects.get(id=id)

    # fetch file with fitlib
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + m.datafile.name)

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
    t = 'vg/showmeasurement.html'
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

    t = 'vg/export.txt'
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
    tempdata = fitlib.helplib.readfile(settings.MEDIA_ROOT + measurement.datafile.name)

    # calibrate
    if calibration.p2 == '':
        for datapoint in tempdata:
            datapoint[0] = calibration.p0 + calibration.p1 * datapoint[0]
    elif calibration.p2 != '':
        for datapoint in tempdata:
            datapoint[0] = calibration.p0 + calibration.p1 * datapoint[0] + calibration.p2 * datapoint[0] ** 2

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
    t = 'vg/showcalmeasurement.html'
    c = {'m': m, 'c': c}
    return HttpResponse(render(request, t, c))


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

    t = 'vg/exportcalibrated.txt'
    c = {'m': m, 'c': c}
    html = render(request, t, c)

    # make it download
    resp = HttpResponse(html, content_type='text/plain')
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
    data = fitlib.helplib.readfile(settings.MEDIA_ROOT + m.datafile.name)

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
    t = 'vg/fitmeasurement.html'
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
    t = 'vg/fitcalmeasurement.html'
    c = {'m': m, 'c': c}
    return HttpResponse(render(request, t, c))


def export_all_f_urls(request):
    # this is mainly used for benchmarking peak finding algorithms and other weird shit josi thinks about
    # it returns a list of ids of F-/SF6 scans

    output = models.Measurement.objects.filter(
        Q(scantype__exact='ES'),
        Q(description__exact='F') | Q(description__exact='F / SF6 neg for cal') | Q(
            description__exact='F neg for cal') | Q(description__exact='F- for Calibration') | Q(
            description__exact='F for calibration'),
        Q(substance__contains='SF6')
    ).all()

    text = 'wget 138.232.74.60/vg/export/' + '\r\nwget 138.232.74.60/vg/export/'.join([str(m.id) for m in output])

    return HttpResponse(text)


def all_usable_es(request):
    substancelist = []
    fragmentlist = []

    output = models.Measurement.objects.exclude(fragment=u'').all()
    for m in output:
        success = False
        chemform = get_chemical_formula(m.substance)
        if chemform != u'':
            substancelist.append(chemform)
            fragmentlist.append(m.fragment)
        else:
            o = ChemicalObject(token='03ed8095-9ff1-42e5-8548-4e716da2622a', name=m.substance)
            o.complete()
            if o.chemicalformula != '':
                substancelist.append(o.chemicalformula)
                fragmentlist.append(m.fragment)

    text = ''
    i = 0
    for s in substancelist:
        text = text + s + ' ' + fragmentlist[i] + '<br />'
        i = i + 1

    return HttpResponse(text)


def export_all_sf6_urls(request):
    # this is mainly used for benchmarking peak finding algorithms and other weird shit josi thinks about
    # it returns a list of ids of SF6-/SF6 scans

    output = models.Measurement.objects.filter(
        Q(scantype__exact='ES'),
        Q(description__exact='SF6') | Q(description__exact='SF6 neg for cal') | Q(
            description__exact='SF6 for Calibration') | Q(description__exact='SF6 for calibration'),
        Q(substance__contains='SF6')
    ).all()

    text = 'wget 138.232.74.60/vg/export/' + '\r\nwget 138.232.74.60/vg/export/'.join([str(m.id) for m in output])

    return HttpResponse(text)


def export_all_sf5_urls(request):
    # this is mainly used for benchmarking peak finding algorithms and other weird shit josi thinks about
    # it returns a list of ids of SF6-/SF6 scans

    output = models.Measurement.objects.filter(
        Q(scantype__exact='ES'),
        Q(description__exact='SF5') | Q(description__exact='SF5 neg for cal') | Q(
            description__exact='SF5 for Calibration') | Q(description__exact='SF5 for calibration'),
        Q(substance__contains='SF6')
    ).all()

    text = 'wget 138.232.74.60/vg/export/' + '\r\nwget 138.232.74.60/vg/export/'.join([str(m.id) for m in output])

    return HttpResponse(text)


def export_all_f2_urls(request):
    # this is mainly used for benchmarking peak finding algorithms and other weird shit josi thinks about
    # it returns a list of ids of SF6-/SF6 scans

    output = models.Measurement.objects.filter(
        Q(scantype__exact='ES'),
        Q(description__exact='F2') | Q(description__exact='F2 neg for cal') | Q(
            description__exact='F2 for Calibration') | Q(description__exact='F2 for calibration'),
        Q(substance__contains='SF6')
    ).all()

    text = 'wget 138.232.74.60/vg/export/' + '\r\nwget 138.232.74.60/vg/export/'.join([str(m.id) for m in output])

    return HttpResponse(text)


def pump(request, pumpnumber):
    pump = get_object_or_404(models.Turbopump, id=pumpnumber)
    datasets = models.TurbopumpStatus.objects.filter(pump=pump.id).all()
    values = []
    for dataset in datasets:
        # time 1000 because flot wants milliseconds
        timestamp = time.mktime(dataset.date.timetuple()) * 1000
        values.append('[' + str(timestamp) + ', ' + str(dataset.current) + ']')

    values = ', '.join(values)

    t = 'vg/pump.html'
    c = {'values': values, 'pump': pump}

    return HttpResponse(render(request, t, c))
