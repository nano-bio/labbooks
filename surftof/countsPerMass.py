from glob import glob
from os import makedirs, remove
from os.path import exists, dirname, realpath
from random import randint
from shutil import rmtree, make_archive
from threading import Thread
import h5py
import numpy as np
from django.conf import settings
from django.shortcuts import get_object_or_404
from matplotlib.figure import Figure
from scipy.optimize import curve_fit
from surftof.models import Measurement


class CountsPerMassCreator:

    def __init__(self, form_data):
        # DESTINATION FOLDER
        if exists(settings.SURFTOF_EXPORT_CPM_DIR):
            rmtree(settings.SURFTOF_EXPORT_CPM_DIR)  # delete old files
        self.destination_folder = f"{settings.SURFTOF_EXPORT_CPM_DIR}tmp-{randint(1000000000, 10000000000)}/"
        makedirs(self.destination_folder)

        # MEASUREMENT IDS
        self.measurement_id_list_str = form_data['id_list']
        self.measurement_ids = []
        for a in self.measurement_id_list_str.split(','):
            if '-' in a:
                rang = range(int(a.split('-')[0].strip()), int(a.split('-')[1].strip()) + 1)
                self.measurement_ids += rang
            elif a:
                self.measurement_ids.append(int(a.strip()))
        self.measurement_ids = list(dict.fromkeys(self.measurement_ids))
        self.measurement_ids.sort()

        # CURRENT NORM
        self.current_normalization = form_data['current_normalization']
        if self.current_normalization == 'value':
            self.current_normalization_value = form_data['current_normalization_value']
        else:
            self.current_normalization_value = None

        # MASSES
        self.masses = []
        mass = 1
        while True:
            try:
                if (
                        type(form_data[f'mass_{mass}_mass_nominal']) == float and
                        type(form_data[f'mass_{mass}_mass_min']) == float and
                        type(form_data[f'mass_{mass}_mass_max']) == float and
                        type(form_data[f'mass_{mass}_zero_min']) == float and
                        type(form_data[f'mass_{mass}_zero_max']) == float
                ):
                    self.masses.append({
                        'mass_nominal': form_data[f'mass_{mass}_mass_nominal'],
                        'mass_min': form_data[f'mass_{mass}_mass_min'],
                        'mass_max': form_data[f'mass_{mass}_mass_max'],
                        'zero_min': form_data[f'mass_{mass}_zero_min'],
                        'zero_max': form_data[f'mass_{mass}_zero_max']
                    })
                else:
                    break
            except KeyError:
                break
            mass += 1

    def run(self, save_plots=True):
        threads = list()
        for measurement_id in self.measurement_ids:
            x = Thread(target=counts_per_mass_worker, args=(
                self.destination_folder,
                measurement_id,
                self.masses,
                self.current_normalization,
                self.current_normalization_value,
                save_plots
            ))
            threads.append(x)
            x.start()
        for thread in threads:
            thread.join()

    def create_zip(self):
        csv_lines = []
        for file in glob(f"{self.destination_folder}CPM*.csv"):
            with open(file, "r") as f:
                csv_lines.append(f.readline())
            remove(file)

        with open(f"{self.destination_folder}cpm-ids-{self.measurement_id_list_str}.csv", "w") as f:
            f.write("MeasurementId,ImpactEnergy")
            for mass in self.masses:
                f.write(f",{mass['mass_nominal']},{mass['mass_nominal']}err")
            f.write('\n')
            for csv_line in csv_lines:
                f.write(csv_line)
                f.write('\n')

        file_name = f"{settings.SURFTOF_EXPORT_CPM_DIR}cpm"
        make_archive(file_name, 'zip', self.destination_folder)
        return file_name + ".zip"


