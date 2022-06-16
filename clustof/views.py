import datetime
import json
import re
import time
from os.path import exists, getsize
from time import time

from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db import models as djangomodels
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, \
    Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import utc, now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

import clustof.models as models
from clustof.models import Measurement, Turbopump, TurbopumpStatus
from massspectra.views import mass_spectra_data, get_mass_spectrum_tofwerk, laser_scan, laser_scan_data


def retrieve_plotable_parameters():
    # show all fields that are numbers and can be plotted
    m = models.Measurement._meta.fields
    fieldlist = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter,
                                                                               djangomodels.fields.PositiveIntegerField):
            fieldlist.append(parameter.name)

    return fieldlist


def readable_time_ago(datetimeobject):
    # calculate the duration in minutes and return string <minutes>m
    # datetime1 should be the older one
    td = datetime.datetime.utcnow().replace(tzinfo=utc) - datetimeobject
    minutes = int(round(abs(td).total_seconds() / 60, 0))
    if minutes > 60:
        message = 'about ' + str(int(round(minutes / 60, 0))) + ' h ago'
    else:
        message = str(minutes) + ' m ago'
    return message


# define a class for a form to enter new measurements
class MeasurementForm(forms.ModelForm):
    # we need to overwrite the __init__ because we want to access the instance object
    def __init__(self, *args, **kwargs):
        super(MeasurementForm, self).__init__(*args, **kwargs)
        # run through all values of our start-instance ...
        for field in self.instance.__dict__:
            # ... that are time fields ...
            if '_time' in field:
                # ... and take them over in our new form instance
                self.__dict__[field] = self.instance.__dict__[field]

    # in this function we create a timelabel for each field
    # stating how long it has been since its last update
    def update_labels(self):
        for field in self.fields:
            # none time-fields only
            if '_time' not in field:
                # not all fields have a time field (hence the try/except)
                try:
                    self.fields[field].timelabel = readable_time_ago(self.__dict__[field + '_time'])
                except KeyError:
                    pass

    class Meta:
        model = Measurement
        fields = '__all__'


@login_required
def newmeasurement(request):
    # form was already submitted
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            new_measurement = form.save()
            return HttpResponseRedirect('/admin/clustof/measurement/' + str(new_measurement.id))

    # form was not submitted, create a form
    else:
        # latest instance for measurement
        try:
            m = Measurement.objects.latest()
        except:
            return HttpResponse('Bad Error. No latest measurement is available. Create one in the admin interface.')

        # now...
        m.time = datetime.datetime.utcnow().replace(tzinfo=utc)

        # now create a new form for a Measurement
        form = MeasurementForm(instance=m)
        form.update_labels()

    return render(request, 'clustof/newmeasurement.html', {'form': form})


def plot_parameters(request, parameter1='extraction_1', parameter2='extraction_2'):
    # first we check whether the parameters are allowed
    m = models.Measurement._meta.fields
    fieldlist_allowed = []
    for parameter in m:
        if isinstance(parameter, djangomodels.fields.FloatField) or isinstance(parameter,
                                                                               djangomodels.fields.PositiveIntegerField):
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

    t = 'clustof/plot_parameters.html'
    c = {'values': values, 'parameter1': parameter1, 'parameter2': parameter2, 'fieldlist': fieldlist}

    return HttpResponse(render(request, t, c))


def exportfile(request, id):
    m = get_object_or_404(Measurement, id=id)
    # this is a redirect to a URL handled by nginx
    return HttpResponseRedirect(
        '/clustof/export/files/' + m.data_filename.replace('D:\\Data\\', '').replace('G:\\Data\\', ''))


def export_file_size(request, pk):
    m = get_object_or_404(Measurement, pk=pk)
    file_name = m.data_filename.replace('D:\\Data\\', '').replace('G:\\Data\\', '')
    full_file_name = f"/var/storage/clustof/{file_name}"
    if exists(full_file_name):
        return JsonResponse({
            'file_name': file_name,
            'size': getsize(full_file_name)
        })
    else:
        return Http404(f'File not found: {full_file_name}')


# def exportfilesize(request, id):
#    m = get_object_or_404(Measurement, id = id)
#    fs = os.stat('/clustof/' + m.data_filename.replace('D:\\Data\\', '')).st_size
#    return HttpResponse(fs)

def exportfilename(request, id):
    m = get_object_or_404(Measurement, id=id)
    fs = m.data_filename.replace('D:\\Data\\', '')
    return HttpResponse(fs)


def mjson(request, count=20):
    # takes the last count measurements and exports to JSON
    data = serializers.serialize("json", Measurement.objects.order_by('-time').all()[:count])
    return HttpResponse(data)


def mcsv(request, count=20, offset=0):
    # takes the last count measurements and exports to CSV
    response = HttpResponse(content_type='text/csv')
    # response = HttpResponse()

    m = Measurement.objects.order_by('-time').all()[offset:count]

    t = 'clustof/mcsv.csv'
    c = {'m': m}

    response.write(render(request, t, c))
    return response


