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


def get_data_from_measurement_data_object(measurement_id, measurement_type):
    try:
        start = time()
        md = MeasurementData.objects.get(measurement_id=measurement_id)
        print(222, time() - start)
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



def new_mage(request):
    xvalues, yvalues = [1, 2, 3], [4, 6, 5]
    figure = io.BytesIO()
    plt.plot(xvalues, yvalues)
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    m = TestM()
    m.image.save('name_of_image.png', content_file)
    m.save()

# new_mage()
def extract_data_from_nid_file(measurement_id):
    def get_data(direction, m_type):
        a= numpy.array(
            f.data['Image'][direction][m_type],
            dtype=numpy.float).tolist()
        return a

    def create_image(data):

        image = BytesIO()
        fig = Figure(figsize=(1, 1), dpi=len(data))

        ax = fig.add_subplot()
        # ax.axis('off')
        # ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0,
                            hspace=0, wspace=0)
        # plt.margins(0,0)
        # fig.add_axes(ax)
        # ax.set_cmap('hot')
        ax.imshow(data, aspect='equal', cmap='hot')
        FigureCanvasAgg(fig).print_png(image)
        return image

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
    f = afmreader(full_file_name, verbose=False)

    forward_phase_data = get_data('Forward', 'Phase')
    forward_amplitude_data = get_data('Forward', 'Amplitude')
    forward_z_axis_data = get_data('Forward', 'Z-Axis')
    backward_phase_data = get_data('Backward', 'Phase')
    backward_amplitude_data = get_data('Backward', 'Amplitude')
    backward_z_axis_data = get_data('Backward', 'Z-Axis')

    md.forward_phase_data = forward_phase_data
    md.forward_amplitude_data = forward_amplitude_data
    md.forward_z_axis_data = forward_z_axis_data
    md.backward_phase_data = backward_phase_data
    md.backward_amplitude_data = backward_amplitude_data
    md.backward_z_axis_data = backward_z_axis_data

    md.forward_phase_image.save('forward-phase.png',create_image(forward_phase_data))
    md.forward_amplitude_image.save('forward-phase.png',create_image(forward_amplitude_data))
    md.forward_z_axis_image.save('forward-phase.png',create_image(forward_z_axis_data))
    md.backward_phase_image.save('forward-phase.png',create_image(backward_phase_data))
    md.backward_amplitude_image.save('forward-phase.png',create_image(backward_amplitude_data))
    md.backward_z_axis_image.save('forward-phase.png',create_image(backward_z_axis_data))

    md.save()
    return md
