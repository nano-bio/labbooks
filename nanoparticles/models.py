import pickle
import threading
from base64 import b64encode
from io import BytesIO
from time import sleep

import numpy
from NSFopen.read import read as afmreader
from django.db import models
from django.utils.timezone import now
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from journal.models import BasicJournalEntry


class JournalEntry(BasicJournalEntry):
    pass


class Operator(models.Model):
    name = models.CharField(max_length=50)


class Substrate(models.Model):
    name = models.CharField(
        max_length=500)
    width = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Width (mm)")
    height = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Height (mm)")
    thickness = models.FloatField(
        blank=True,
        null=True,
        verbose_name="Thickness (mm)")

    def __str__(self):
        if self.width and self.height and self.thickness:
            return f"{self.name} ({self.width:.1f}mm x {self.height}mm x {self.thickness}mm)"
        return self.name


class Coating(models.Model):
    name = models.CharField(
        max_length=500)
    comment = models.TextField(
        blank=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    DEVICES = (
        ('AFM', 'AFM'),
        ('STM', 'STM'),
    )
    RATING = (
        (5, '5 - Science'),
        (4, '4 - Interesting'),
        (3, '3 - Normal'),
        (2, '2 - Not interesting'),
        (1, '1 - Trash')
    )
    SPUTTER_METHODS = (
        ('magnetronTi', 'Magnetron Titan'),
        ('magnetronAu', 'Magnetron Gold'),
        ('snowball', 'Snowball'),
        ('toffy', 'Toffy'),
    )

    # General
    time = models.DateTimeField(
        default=now)
    device = models.CharField(
        max_length=10,
        choices=DEVICES)
    rating = models.IntegerField(
        choices=RATING,
        default=3)

    substrate = models.ForeignKey(
        Substrate,
        on_delete=models.PROTECT)
    tip = models.CharField(
        blank=True,
        max_length=500)
    coating = models.ForeignKey(
        Coating,
        on_delete=models.PROTECT)
    thickness = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Thickness  (nm)")
    sputter_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Sputter Time (min)")
    sputter_method = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=SPUTTER_METHODS,
        default='magnetronTi'
    )
    comment = models.TextField(
        blank=True)

    nid_file = models.FileField(
        blank=True,
        upload_to='nanoparticles')
    spectroscopy = models.BooleanField(
        default=False)
    conductivity = models.BooleanField(
        default=False)
    xps = models.BooleanField(
        default=False)
    image_size = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Image Size in µm"
    )

    def save(self, *args, **kwargs):
        super(Measurement, self).save(*args, **kwargs)
        create_or_update_images(self.id)

    def __str__(self):
        return f"{self.device}: {self.coating} on {self.substrate}"


class MeasurementData(models.Model):
    measurement = models.OneToOneField(
        Measurement,
        on_delete=models.CASCADE)

    forward_phase_data = models.BinaryField()
    forward_amplitude_data = models.BinaryField()
    forward_z_axis_data = models.BinaryField()
    backward_phase_data = models.BinaryField()
    backward_amplitude_data = models.BinaryField()
    backward_z_axis_data = models.BinaryField()

    forward_phase_image = models.ImageField(upload_to='nanoparticles')
    forward_amplitude_image = models.ImageField(upload_to='nanoparticles')
    forward_z_axis_image = models.ImageField(upload_to='nanoparticles')
    backward_phase_image = models.ImageField(upload_to='nanoparticles')
    backward_amplitude_image = models.ImageField(upload_to='nanoparticles')
    backward_z_axis_image = models.ImageField(upload_to='nanoparticles')


def create_or_update_images(measurement_id):
    for thread in threading.enumerate():
        if thread.name == f'thread_image_{measurement_id}':
            return

    x = threading.Thread(target=extract_data_from_nid_file, args=(measurement_id,))
    x.name = f'thread_image_{measurement_id}'
    x.start()


def get_data_from_measurement_data_object(measurement_id, measurement_type):
    """
    @param measurement_id: int
    @param measurement_type: str, one of forward_phase, _amplitude, _z_axis, backward_phase, ...
    """
    md = MeasurementData.objects. \
        filter(measurement_id=measurement_id). \
        values(measurement_type + '_data')
    if len(md) != 1:
        raise Exception(f'{len(md)} matches found for ID {measurement_id}, type {measurement_type}')
    return md[0][measurement_type + '_data']


def extract_data_from_nid_file(measurement_id):
    sleep(5)  # make sure that DB save was finished

    def get_data(direction, m_type):
        print(f"Image importer: ID{measurement_id}, DIR{direction}, TYP{m_type}")
        a = numpy.array(
            f.data['Image'][direction][m_type],
            dtype=numpy.float)
        return a

    def create_image(image_data):
        image = BytesIO()
        fig = Figure(figsize=(1, 1), dpi=len(image_data))

        ax = fig.add_subplot()
        ax.set_axis_off()
        fig.subplots_adjust(
            top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        ax.imshow(image_data, aspect='equal', cmap='hot')
        FigureCanvasAgg(fig).print_png(image)
        return image

    m = Measurement.objects.get(id=measurement_id)

    try:
        md = MeasurementData.objects.get(measurement=m)
    except MeasurementData.DoesNotExist:
        md = MeasurementData(measurement=m)

    f = afmreader(m.nid_file.path, verbose=False)

    data = {}
    for k in [
        ['forward_amplitude', ('Forward', 'Amplitude')],
        ['forward_phase', ('Forward', 'Phase')],
        ['forward_z_axis', ('Forward', 'Z-Axis')],
        ['backward_amplitude', ('Backward', 'Amplitude')],
        ['backward_phase', ('Backward', 'Phase')],
        ['backward_z_axis', ('Backward', 'Z-Axis')],
    ]:
        data[k[0]] = get_data(*k[1])
        md.__setattr__(k[0] + '_data', b64encode(pickle.dumps(data[k[0]])))

    md.forward_phase_image.save(
        f'forward-phase-{measurement_id}.png', create_image(data['forward_phase']))
    md.forward_amplitude_image.save(
        f'forward-amplitude-{measurement_id}.png', create_image(data['forward_amplitude']))
    md.forward_z_axis_image.save(
        f'forward-z_axis-{measurement_id}.png', create_image(data['forward_z_axis']))
    md.backward_phase_image.save(
        f'backward-phase-{measurement_id}.png', create_image(data['backward_phase']))
    md.backward_amplitude_image.save(
        f'backward-amplitude-{measurement_id}.png', create_image(data['backward_amplitude']))
    md.backward_z_axis_image.save(
        f'backward-z_axis-{measurement_id}.png', create_image(data['backward_z_axis']))

    md.save()
    print("Finished import of NanoParticles Image")
