import csv
import itertools
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from toffy2.models import Measurement


def preview_data(request, pk):
    obj = get_object_or_404(Measurement, id=int(pk))
    reader = csv.reader(open(obj.data_file.path, 'r'), delimiter="\t")
    xy_data = []
    for line in reader:
        xy_data.append([
            float(line[0]),
            int(float(line[1]))])
    return JsonResponse({'data': xy_data, 'id': obj.id, 'datetime': obj.time.strftime('%d.%m.%Y %H:%M')}, safe=False)


def preview_file_list(request):
    # get all measurements from DB
    objects = Measurement.objects.order_by('-time')

    response = []
    for key, group in itertools.groupby(objects, key=lambda x: x.time.date()):

        tmp = {'date': key, 'times': []}
        for val in group:
            if val.data_file:
                tmp['times'].append({
                    'time': val.time.strftime('%H:%M'),
                    'id': val.id,
                    'downloadUrl': "{}".format(val.data_file.url)})
        response.append(tmp)
    return JsonResponse(response, safe=False)


def preview_measurement_info(request, measurement_id):
    obj = get_object_or_404(Measurement, pk=measurement_id)
    data = {
        'measurementId': obj.id,
        'fields': {
            "Short Description": obj.short_description,
            "Comment": obj.comment,
            "Bronkhorst Sample Setpoint": obj.sample_gas_bronkhorst_setpoint,
            "Bronkhorst Vvaporation Setpoint": obj.evaporation_gas_bronkhorst_setpoint
        }
    }
    return JsonResponse(data, safe=False)