def pump(request, pumpnumber):
    pump = get_object_or_404(Turbopump, id=pumpnumber)
    datasets = TurbopumpStatus.objects.filter(pump=pump.id).all()
    values = []
    for dataset in datasets:
        # time 1000 because flot wants milliseconds
        timestamp = time.mktime(dataset.date.timetuple()) * 1000
        values.append('[' + str(timestamp) + ', ' + str(dataset.current) + ']')

    values = ', '.join(values)

    t = 'clustof/pump.html'
    c = {'values': values, 'pump': pump}

    return HttpResponse(render(request, t, c))


@csrf_exempt
def readvacuumstatus(request):
    # this is only allowed from pressure IPs
    if request.META.get('HTTP_X_REAL_IP') not in settings.PRESSUREIPS:
        print(request.META.get('HTTP_X_REAL_IP'))
        return HttpResponseForbidden()

    # has to be a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest()
    else:
        # define pattern to look for in delivered data
        linepattern = r'([0-9]{9,10})\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E-[0-9]{2})?\t([0-9]{1}\.[0-9]{3}E\+[0-2]{2})?'
        lineregex = re.compile(linepattern)

        # get the data and split by line break
        rawinput = request.body
        if rawinput != "":
            lines = rawinput.split("\r\n")

            # match each line and put to database
            i = 0
            for line in lines:
                values = lineregex.match(line)
                if values:
                    models.VacuumStatus.objects.create(time=values.group(1), g1=values.group(2), g2=values.group(3),
                                                       g3=values.group(4), g4=values.group(5), g5=values.group(6),
                                                       g6=values.group(7), temperature=values.group(8))
                    i = i + 1

            return HttpResponse('%s entries saved' % (i))
        else:
            return HttpResponseBadRequest()


def writevacuumstatus(request, after=None, before=None):
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
    data = json.dumps([{'time': dataset.time, 'g1': dataset.g1, 'g2': dataset.g2, 'g3': dataset.g3, 'g4': dataset.g4,
                        'g5': dataset.g5, 'g6': dataset.g6, 'temperature': dataset.temperature} for dataset in
                       datasets])
    return HttpResponse(data)


@csrf_exempt
def filetest(request):
    if request.method == 'POST' and request.FILES['logfile']:
        logfile = request.FILES['logfile']
        fs = FileSystemStorage()
        filename = fs.save(logfile.name, logfile)
        uploaded_file_url = fs.url(filename)
        return HttpResponse('File URL: ' + uploaded_file_url, content_type="text/plain")
    else:
        return HttpResponse('No file logfile')


# =========================================================
# The following two classes export our measurements older than 5 years publicly
# Mainly intended for B. R.
# =========================================================

class PublicMeasurementList(ListView):
    five_years_ago = now() - datetime.timedelta(365 * 5)
    queryset = models.Measurement.objects.filter(time__lt=five_years_ago).all()
    context_object_name = 'measurement_list'
    template_name = 'clustof/measurement_public.html'
    paginate_by = 100


class PublicMeasurementDetailView(DetailView):
    model = models.Measurement
    template_name = 'clustof/measurement_public_detail.html'
    context_object_name = 'm'


def exportfile_public(request, pk):
    m = get_object_or_404(Measurement, id=pk)
    return HttpResponseRedirect(
        '/public/GVzZacSHmhQdmTv/files/' + m.data_filename.replace('D:\\Data\\', '').replace('G:\\Data\\', ''))


# ------------
# Mass Spectra
# ------------
@require_POST
def get_mass_spectra_data(request):
    data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)

    try:
        x_data1, y_data1 = get_mass_spectrum(data_id_file_1)
    except MassSpectraException as e:
        return JsonResponse(status=404, data={'error': str(e)})

    if data_id_file_2:
        x_data2, y_data2 = get_mass_spectrum(data_id_file_2)
        return mass_spectra_data(request, x_data1, y_data1, x_data2, y_data2)

    else:
        return mass_spectra_data(request, x_data1, y_data1)


def get_measurement_file_name(measurement_id):
    m = Measurement.objects.get(pk=int(measurement_id))
    file_name = m.data_filename.replace('D:\\Data\\', '').replace('G:\\Data\\', '')
    return f"{settings.CLUSTOF_FILES_ROOT}{file_name}"


class MassSpectraException(Exception):
    pass


def get_mass_spectrum(measurement_id, mass_max=None):
    file_name_full = get_measurement_file_name(measurement_id)
    if not exists(file_name_full):
        raise MassSpectraException(f'File for this measurement not found on the server ({file_name_full})')
    return get_mass_spectrum_tofwerk(file_name_full, mass_max)


def laser_scan_data_clustof(request):
    measurement_id = int(request.POST.get('measurementId'))
    file_name_full = get_measurement_file_name(measurement_id)
    return laser_scan_data(request=request, file_name_full=file_name_full)


def laser_scan_clustof(request, measurement_id):
    file_name_full = get_measurement_file_name(measurement_id)
    return laser_scan(
        request=request,
        measurement_id=measurement_id,
        file_name_full=file_name_full,
        experiment='clustof',
        url=reverse('clustof-laser-scan-data'))
