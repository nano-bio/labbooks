from pathlib import Path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from massspectra.views import get_mass_spectrum_from_csv, get_mass_spectrum_tofwerk, mass_spectra_data
from toffy2.models import Measurement


@require_POST
def get_mass_spectra_data(request):
    data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)
    try:
        x_data1, y_data1 = get_spectra_per_id(data_id_file_1)

        if data_id_file_2:
            x_data2, y_data2 = get_spectra_per_id(data_id_file_2)
            return mass_spectra_data(request, x_data1, y_data1, x_data2, y_data2)

        else:
            return mass_spectra_data(request, x_data1, y_data1)
    except Exception as e:
        return JsonResponse({'error': str(e)})


def get_spectra_per_id(measurement_id):
    id1_obj = Measurement.objects.get(pk=int(measurement_id))
    if id1_obj.data_file:
        return get_mass_spectrum_from_csv(id1_obj.data_file.path)
    else:
        unix_path = Path(
            id1_obj.data_file_path_h5
            .replace("\\", "/")
            .replace(settings.TOFFY2_REPLACE_H5_PATH[0], settings.TOFFY2_REPLACE_H5_PATH[1])
        )
        if not unix_path.exists():
            raise Exception("Measurement has no 'data file' and the given h5 file does not exist!")
        if not unix_path.is_file():
            raise Exception("Measurement has no 'data file' and the given h5 file path is no file!")
        return get_mass_spectrum_tofwerk(unix_path)
