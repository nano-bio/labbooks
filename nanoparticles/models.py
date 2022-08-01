import numpy
from NSFopen.read import read as afmreader
from django.conf import settings
from django.db import models
from django.utils.timezone import now
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
        ('magnetronTi', 'Magnetron'),
        ('magnetronAu', 'Magnetron Gold'),
        ('snowball', 'Snowball'),
        ('toffy', 'Toffy'),
        ('hollowCathode', 'Hollow Cathode'),
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
        if self.nid_file:
            create_or_update_images(self.id, self.nid_file.path)

    def __str__(self):
        return f"{self.device}: {self.coating} on {self.substrate}"


def create_or_update_images(measurement_id, file_name):
    f = afmreader(file_name, verbose=False)

    for direction in ['Forward', 'Backward']:
        for measurement_type in ['Amplitude', 'Phase', 'Z-Axis']:
            a = numpy.array(
                f.data['Image'][direction][measurement_type],
                dtype=float)

            fig = Figure(figsize=(1, 1))

            ax = fig.add_subplot()
            ax.set_axis_off()
            fig.subplots_adjust(
                top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            ax.imshow(a, aspect='equal', cmap='hot')
            fig.savefig(
                f"{settings.MEDIA_ROOT}nanoparticles/{measurement_id}-{direction}-{measurement_type}.png", dpi=len(a))
