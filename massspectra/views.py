import numpy as np
from django.http import HttpResponse


# for mass_spectra_data
def reduce_data_by_mean(data, binning, scale=1):
    mean_value = 0
    reduced_date = []
    for i, v in enumerate(data):
        mean_value += v
        if i % binning == binning - 1:
            reduced_date.append(mean_value / binning * scale)
            mean_value = 0
    return reduced_date


def bin_array(arr, binning):
    return arr[:int(arr.shape[0] / binning) * binning].reshape(-1, binning).mean(axis=1)


def slice_data(x_data, y_data, x_min, x_max):
    # returns part of the x and y data as a function of
    # x min and x max
    def find_index_of_nearest(array, value):
        array = np.asarray(array)
        return (np.abs(array - value)).argmin()

    x_min_index = find_index_of_nearest(x_data, x_min)
    x_max_index = find_index_of_nearest(x_data, x_max)

    x_data = x_data[x_min_index:x_max_index]
    y_data = y_data[x_min_index:x_max_index]

    return x_data, y_data


def mass_spectra_data(request, x_data1, y_data1, x_data2=None, y_data2=None):
    # data_id_file_1 = request.POST.get('dataIdFile1')
    data_id_file_2 = request.POST.get('dataIdFile2', None)
    scale_data_file_2 = float(request.POST.get('scaleDataFile2', 1))
    diff_plot = request.POST.get('diffPlot', False)
    binned_by = int(request.POST.get('binnedBy', 1))
    max_mass = int(request.POST.get('maxMass'))

    if x_data1[-1] > max_mass:
        x_data1, y_data1 = slice_data(x_data1, y_data1, 0, max_mass)
    x_data1 = bin_array(x_data1, binned_by)
    y_data1 = bin_array(y_data1, binned_by)
    if data_id_file_2:
        if x_data2[-1] > max_mass:
            x_data2, y_data2 = slice_data(x_data2, y_data2, 0, max_mass)
        x_data2 = bin_array(x_data2, binned_by)
        y_data2 = bin_array(y_data2, binned_by)
        if scale_data_file_2 != 1:
            y_data2 *= scale_data_file_2

        if not np.array_equal(x_data1, x_data2):
            # interpolate_thing() TODO
            masses = x_data1
        else:
            masses = x_data1
    else:
        masses = x_data1

    # create json string from xy-data
    if not data_id_file_2:
        data_str = ",".join([f"[{masses[i]:.3f},{y_data1[i]:.2e}]" for i in range(len(masses))])
    elif diff_plot == 'true':
        data_str = ",".join([f"[{masses[i]:.3f},{(y_data1[i] - y_data2[i]):.2e}]" for i in range(len(masses))])
    else:
        data_str = ",".join([f"[{masses[i]:.3f},{y_data1[i]:.2e},{y_data2[i]:.2e}]" for i in range(len(masses))])
    return HttpResponse("{" + f'"data":[{data_str}]' + "}", content_type="application/json")
