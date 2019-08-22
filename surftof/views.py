from django.db.models import FloatField
from django.http import JsonResponse
from surftof.models import IsegAssignments, PotentialSettings


def export_iseg_profile(request, pk):
    channel_voltages = {
        'm1': {
            'ch00': 0,
            'ch01': 0,
            'ch02': 0,
            'ch03': 0,
            'ch04': 0,
            'ch05': 0,
            'ch06': 0,
            'ch07': 0
        },
        'm2': {
            'ch00': 0,
            'ch01': 0,
            'ch02': 0,
            'ch03': 0,
            'ch04': 0,
            'ch05': 0,
            'ch06': 0,
            'ch07': 0,
            'ch08': 0,
            'ch09': 0,
            'ch10': 0,
            'ch11': 0
        },
        'm3': {
            'ch00': 0,
            'ch01': 0,
            'ch02': 0,
            'ch03': 0,
            'ch04': 0,
            'ch05': 0,
            'ch06': 0,
            'ch07': 0,
            'ch08': 0,
            'ch09': 0,
            'ch10': 0,
            'ch11': 0
        }
    }

    potential_setting = PotentialSettings.objects.get(pk=int(pk))
    iseq_assignment = IsegAssignments.objects.first()

    for key, value in iseq_assignment.__dict__.items():
        if "_ch" in key and len(value) > 0:
            for field in PotentialSettings._meta.get_fields():
                if type(field) == FloatField and field.verbose_name.lower() == value.lower() and type(
                        getattr(potential_setting, field.name)) == float:
                    channel_voltages[key[:2]][key[3:]] = getattr(potential_setting, field.name)
    return JsonResponse(channel_voltages, safe=False)
