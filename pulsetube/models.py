from django.db import models
from django.utils.timezone import now

SCAN_TYPE = (
    ('mass', 'Mass scan'),
    ('energy', 'Energy scan'),
    ('current', 'Current scan'),
    ('temperature', 'Temperature scan'),
)

POLARITY = (
    ('pos', 'positive'),
    ('neg', 'negative')
)


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}.".format(self.first_name, self.last_name[:1])


class Measurement(models.Model):
    # general
    operator = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='operator')
    operator_2 = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='operator_2')
    data_file = models.FileField(upload_to='pulsetube/dataFiles/', blank=True)
    date_time = models.DateTimeField(default=now)
    scan_type = models.CharField(max_length=20, choices=SCAN_TYPE, null=True, blank=True)

    # chamber pressures
    pressure_source = models.FloatField(null=True, blank=True)
    pressure_sector = models.FloatField(null=True, blank=True)

    # source settings
    he_temp = models.FloatField(verbose_name='He temperature')
    he_pres = models.FloatField(verbose_name='He stagnation pressure')

    # ion source settings
    ion_source_electron_energy = models.FloatField(verbose_name="Electron Energy [V]")
    ion_source_filament_current = models.FloatField(verbose_name="Filament Current [A]")
    ion_source_fc_current = models.FloatField(verbose_name="FC Current [uA]")

    # sector settings
    polarity = models.CharField(max_length=3, choices=POLARITY)
    channeltron_voltage = models.IntegerField(blank=True, null=True)
    voltage_start = models.IntegerField(blank=True, null=True)
    voltage_stop = models.IntegerField(blank=True, null=True)
    voltage_step_size = models.IntegerField(blank=True, null=True)
    time_per_step = models.FloatField(blank=True, null=True)
    number_of_runs = models.IntegerField(blank=True, null=True)

    # comment
    comment = models.TextField(max_length=1500, blank=True)

    def __str__(self):
        return "ID {}, {} by {}".format(
            self.id,
            self.date_time.strftime("%Y-%m-%d %H:%M"),
            self.operator)

    # this provides a link to the data file in the admin interface
    def get_data_file(self):
        return "<a href='%s' download>Data file</a>" % ('/files/' + str(self.data_file))

    get_data_file.allow_tags = True

    def get_comment(self):

        if len(self.comment) > 30:
            return "{} [...]".format(self.comment[:25])
        else:
            return self.comment

    get_comment.short_description = 'Comment'
