from django.db import models
from django.utils.safestring import mark_safe

from journal.models import BasicJournalEntry


class Operator(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return u'%s %s' % (self.firstname, self.lastname)


class Measurement(models.Model):
    OVEN_TYPE_CHOICES = (
        ('organic', 'Organic'),
        ('metal', 'Metal'),
        ('external', 'External'),
        ('description', 'See description'),
    )
    time = models.DateTimeField()
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    short_description = models.CharField(max_length=500, blank=True)
    integration_start = models.IntegerField(blank=True, null=True, verbose_name="Integration start [s]")
    integration_stop = models.IntegerField(blank=True, null=True, verbose_name="Integration stop [s]")
    data_file = models.FileField(upload_to='toffy/dataFiles/', blank=True,
                                 help_text="Export massspecs and upload plain text files only.")
    tof_settings_file = models.FileField(upload_to='toffy/settingsFiles/', blank=True, verbose_name="TOF settings file")
    iseg_settings_file = models.FileField(upload_to='toffy/isegFiles/', blank=True)
    comment = models.TextField(max_length=5000, blank=True)

    he_pressure = models.FloatField(verbose_name="He pressure [bar]", default=20, blank=True, null=True)
    nozzle_temperature = models.FloatField(verbose_name="Nozzle temperature [K]", blank=True, null=True)
    quad_pressure = models.FloatField(verbose_name="Quad pressure [mbar]", default=0.000001, blank=True, null=True)

    ion_block_potential = models.FloatField(verbose_name="Ion block potential [V]", blank=True, null=True)
    ion_source_deflector_vertical = models.FloatField(verbose_name="Deflector vertical [V]", blank=True, null=True)
    ion_source_deflector_horizontal = models.FloatField(verbose_name="Deflector horizontal [V]", blank=True, null=True)
    electron_energy = models.FloatField(verbose_name="Electron energy [eV]", blank=True, null=True)
    electron_current = models.FloatField(verbose_name="Electron current [uA]", blank=True, null=True)

    bender_float_voltage = models.FloatField(verbose_name="Float voltage [V]", blank=True, null=True)
    bender_deflect_voltage = models.FloatField(verbose_name="Deflect voltage [V]", blank=True, null=True)

    deflector_float_z = models.FloatField(verbose_name="Float Z [V]", blank=True, null=True)
    deflector_u_z = models.FloatField(verbose_name="U Z [V]", blank=True, null=True)
    deflector_float_y = models.FloatField(verbose_name="Float Y [V]", blank=True, null=True)
    deflector_u_y = models.FloatField(verbose_name="U Y [V]", blank=True, null=True)
    deflector_front_aperture = models.FloatField(verbose_name="Front aperture [V]", blank=True, null=True)

    oven_type = models.CharField(verbose_name="Oven type", max_length=20, null=True, blank=True,
                                 choices=OVEN_TYPE_CHOICES)
    oven_voltage = models.FloatField(verbose_name="Voltage [V]", blank=True, null=True)
    oven_current = models.FloatField(verbose_name="Current [I]", blank=True, null=True)
    oven_power = models.FloatField(verbose_name="Power [W]", blank=True, null=True)
    oven_temperature = models.FloatField(verbose_name="Temperature [C]", blank=True, null=True)
    pickup_pressure = models.FloatField(verbose_name="Pickup pressure [mbar]", default=0.00001, blank=True, null=True)
    pickup_bronk = models.FloatField(verbose_name="Pickup bronki [a.U.]", default=99, blank=True, null=True)

    evaporation_gas = models.CharField(verbose_name="Gas", max_length=100, blank=True, default="Helium")
    evaporation_pressure = models.FloatField(verbose_name="Pressure [mbar]", default=0.0001, blank=True, null=True)
    evap_bronk = models.FloatField(verbose_name="Evap bronki [a.U.]", default=99, blank=True, null=True)

    collision_gas = models.CharField(verbose_name="Gas", max_length=100, blank=True, default="Argon")
    collision_pressure = models.FloatField(verbose_name="Pressure [mbar]", default=0.00001, blank=True, null=True)
    collision_energy = models.FloatField(verbose_name="Energy [eV]", blank=True, null=True)
    coll_bronk = models.FloatField(verbose_name="Coll bronki [a.U.]", default=99, blank=True, null=True)

    # this provides a link to the data file in the admin interface
    def get_data_file(self):
        return mark_safe("<a href='%s' download>Data file</a>" % ('/files/' + str(self.data_file)))

    def get_short_description(self):
        return "{}...".format(self.short_description[:30])

    def __str__(self):
        return f"ID {self.id}, {self.time}, {self.short_description}"

    class Meta:
        ordering = ['-time']
        get_latest_by = 'time'


class JournalEntry(BasicJournalEntry):
    pass