def counts_per_mass_worker(
        destination_folder,
        measurement_id,
        masses,
        current_normalization,
        current_normalization_value,
        save_plots):
    h5_file_name = glob(f"{settings.SURFTOF_BIGSHARE_DATA_ROOT}{measurement_id}/*.h5")[0]
    x_data_raw, y_data_raw, file_duration, sweeps = import_mass_spectrum(h5_file_name)

    # get surface current
    if current_normalization == 'value':
        surface_current = current_normalization_value
    elif current_normalization == 'fixed':
        surface_current = 1e-9
    elif current_normalization == 'file':
        surface_current = import_pico_log_and_median(h5_file_name)
    else:
        surface_current = 1

    with open(f"{destination_folder}CPM-ID-{measurement_id}.csv", "w") as f:
        f.write(
            f"{measurement_id},{get_object_or_404(Measurement, pk=measurement_id).get_impact_energy_surface_value()}")
        for mass in masses:
            y_data = y_data_raw.copy()
            x_data = x_data_raw.copy()

            # subtract zero level
            zero_level = calc_zero_level(x_data, y_data, mass['zero_min'], mass['zero_max'])
            y_data = y_data - zero_level

            x_data, y_data = slice_data(x_data, y_data, mass['mass_min'], mass['mass_max'])
            sum_cps = sum(y_data)
            cps = sum_cps * file_duration / sweeps / surface_current
            cps_error = np.sqrt(sum_cps * file_duration) / sweeps / surface_current
            f.write(f",{cps},{cps_error}")

            if save_plots:
                fig = Figure()
                ax = fig.subplots()
                ax.plot(x_data, y_data)
                ax.plot([min(x_data), max(x_data)], [0, 0])
                fig.savefig(f"{destination_folder}ZeroPlot-ID-{measurement_id}-Mass-{mass['mass_nominal']}.png")


def import_mass_spectrum(filename):
    def quadratic_fit_function(x, a, t0):
        return a * (x + t0) ** 2

    with h5py.File(filename, 'r')as f:
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

        # from h5 file get file duration for error calculation on counts
        file_duration = int(
            dict(f.attrs.items())['Single Spec Duration (ms)'][0] / 1000 * len(f['SPECdata']['Intensities']))
        sweeps = file_duration * 1e9 / dict(f.attrs.items())['Pulsing Period (ns)'][0]
    return x_data, y_data, file_duration, sweeps


def calc_zero_level(x_data, y_data, x_min, x_max):
    _, y_data = slice_data(x_data, y_data, x_min, x_max)
    y_data = sorted(y_data)

    # remove some of the highest and lowest values
    remove_percent = 1
    y_data = y_data[
             int(len(y_data) / 100 * remove_percent):
             int(len(y_data) / 100 * (100 - remove_percent))]

    # create mean of the residual data
    zero_level = np.mean(y_data)
    return zero_level


def slice_data(x_data, y_data, x_min, x_max):
    # returns part of the x and y data as a function of
    # x min and x max
    # x min and x max is included

    position_mass_min = None
    position_mass_max = None
    for i in range(len(x_data)):
        if not position_mass_min and x_data[i] > x_min:
            print(55, i)
            position_mass_min = i - 1
        if not position_mass_max and x_data[i] > x_max:
            print(66, i)
            position_mass_max = i + 1

    x_data = x_data[position_mass_min:position_mass_max]
    y_data = y_data[position_mass_min:position_mass_max]

    return x_data, y_data


def import_pico_log_and_median(file_name):
    try:
        dir_path = dirname(realpath(file_name))
        try:
            pico_file_name = glob(dir_path + "/*Pico*")[0]
        except IndexError:
            pico_file_name = glob(dir_path + "/*eV-*")[0]
        except Exception as e:
            print(e)
            raise
        a = []
        b = 0
        with open(pico_file_name) as f:
            for line in f:
                try:
                    a.append(float(line.split(' , ')[1]))
                except (IndexError, ValueError, FloatingPointError):
                    b += 1
        if b > 0:
            print(f"{b} corrupted lines skipped!")
        return np.mean(a)
    except Exception as e:
        print(e)
        raise e
