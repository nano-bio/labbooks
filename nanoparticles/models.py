from django.db import models
from django.utils.timezone import now


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

    file_path = models.CharField(
        blank=True,
        max_length=500,
        default="Z:\\Experiments\\NanoParticles\\",
        help_text="Full path of the .nid file")
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

    def __str__(self):
        return f"{self.device}: {self.coating} on {self.substrate}"
