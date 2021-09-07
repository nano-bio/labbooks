from datetime import datetime, timedelta
from glob import glob
from io import BytesIO

import h5py
import numpy as np
from django.conf import settings
from django.utils.timezone import make_aware
from scipy.optimize import curve_fit

from massspectra.views import slice_data
from surftof.models import Measurement, JournalEntry


def import_pressure(measurement_id):
    from django.conf import settings

    pressures = {}
    try:
        pressure_file = glob(settings.SURFTOF_BIGSHARE_DATA_ROOT + str(measurement_id) + "/*ressure*")[0]
        a = np.loadtxt(pressure_file, delimiter='\t',
                       dtype=[('a', '|S8'), ('b', '<f4'), ('c', '<f4'),
                              ('d', '<f4'), ('e', '<f4'), ('f', '<f4'),
                              ('g', '<f4')], skiprows=1)
        ion_source = []
        surf = []
        tof = []
        for b in a:
            ion_source.append(b[1])
            surf.append(b[2])
            tof.append(b[3])
        pressures['is'] = np.median(ion_source)
        pressures['surf'] = np.median(surf)
        pressures['tof'] = np.median(tof)
    except:
        pressures['is'] = -1
        pressures['surf'] = -1
        pressures['tof'] = -1
    return pressures


def get_temp_from_file(measurement_id, return_type="str"):
    from django.conf import settings

    try:
        h5_file_name = glob("{}{}/*h5".format(settings.SURFTOF_BIGSHARE_DATA_ROOT, int(measurement_id)))[-1]
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
                with open(settings.SURFTOF_BIGSHARE_DATA_ROOT + 'temperature/' + filename, 'r') as g:
                    for line in g:
                        line_time = datetime.strptime(line.strip().split(',')[0][:19], '%Y-%m-%dT%H:%M:%S')
                        if file_start < line_time < file_end:
                            temps.append(float(line.strip().split(',')[1]))
            if return_type == 'float':
                return np.median(temps)
            return_value = "{:.1f} &#176;C".format(np.median(temps))
            if "nan" in return_value:
                return "-1 &#176;C"
            return return_value
    except:
        return "-1 &#176;C"


def import_pico_log_and_median(measurement_id):
    from django.conf import settings

    try:
        current_file = glob(settings.SURFTOF_BIGSHARE_DATA_ROOT + str(measurement_id) + "/*Pico*")[0]
        a = []
        with open(current_file) as f:
            for line in f:
                try:
                    a.append(float(line.split(' , ')[1]))
                except (IndexError, ValueError, FloatingPointError):
                    pass
        return np.median(a)
    except:
        return -1


def get_measurements_and_journal_entries_per_month(date):
    end = (date + timedelta(days=35)).replace(day=1)

    start = make_aware(date)
    end = make_aware(end)

    measurement_objs = Measurement.objects. \
        filter(time__gte=start). \
        filter(time__lt=end). \
        order_by('-time')

    journal_objs = JournalEntry.objects. \
        filter(time__gte=start). \
        filter(time__lt=end). \
        order_by('-time')

    # sort all values by time
    measurements_journal_entries = []
    journal_objs = list(journal_objs)
    for measurement_obj in measurement_objs:
        while len(journal_objs) > 0 and measurement_obj.time < journal_objs[0].time:
            measurements_journal_entries.append({'t': 'journal', 'e': journal_objs.pop(0)})
        measurements_journal_entries.append({'t': 'measurement', 'e': measurement_obj})
    measurements_journal_entries += [{'t': 'journal', 'e': e} for e in journal_objs]
    return measurements_journal_entries


def get_mass_spectrum_preview_image(
        measurement_id,
        mass_max,
        use_log,
        pixel_height,
        pixel_width,
        show_x_axis):
    xs, ys = get_mass_spectrum(
        measurement_id=measurement_id,
        mass_max=mass_max)
    if len(xs) == len(ys) and len(xs) > 2:

        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure
        fig = Figure(figsize=(pixel_width / 100, pixel_height / 100))
        ax = fig.subplots()
        if use_log:
            ax.semilogy(xs, ys)
        else:
            ax.plot(xs, ys)

        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(show_x_axis)

        fig.subplots_adjust(left=0, right=1, bottom=int(show_x_axis) * 25 / pixel_height, top=1)

        with BytesIO() as pseudo_file:
            FigureCanvas(fig).print_png(pseudo_file)
            return pseudo_file.getvalue()


def get_mass_spectrum(measurement_id, mass_max=None):
    def quadratic_fit_function(x, a, t0):
        return a * (x + t0) ** 2

    with h5py.File(glob(f"{settings.SURFTOF_BIGSHARE_DATA_ROOT}{measurement_id}/*.h5")[0], 'r') as f:
        y_data = np.array(f['SPECdata']['AverageSpec'])
        x_data = np.array(f['CALdata']['Mapping'])
        masses = []
        times = []
        for row in x_data:
            if row[0] != 0 and row[1] != 0:
                masses.append(row[0])
                times.append(row[1])
        popt, pcov = curve_fit(quadratic_fit_function, times, masses, p0=(1e-8, 10000))
        x_data = quadratic_fit_function(np.array(np.arange(len(y_data))), *popt)

    if mass_max is None:
        return x_data, y_data
    return slice_data(x_data, y_data, 0, mass_max)
