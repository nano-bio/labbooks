import itertools
from datetime import datetime, timedelta
from glob import glob
from json import dumps
import numpy as np
import h5py
from django.db.models import FloatField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from surftof.models import IsegAssignments, PotentialSettings, Measurement, MassCalibration
from django.core import serializers

root = "/mnt/bigshare/Experiments/SurfTOF/Measurements/rawDATA/"

def export_iseg_profile(request, pk):
    channel_voltages = {
        '00': 0,
        '01': 0,
        '02': 0,
        '03': 0,
        '04': 0,
        '05': 0,
        '06': 0,
        '07': 0,

        '10': 0,
        '11': 0,
        '12': 0,
        '13': 0,
        '14': 0,
        '15': 0,
        '16': 0,
        '17': 0,
        '18': 0,
        '19': 0,
        '110': 0,
        '111': 0,

        '20': 0,
        '21': 0,
        '22': 0,
        '23': 0,
        '24': 0,
        '25': 0,
        '26': 0,
        '27': 0,
        '28': 0,
        '29': 0,
        '210': 0,
        '211': 0
    }

    potential_setting = PotentialSettings.objects.get(pk=int(pk))
    iseq_assignment = IsegAssignments.objects.first()

    for key, value in iseq_assignment.__dict__.items():
        if "_ch" in key and len(value) > 0:
            for field in PotentialSettings._meta.get_fields():
                if type(field) == FloatField and field.verbose_name.lower() == value.lower() and type(
                        getattr(potential_setting, field.name)) == float:
                    channel_voltages["{}{}".format(int(key[1:2]) - 1, int(key[5:]))] = getattr(potential_setting,
                                                                                               field.name)

    response = HttpResponse(dumps(channel_voltages), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=iseg-voltages.txt'
    return response


def measurement_json_export(request, pk):
    obj = get_object_or_404(Measurement, pk=pk)
    serialized_obj = serializers.serialize('json', [obj, ])
    return HttpResponse(serialized_obj, content_type='application/json')


def potential_settings_json_export(request, pk):
    obj = get_object_or_404(PotentialSettings, pk=pk)
    serialized_obj = serializers.serialize('json', [obj, ])
    return HttpResponse(serialized_obj, content_type='application/json')


def preview_data(request, time_bin_or_mass, calibration_id, data_id_file_1, data_id_file_2, scale_data_file_2,
                 diff_plot, binned_by, max_time_bin):
    max_time_bin = int(max_time_bin)
    binned_by = int(binned_by)

    # x-axis
    if time_bin_or_mass == 'mass':
        mass_data = calibrate_mass_axis(calibration_id, binned_by, max_time_bin)
        xlabel = "m/z"
    else:
        mass_data = range(binned_by - 1, max_time_bin, binned_by)
        xlabel = "time bins"

    # get y-axis data from h5 file
    file = glob("{}{}/*h5".format(root, int(data_id_file_1)))[-1]
    with h5py.File(file, 'r')as f:
        y_data1 = np.array(f['SPECdata']['AverageSpec'])
        y_data1 = reduce_data_by_mean(y_data1, binned_by, 1)
    if data_id_file_2 != 'null':
        file = glob("{}{}/*h5".format(root, int(data_id_file_2)))[-1]
        with h5py.File(file, 'r')as f:
            y_data2 = np.array(f['SPECdata']['AverageSpec'])
            y_data2 = reduce_data_by_mean(y_data2, binned_by, float(scale_data_file_2))

    # create json string from y-axis data
    response = '{"data":['
    for i in range(min([len(y_data1), len(mass_data)])):
        if data_id_file_2 == 'null':
            response += "[{},{:.2e}],".format(mass_data[i], y_data1[i])
        elif diff_plot == 'true':
            response += "[{},{:.2e}],".format(mass_data[i], y_data1[i] - y_data2[i])
        else:
            response += "[{},{:.2e},{:.2e}],".format(mass_data[i], y_data1[i], y_data2[i])
    response = response[:-1]  # remove last ','

    # append labels to json string
    if data_id_file_2 == 'null':
        labels = '["time bin","cps ID {}"]'.format(data_id_file_1)
    elif diff_plot == 'true':
        labels = '["time bin","cps ID {} - cps ID {}"]'.format(data_id_file_1, data_id_file_2)
    else:
        labels = '["time bin","cps ID {}","cps ID {}"]'.format(data_id_file_1, data_id_file_2)

    response += '],"xlabel":"{}","labels":{}}}'.format(xlabel, labels)

    return HttpResponse(response, content_type='application/json')


def import_pressure(id):
    pressures = {}
    try:
        pressure_file = glob(root + str(id) + "/*ressure*")[0]
        a = np.loadtxt(pressure_file, delimiter='\t',
                       dtype=[('a', '|S8'), ('b', '<f4'), ('c', '<f4'),
                              ('d', '<f4'), ('e', '<f4'), ('f', '<f4'),
                              ('g', '<f4')], skiprows=1)
        ionsource = []
        surf = []
        tof = []
        for b in a:
            ionsource.append(b[1])
            surf.append(b[2])
            tof.append(b[3])
        pressures['is'] = np.median(ionsource)
        pressures['surf'] = np.median(surf)
        pressures['tof'] = np.median(tof)
    except:
        pressures['is'] = -1
        pressures['surf'] = -1
        pressures['tof'] = -1
    return pressures


def get_file_info_for_preview(request, measurement_id):
    response = []
    measurement = get_object_or_404(Measurement, pk=int(measurement_id))
    pressures = import_pressure(measurement_id)
    response.append({'key': 'ID', 'value': measurement.id})
    response.append({'key': 'Impact Energy', 'value': measurement.get_impact_energy_surface()})
    response.append({'key': 'Temperature', 'value': get_temp_from_file(measurement_id)})
    response.append({'key': 'Projectile', 'value': "{}".format(measurement.projectile)})
    response.append({'key': 'Gas Surf', 'value': "{}".format(measurement.gas_surf.__str__())})
    response.append({'key': 'Pressure IS', 'value': "{:.1e} mbar".format(pressures['is'])})
    response.append({'key': 'Pressure Surf', 'value': "{:.1e} mbar".format(pressures['surf'])})
    response.append({'key': 'Pressure Tof', 'value': "{:.1e} mbar".format(pressures['tof'])})
    return JsonResponse(response, safe=False)


def get_temp_from_file(measurement_id):
    try:
        h5_file_name = glob("{}{}/*h5".format(root, int(measurement_id)))[-1]
        with h5py.File(h5_file_name, 'r') as f:
            file_start = datetime.strptime(dict(f.attrs.items())['FileCreatedTimeSTR_LOCAL'][0].decode(),
                                           "%d/%m/%Y %Hh %Mm %Ss")
            file_duration = int(
                dict(f.attrs.items())['Single Spec Duration (ms)'][0] / 1000 * len(f['SPECdata']['Intensities']))
            file_end = file_start + timedelta(seconds=file_duration)
            filenames = ["{}_temperaturePT100.csv".format(file_start.strftime("%Y-%m-%d"))]
            if file_end.date() != file_start.date():
                filenames.append("{}_temperaturePT100.csv".format(file_end.strftime("%Y-%m-%d")))

            temps = []
            for filename in filenames:
                with open(root + 'temperature/' + filename, 'r') as g:
                    for line in g:
                        line_time = datetime.strptime(line.strip().split(',')[0][:19], '%Y-%m-%dT%H:%M:%S')
                        if file_start < line_time < file_end:
                            temps.append(float(line.strip().split(',')[1]))
            return "{:.1f} &#176;C".format(np.median(temps))
    except:
        return "-1 &#176;C"


# for preview_data
def reduce_data_by_mean(data, binning, scale):
    mean_value = 0
    reduced_date = []
    for i, v in enumerate(data):
        mean_value += v
        if i % binning == binning - 1:
            reduced_date.append(mean_value / binning * scale)
            mean_value = 0
    return reduced_date


# for preview_data
def calibrate_mass_axis(calibration_id, binned_by, max_time_bin):
    mass_data = []
    if calibration_id == 'null':
        calibration = MassCalibration.objects.last()
    else:
        calibration = MassCalibration.objects.get(pk=int(calibration_id))
    for i in range(binned_by - 1, max_time_bin, binned_by):
        mass_data.append(calibration.a * (i + calibration.to) ** 2)
    return mass_data


# for preview data
def preview_file_list(request):
    # get all measurements from DB
    objects = Measurement.objects.order_by('-time')

    response = []
    for key, group in itertools.groupby(objects, key=lambda x: x.time.date()):
        tmp = {'date': key, 'times': []}
        for val in group:
            tmp['times'].append({
                'time': val.time.strftime('%H:%M'),
                'id': val.id,
                'name': "ID {}, {} eV, {} C<br> {} on {} with {}".format(val.id, val.impact_energy_surface,
                                                                         val.surface_temperature, val.projectile,
                                                                         val.surface_material, val.gas_surf)
            })
        response.append(tmp)
    response = []
    for obj in objects:
        response.append({
            'id': obj.id,
            'name': "ID {}, {}, {} C<br> {} on {} with {}".format(obj.id, obj.get_impact_energy_surface(),
                                                                  obj.surface_temperature, obj.projectile,
                                                                  obj.surface_material, obj.gas_surf)
        })
    return JsonResponse(response, safe=False)


# for preview data
def calibration_list(reqest):
    calibrations = MassCalibration.objects.all()
    response = []
    for c in calibrations:
        response.append({'id': c.id, 'name': c.__str__()})
    return JsonResponse(response, safe=False)


# update the rating of a measurement
def set_rating_of_measurement(request, id, rating):
    if request.user.has_perm('surftof.add_measurement'):
        obj = get_object_or_404(Measurement, pk=id)
        obj.rating = int(rating)
        obj.save()
        return redirect('/admin/surftof/measurement/')
