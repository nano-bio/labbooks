from io import BytesIO

import matplotlib
from django.conf import settings
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.colors import Normalize

from nanoparticles.models import Measurement

matplotlib.use('Agg')
import numpy
from NSFopen.read import read as afmreader
# from django.conf import settings
from matplotlib import pyplot as plt


#
# from nanoparticles.models import Measurement
#
# # def open_nid_file(measurement_id):
# m = Measurement.objects.get(pk=1)
# full_file_name = m.file_path.replace('Z:\\', settings.NANOPARTICLES_DATA_ROOT).replace("\\", "/")
# f = afmreader(full_file_name, verbose=True)
# print(f.data)
#
# data = numpy.array(
#     f.data['Image']['Forward']['Amplitude'],
#     dtype=numpy.float)
# data.dump('data.p')

def make_image(data, outputname, size=(1,1), dpi=80):
    dpi = len(data)
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.set_cmap('hot')
    ax.imshow(data, aspect='equal')
    plt.savefig(outputname, dpi=dpi)


data = numpy.load('data.p', allow_pickle=True)
make_image(data, 'out.png')
#
# pyplot.imshow(data)
# # pyplot.savefig('OUTPUT_FILENAME.png')
# pyplot.axis('off')
# pyplot.savefig("test.png", bbox_inches=0)
# pyplot.show()

with BytesIO() as pseudo_file:
    FigureCanvasAgg(fig).print_png(pseudo_file)
    return pseudo_file.getvalue()
html = HttpResponse(content, content_type="image/png")


def get_image(measurement_id, measurement_type):
    m = Measurement.objects.get(pk=1)
    if m.data:
        data = numpy.array(
        m.data,
            dtype=numpy.float)
    else:
        full_file_name = m.file_path.replace('Z:\\', settings.NANOPARTICLES_DATA_ROOT).replace("\\", "/")
        f = afmreader(full_file_name, verbose=False)

    data = numpy.array(
        f.data['Image']['Forward']['Amplitude'],
        dtype=numpy.float)

    return 0