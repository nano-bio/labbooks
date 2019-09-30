from django.db.models import FloatField
from django.http import JsonResponse
from surftof.models import IsegAssignments, PotentialSettings


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
    return JsonResponse(channel_voltages, safe=False)
