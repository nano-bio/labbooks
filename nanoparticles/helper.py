import os
from io import BytesIO

# matplotlib.use('Agg')
from time import time

import numpy
from NSFopen.read import read as afmreader
# import matplotlib
from django.conf import settings
from django.http import Http404
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from nanoparticles.models import MeasurementData, Measurement


# from matplotlib import pyplot as plt


#
# from nanoparticles.models import Measurement
#
# # def open_nid_file(measurement_id):
# m = Measurement.objects.get(pk=1)
# f = afmreader(full_file_name, verbose=True)
# print(f.data)
#
# data = numpy.array(
#     f.data['Image']['Forward']['Amplitude'],
#     dtype=numpy.float)
# data.dump('data.p')

def make_image(data):
    start = time()
    fig = Figure(figsize=(1, 1), dpi=len(data))

    ax = fig.add_subplot()
    # ax.axis('off')
    # ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0,
                hspace = 0, wspace = 0)
    # plt.margins(0,0)
    # fig.add_axes(ax)
    # ax.set_cmap('hot')
    ax.imshow(data, aspect='equal',cmap='hot')
    print(55, time()-start)
    with BytesIO() as pseudo_file:
        FigureCanvasAgg(fig).print_png(pseudo_file)
        a = pseudo_file.getvalue()
    print(66, time()-start)
    return a

# data = numpy.load('data.p', allow_pickle=True)
# make_image(data, 'out.png')
#
# pyplot.imshow(data)
# # pyplot.savefig('OUTPUT_FILENAME.png')
# pyplot.axis('off')
# pyplot.savefig("test.png", bbox_inches=0)
# pyplot.show()


def get_data_from_measurement_data_object(measurement_id, measurement_type):
    try:
        start = time()
        md = MeasurementData.objects.get(measurement_id=measurement_id)
        print(222, time()-start)
    except MeasurementData.DoesNotExist:
        print(345)
        md = extract_data_from_nid_file(measurement_id=measurement_id)
    if measurement_type == "forward-phase":
        return md.forward_phase
    elif measurement_type == "forward-amplitude":
        return md.forward_amplitude
    elif measurement_type == "forward-z-axis":
        return md.forward_z_axis
    elif measurement_type == "backward-phase":
        return md.backward_phase
    elif measurement_type == "backward-amplitude":
        return md.backward_amplitude
    elif measurement_type == "backward-z-axis":
        return md.backward_z_axis
    else:
        raise Http404('wrong measurement type given!')


def extract_data_from_nid_file(measurement_id):
    def get_data(direction, m_type):
        return numpy.array(
            f.data['Image'][direction][m_type],
            dtype=numpy.float).tolist()

    m = Measurement.objects.get(id=measurement_id)

    try:
        md = MeasurementData.objects.get(measurement=m)
    except MeasurementData.DoesNotExist:
        md = MeasurementData(measurement=m)

    full_file_name = m.file_path.replace(
        'Z:\\',
        settings.NANOPARTICLES_DATA_ROOT
    ).replace(
        "\\",
        "/")
    print(os.path.abspath(full_file_name))
    f = afmreader(full_file_name, verbose=False)

    md.forward_phase = get_data('Forward', 'Phase')
    md.forward_amplitude = get_data('Forward', 'Amplitude')
    md.forward_z_axis = get_data('Forward', 'Z-Axis')
    md.backward_phase = get_data('Backward', 'Phase')
    md.backward_amplitude = get_data('Backward', 'Amplitude')
    md.backward_z_axis = get_data('Backward', 'Z-Axis')

    md.save()

    return md
